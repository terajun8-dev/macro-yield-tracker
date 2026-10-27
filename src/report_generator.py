"""Generate an educational Japanese market report with the Gemini API."""

from __future__ import annotations

import json
import os
from datetime import datetime
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

import pandas as pd

from .config import GEMINI_MODEL, INDICATORS, JAPAN_TIMEZONE, JGB_INDICATORS
from .news_fetcher import fetch_related_news


GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
GEMINI_FALLBACK_MODELS = (
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
)


def _build_market_context(data: pd.DataFrame) -> dict:
    expected_symbols = {symbol: name for name, symbol in INDICATORS.items()}
    expected_symbols.update(JGB_INDICATORS)
    series = []
    for symbol, observations in data.sort_values("Date").groupby("Symbol"):
        observations = observations.tail(5)
        latest = observations.iloc[-1]
        series.append(
            {
                "indicator": str(latest["Indicator"]),
                "symbol": str(symbol),
                "type": str(latest["PriceType"]),
                "recent_observations": [
                    {
                        "date": pd.to_datetime(row.Date).date().isoformat(),
                        "value": round(float(row.Value), 6),
                    }
                    for row in observations.itertuples()
                ],
            }
        )

    available_symbols = set(data["Symbol"].astype(str))
    related_news = fetch_related_news(limit=4)
    return {
        "as_of_jst": datetime.now(ZoneInfo(JAPAN_TIMEZONE)).strftime("%Y-%m-%d %H:%M %Z"),
        "markets": series,
        "related_news": related_news,
        "unavailable_indicators": [
            {"indicator": name, "symbol": symbol}
            for symbol, name in expected_symbols.items()
            if symbol not in available_symbols
        ],
    }


def _build_prompt(context: dict) -> str:
    serialized_context = json.dumps(context, ensure_ascii=False, indent=2)
    return f"""あなたは金融リテラシーを支援するマーケット解説者です。次のJSONに含まれる最新市場データだけを根拠に、初心者向けの日本語Markdown日次レポートを書いてください。

必ず守ること:
- 日付、数値、値動きはJSONの値を正確に使い、未提供の市場ニュースや値動きの原因を作らない。
- 観測事実と一般的な解釈を区別し、データがない指標や市場ごとの更新日の違いも必要に応じて説明する。
- 国内外の材料は、JSONに含まれる米国株・日本株・為替・債券・ETFの動きから読み取れる一般的な背景として説明する。実在のニュース記事本文を作らない。
- `related_news` がある場合は、それを「国内・海外の材料として要点を反映」する。ニュースが空の場合は、空であることを明言し、データベースの動きだけで解説する。
- オルカン（全世界株式）とS&P 500の長期保有者向けの一般的な見方を含める。個人別の売買・配分指示、短期予測、利益保証はしない。
- TOPIX連動ETFの価格をTOPIX指数そのものとして扱わない。
- 専門用語は短く説明し、煽らず、誤解のない表現にする。
- 各見出しの後に、3〜5文の本文を必ず書く。見出しだけで終わらせず、短い一言で切らない。
- 各見出しには、少なくとも1つの具体的な数値または変化率を含める。例: 「日経平均は○○円で、前日比△○○円」など。
- 全体で700〜1200文字程度の分量を目安にし、初心者にも理解しやすい文章にする。
- 次の4つの見出しをこの順で使い、前後にコードフェンスや余分な挨拶を付けない。
  1. `### 今日の市場をひとことで`
  2. `### 主な指標の動き`
  3. `### オルカン・S&P 500を保有する人向けの見方`
  4. `### 直近数営業日の動向`
- 見出しのあとに本文がない、または途中で見出しが切れる出力は絶対にしない。
- 各節で「国内の動き」「海外の動き」「為替と金利」「ETFの動き」のような材料を自然に含めて、広い視点でまとめる。
- もし `related_news` があるなら、国内の見出しと海外の見出しの両方を1つずつ取り上げて、相場への影響を簡潔に示す。
- 文章は「関連ニュース」を必ず何かしら含めるか、または「関連ニュースが十分にないため市場データに基づいて整理する」と明示する。

出力テンプレートの例:
### 今日の市場をひとことで
今日の日本市場では日経平均が... で、前日比で... と上昇しました。米国市場でも... が続き、為替は... に動いたため、日本株の上値を支えたと考えられます。国内外の材料が同時に影響しているため、短期的には... という見方が自然です。

### 主な指標の動き
日経平均は...、TOPIX連動ETFは...、ドル円は... でした。米10年債利回りが... であった一方で、VIX指数は... となり、リスク志向の強さと警戒感が同時に見られました。これらの動きから、国内外の市場参加者は... と受け止めていると考えられます。

### オルカン・S&P 500を保有する人向けの見方
オルカンとS&P 500の両方で... が続いており、長期保有者にとっては... と見るのが自然です。一方で、短期の値動きは... に左右されやすいため、相場の急変に備えて... を意識するのが大切です。

### 直近数営業日の動向
直近の数営業日では、日経平均は...、米国株は...、ドル円は... といった流れが続いています。特に... は今後の資金の流れを左右しやすく、国内外の投資家がどこに注目しているかを確認するうえで重要です。

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

    preferred_models = []
    configured_model = model or os.environ.get("GEMINI_MODEL") or GEMINI_MODEL
    preferred_models.append(configured_model)
    preferred_models.extend(model for model in GEMINI_FALLBACK_MODELS if model != configured_model)

    last_error: Exception | None = None
    for model_name in dict.fromkeys(preferred_models):
        url = GEMINI_API_URL.format(model=quote(model_name, safe=""))
        payload = {
            "contents": [{"role": "user", "parts": [{"text": _build_prompt(_build_market_context(data))}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1600},
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
    parts = candidates[0].get("content", {}).get("parts", [])
    report = "\n".join(part.get("text", "") for part in parts).strip()
    if not report:
        raise RuntimeError("Gemini API returned an empty report.")
    return report