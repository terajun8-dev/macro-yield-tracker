"""Generate an educational Japanese market report with the Gemini API."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import pandas as pd

from .config import (
    GEMINI_MODEL,
    INDICATORS,
    JAPAN_TIMEZONE,
    JGB_INDICATORS,
    SYMBOL_UNITS,
)
from .fetcher import _remove_isolated_etf_price_spikes
from .news_fetcher import fetch_related_news


GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GEMINI_FALLBACK_MODELS = (
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
)
REQUIRED_REPORT_HEADINGS = (
    "### 今日の市場をひとことで",
    "### 主な指標の動き",
    "### 国内外のニュースと市場の反応",
    "### オルカン・S&P 500を保有する人向けの見方",
    "### チャートで見る直近の流れ",
)
REPORT_NUMBER_PATTERN = re.compile(r"(?<![\d.,])[+-]?\d[\d,]*(?:\.\d+)?")
ISO_DATE_PATTERN = re.compile(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b")
TIME_PATTERN = re.compile(r"\b(\d{1,2}):(\d{2})\b")
REPORT_STATIC_NUMBERS = {0.01, 1, 2, 3, 5, 10, 20, 30, 500}


def _build_market_context(data: pd.DataFrame) -> dict:
    data = _remove_isolated_etf_price_spikes(data)
    expected_symbols = {symbol: name for name, symbol in INDICATORS.items()}
    expected_symbols.update(JGB_INDICATORS)
    series = []
    for symbol, observations in data.sort_values("Date").groupby("Symbol"):
        observations = observations.sort_values("Date")
        recent = observations.tail(5)
        first = observations.iloc[0]
        latest = observations.iloc[-1]
        previous = observations.iloc[-2] if len(observations) > 1 else None
        is_yield = str(latest["PriceType"]) == "Yield"

        def summarize_change(start_value: float, end_value: float) -> dict:
            difference = float(end_value) - float(start_value)
            summary = {"difference": round(difference, 6)}
            if is_yield:
                summary["basis_points"] = round(difference * 100, 2)
            elif start_value:
                summary["percent"] = round(difference / abs(float(start_value)) * 100, 3)
            return summary

        low = observations.loc[observations["Value"].idxmin()]
        high = observations.loc[observations["Value"].idxmax()]
        series.append(
            {
                "indicator": str(latest["Indicator"]),
                "symbol": str(symbol),
                "type": str(latest["PriceType"]),
                "unit": SYMBOL_UNITS.get(str(symbol), str(latest["PriceType"])),
                "latest": {
                    "date": pd.to_datetime(latest["Date"]).date().isoformat(),
                    "value": round(float(latest["Value"]), 6),
                },
                "change_since_previous_observation": (
                    {
                        "previous_date": pd.to_datetime(previous["Date"]).date().isoformat(),
                        **summarize_change(previous["Value"], latest["Value"]),
                    }
                    if previous is not None
                    else None
                ),
                "chart_period_summary": {
                    "from": pd.to_datetime(first["Date"]).date().isoformat(),
                    "to": pd.to_datetime(latest["Date"]).date().isoformat(),
                    "observation_count": int(len(observations)),
                    "first_value": round(float(first["Value"]), 6),
                    "change_from_first": summarize_change(first["Value"], latest["Value"]),
                    "low": {
                        "date": pd.to_datetime(low["Date"]).date().isoformat(),
                        "value": round(float(low["Value"]), 6),
                    },
                    "high": {
                        "date": pd.to_datetime(high["Date"]).date().isoformat(),
                        "value": round(float(high["Value"]), 6),
                    },
                },
                "recent_observations": [
                    {
                        "date": pd.to_datetime(row.Date).date().isoformat(),
                        "value": round(float(row.Value), 6),
                    }
                    for row in recent.itertuples()
                ],
            }
        )

    available_symbols = set(data["Symbol"].astype(str))
    market_dates = [
        pd.to_datetime(item["latest"]["date"])
        for item in series
        if item["type"] != "Yield"
    ]
    latest_market_date = max(market_dates) if market_dates else None
    for item in series:
        if item["type"] == "Yield" and latest_market_date is not None:
            yield_date = pd.to_datetime(item["latest"]["date"])
            item["lag_vs_latest_market_days"] = (latest_market_date - yield_date).days

    related_news = fetch_related_news(limit=4)
    return {
        "as_of_jst": datetime.now(ZoneInfo(JAPAN_TIMEZONE)).strftime("%Y-%m-%d %H:%M %Z"),
        "latest_market_date": (
            latest_market_date.date().isoformat() if latest_market_date is not None else None
        ),
        "markets": series,
        "currency_return_comparisons": _build_currency_return_comparisons(data),
        "related_news": related_news,
        "unavailable_indicators": [
            {"indicator": name, "symbol": symbol}
            for symbol, name in expected_symbols.items()
            if symbol not in available_symbols
        ],
    }


def _build_currency_return_comparisons(data: pd.DataFrame) -> list[dict]:
    """Compare USD price returns with indicative JPY-converted returns."""
    fx = data.loc[data["Symbol"] == "USDJPY=X", ["Date", "Value"]].rename(
        columns={"Value": "jpy_per_usd"}
    )
    if fx.empty:
        return []

    comparisons = []
    for symbol in ("ACWI", "^GSPC"):
        prices = data.loc[data["Symbol"] == symbol, ["Date", "Value"]].rename(
            columns={"Value": "usd_price"}
        )
        matched = prices.merge(fx, on="Date", how="inner").sort_values("Date")
        if len(matched) < 2:
            continue
        first, latest = matched.iloc[0], matched.iloc[-1]
        if first["usd_price"] <= 0 or first["jpy_per_usd"] <= 0:
            continue
        usd_return = (latest["usd_price"] / first["usd_price"] - 1) * 100
        jpy_return = (
            latest["usd_price"]
            * latest["jpy_per_usd"]
            / (first["usd_price"] * first["jpy_per_usd"])
            - 1
        ) * 100
        comparisons.append(
            {
                "indicator": str(data.loc[data["Symbol"] == symbol, "Indicator"].iloc[-1]),
                "symbol": symbol,
                "from": pd.to_datetime(first["Date"]).date().isoformat(),
                "to": pd.to_datetime(latest["Date"]).date().isoformat(),
                "usd_price_return_percent": round(float(usd_return), 3),
                "indicative_jpy_return_percent": round(float(jpy_return), 3),
                "fx_effect_percentage_points": round(float(jpy_return - usd_return), 3),
                "method": "同日終値を使用。配当・手数料・税金を含まない価格リターン。",
            }
        )
    return comparisons


def _report_number_facts(context: dict) -> set[float]:
    facts = set(REPORT_STATIC_NUMBERS)

    def collect(value) -> None:
        if isinstance(value, dict):
            for item in value.values():
                collect(item)
        elif isinstance(value, list):
            for item in value:
                collect(item)
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            number = float(value)
            for precision in range(7):
                facts.add(round(number, precision))
        elif isinstance(value, str):
            for match in ISO_DATE_PATTERN.finditer(value):
                facts.update(float(part) for part in match.groups())
            for match in TIME_PATTERN.finditer(value):
                facts.update(float(part) for part in match.groups())

    collect({key: value for key, value in context.items() if key != "related_news"})
    return facts


def _validate_report_numbers(report: str, context: dict) -> None:
    """Reject market-section numbers that cannot be traced to supplied data."""
    facts = _report_number_facts(context)
    symbols = {
        str(market["symbol"])
        for market in context.get("markets", [])
        if market.get("symbol")
    }
    sections = re.split(r"(?m)(?=^### )", report)
    market_text = "\n".join(
        section
        for section in sections
        if not section.startswith("### 国内外のニュースと市場の反応")
        and not section.startswith("### 参照したニュース・資料")
    )
    market_text = ISO_DATE_PATTERN.sub(
        lambda match: " ".join(match.groups()), market_text
    )
    market_text = market_text.replace("−", "-").replace("＋", "+")
    for symbol in sorted(symbols, key=len, reverse=True):
        market_text = re.sub(
            rf"(?<![A-Za-z0-9]){re.escape(symbol)}(?![A-Za-z0-9])",
            "",
            market_text,
        )
    unsupported = []
    for match in REPORT_NUMBER_PATTERN.finditer(market_text):
        try:
            number = float(match.group().replace(",", ""))
        except ValueError:
            continue
        if number not in facts:
            unsupported.append(match.group())
    if unsupported:
        values = ", ".join(dict.fromkeys(unsupported))
        raise RuntimeError(f"Gemini report contains unsupported market numbers: {values}.")


def _build_prompt(context: dict) -> str:
    serialized_context = json.dumps(context, ensure_ascii=False, indent=2)
    return f"""あなたは金融リテラシーを支援するマーケット解説者です。JSONの市場データとGoogle Search groundingで確認できたニュースを使い、初心者にも知識のある読者にも読み応えのある日本語Markdown日次レポートを書いてください。

