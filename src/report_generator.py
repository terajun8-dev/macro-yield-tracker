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


GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


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
    return {
        "as_of_jst": datetime.now(ZoneInfo(JAPAN_TIMEZONE)).strftime("%Y-%m-%d %H:%M %Z"),
        "markets": series,
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
- オルカン（全世界株式）とS&P 500の長期保有者向けの一般的な見方を含める。個人別の売買・配分指示、短期予測、利益保証はしない。
- TOPIX連動ETFの価格をTOPIX指数そのものとして扱わない。
- 専門用語は短く説明し、煽らず、簡潔にする。
- 次の4つの見出しをこの順で使い、前後にコードフェンスや余分な挨拶を付けない。
  1. `### 今日の市場をひとことで`
  2. `### 主な指標の動き`
  3. `### オルカン・S&P 500を保有する人向けの見方`
  4. `### 直近数営業日の動向`

市場データ（JST基準、各銘柄は直近最大5観測）:
{serialized_context}
"""


def generate_daily_report(
    data: pd.DataFrame,
    api_key: str | None = None,
    model: str | None = None,
) -> str | None:
    """Return a Gemini-generated Markdown report, or None when no key is configured."""
    api_key = api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None

    model_name = model or os.environ.get("GEMINI_MODEL") or GEMINI_MODEL
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
    except HTTPError as error:
        raise RuntimeError(f"Gemini API request failed with HTTP {error.code}.") from None

    candidates = result.get("candidates") or []
    if not candidates:
        raise RuntimeError("Gemini API returned no report candidates.")
    parts = candidates[0].get("content", {}).get("parts", [])
    report = "\n".join(part.get("text", "") for part in parts).strip()
    if not report:
        raise RuntimeError("Gemini API returned an empty report.")
    return report