必ず守ること:
- 日付、数値、値動きはJSONの値を正確に使い、直前観測日と最新日の違いを「前営業日」と決めつけない。
- 観測事実、ニュースで確認できる事実、一般的な市場解釈を明確に区別する。ニュースと値動きの因果関係は裏付けがある場合だけ述べる。
- 一次データにない市場数値・変化率・因果関係を作らない。ニュースは検索で記事本文を確認できた事実のみを、出典名と記事の日付（確認できる場合）付きで記述する。検索結果の見出しだけから詳細や因果を推測しない。
- ニュース節以外の市場数値は、JSONの観測値またはそこから計算できる変化だけを使う。検証できない数値は書かず、必要ならデータ不足と説明する。
- `chart_period_summary` は生成済みチャートの全期間を表す。短期の値動きだけでなく、期間の始点からの変化やレンジ内の位置も使い、チャートの傾向を文章で説明する。
- Google Search groundingで国内・海外の市場関連ニュースを調べる。JSONの`related_news`は検索の手掛かりとして扱い、記事内容を確認できない場合は断定しない。検索結果が得られない場合はその旨を明示する。
- JSONにない市場価格やニュース内容を作らず、最新データの対象日が異なる場合はその違いを説明する。
- オルカン（全世界株式）とS&P 500の長期保有者向けの一般的な見方を含める。個人別の売買・配分指示、短期予測、利益保証はしない。
- TOPIX連動ETFの価格をTOPIX指数そのものとして扱わない。
- 各系列の`unit`を明記し、価格・指数ポイント・利回り・為替レートを混同しない。TOPIXデータがない場合、ETFの値を指数の代用値にせず、別商品の参考価格として区別する。
- 利回り変化はbpのみで表記し、%での変化幅を重ねて書かない。更新日の遅い利回りは`lag_vs_latest_market_days`を確認し、最新株価との関係や因果を述べない。
- 専門用語（bp、利回り、ボラティリティ等）は初出時に短く説明し、煽らず、観測値と解釈を丁寧に結びつける。
- 各見出しの後に、数値に基づく具体的な本文を3〜5文書く。データがない場合は無理に数字を作らず、その制約を伝える。
- 全体で1000〜1600文字程度を目安にし、主要市場の連動関係と、異なる見方が成り立つ理由も説明する。
- 見出しは次の順で使い、前後にコードフェンスや余分な挨拶を付けない: `### 今日の市場をひとことで` → `### 主な指標の動き` → `### 国内外のニュースと市場の反応` → `### オルカン・S&P 500を保有する人向けの見方` → `### チャートで見る直近の流れ`
- 「主な指標」では日本株・米国株・為替・日米金利・VIX・ETFから入手できたものを比較し、株式・為替・金利のつながりを説明する。各値はJSONの単位を明記し、ETF価格と指数値を区別する。
- 「国内外のニュース」では検索で確認できた国内と海外の材料を最低1件ずつ挙げ、ニュースの出典・日付と相場への関連を簡潔に記す。
- 「チャートで見る直近の流れ」では直近数観測とチャート全期間の方向、期間高安を区別し、更新日の異なる指標を同列比較しない。利回りの`lag_vs_latest_market_days`が5日を超える場合、最新株価との連動・因果を述べない。
- 見出しのあとに本文がない、または途中で見出しが切れる出力はしない。

出力テンプレートの例:
### 今日の市場をひとことで
日本市場では...（対象日、最新値、直前観測比）となり、米国株...やドル円...と対照的な動きでした。チャート全期間では...から...へ推移しており、当日の変化が長期傾向と同じ方向かも確認できます。ニュースでは...が報じられていますが、値動きとの因果は...の範囲で捉える必要があります。総じて...という局面ですが、...には注意が必要です。

### 主な指標の動き
日経平均...、TOPIX...、TOPIX連動ETF...、S&P 500...でした。ドル円...に対し、米国債・日本国債利回りは...、VIXは...です。価格変化と利回り変化（bp）の単位の違いを説明し、確認できる連動と解釈の限界を示します。取得できなかった系列は欠測として扱います。

### 国内外のニュースと市場の反応
国内では...（出典、日付）、海外では...が確認できます。...という市場データとの関係は考えられますが、直接の因果が確認できない場合は可能性として表現します。検索で確認できた記事が不足する場合は、その制約を明記します。

### オルカン・S&P 500を保有する人向けの見方
`currency_return_comparisons`がある場合は、同じ期間のUSD建て価格リターンと、為替を反映した円換算リターンを数値で分けて説明します。これは為替込みの参考比較で、投資信託の実績（配当・費用・税金を含むもの）とは異なります。為替データが不足する場合は円換算値を推測しません。金利は更新日の差を踏まえて説明し、短期変動と長期分散投資の考え方を分けます。

### チャートで見る直近の流れ
直近の数観測では...、チャート期間（...から...）では...でした。期間高値...・安値...のどこに現在値があるかを示し、短期の反発・下落と全期間の方向が異なる場合は両方を説明します。市場ごとの休場日やデータ更新差にも触れます。

市場データ（JST基準、各銘柄は直近最大5観測）:
{serialized_context}
"""


def generate_daily_report(
    data: pd.DataFrame,
    api_key: str | None = None,
    model: str | None = None,
) -> str | None:
    """Return a Gemini-generated Markdown report, or None when the API is unavailable."""
    api_key = api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None

    market_context = _build_market_context(data)
    preferred_models = []
    configured_model = model or os.environ.get("GEMINI_MODEL") or GEMINI_MODEL
    preferred_models.append(configured_model)
    preferred_models.extend(model for model in GEMINI_FALLBACK_MODELS if model != configured_model)

    last_error: Exception | None = None
    for model_name in dict.fromkeys(preferred_models):
        url = GEMINI_API_URL.format(model=quote(model_name, safe=""))
        generation_config = {"temperature": 0.3, "maxOutputTokens": 8192}
        if model_name.startswith("gemini-2.5"):
            generation_config["thinkingConfig"] = {"thinkingBudget": 1024}
        payload = {
            "contents": [{"role": "user", "parts": [{"text": _build_prompt(market_context)}]}],
            "tools": [{"google_search": {}}],
            "generationConfig": generation_config,
        }
        request = Request(
            url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
            method="POST",
        )
        try:
            with urlopen(request, timeout=90) as response:
                result = json.loads(response.read().decode("utf-8"))
            break
        except HTTPError as error:
            last_error = error
            print(f"Gemini HTTP error for model {model_name}: {error.code} {error.reason}")
            if error.code == 404:
                continue
            return None
        except Exception as error:  # pragma: no cover - defensive guard for network errors.
            last_error = error
            print(f"Gemini request failed for model {model_name}: {type(error).__name__}: {error}")
            return None
    else:
        if last_error is not None:
            print(f"Gemini API request failed for all models ({type(last_error).__name__}: {last_error}). AI日次レポートをスキップします.")
        return None

    candidates = result.get("candidates") or []
    if not candidates:
        raise RuntimeError("Gemini API returned no report candidates.")
    candidate = candidates[0]
    parts = candidate.get("content", {}).get("parts", [])
    report = "\n".join(part.get("text", "") for part in parts).strip()
    if not report:
        raise RuntimeError("Gemini API returned an empty report.")
    missing_headings = [heading for heading in REQUIRED_REPORT_HEADINGS if heading not in report]
    if missing_headings or candidate.get("finishReason") == "MAX_TOKENS":
        missing = ", ".join(missing_headings) or "none"
        raise RuntimeError(
            f"Gemini returned an incomplete report (missing sections: {missing}; "
            f"finishReason: {candidate.get('finishReason', 'unknown')})."
        )
    _validate_report_numbers(report, market_context)

    source_links = []
    seen_urls = set()
    metadata = candidate.get("groundingMetadata", {})
    for chunk in metadata.get("groundingChunks", []):
        web_source = chunk.get("web", {})
        title = str(web_source.get("title") or "参照記事").strip()
        uri = str(web_source.get("uri") or "").strip()
        if uri.startswith(("https://", "http://")) and uri not in seen_urls:
            source_links.append(f"- [{title}]({uri})")
            seen_urls.add(uri)
    if source_links:
        report += "\n\n### 参照したニュース・資料\n" + "\n".join(source_links)
    return report