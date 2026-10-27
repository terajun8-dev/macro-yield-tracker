"""Download market history from Yahoo Finance and JGB yields from Japan's MOF."""

from __future__ import annotations

import re
from datetime import date
from io import BytesIO

import pandas as pd
import yfinance as yf

from .config import (
    HISTORY_PERIOD,
    JGB_INDICATORS,
    JGB_SYMBOLS,
    MOF_JGB_URL,
    JP_ETF_SYMBOLS,
    SYMBOL_PRICE_TYPES,
    SYMBOL_TO_INDICATOR,
    US_SYMBOLS,
    JP_MARKET_SYMBOLS,
)


def _parse_mof_date(value: object) -> pd.Timestamp:
    """Convert MOF era dates (for example, R8.10.1) to Gregorian dates."""
    text = str(value).strip()
    era_match = re.fullmatch(r"([MTSHR])\s*(\d+)\.(\d{1,2})\.(\d{1,2})", text)
    if era_match:
        era, era_year, month, day = era_match.groups()
        era_start_year = {"M": 1868, "T": 1912, "S": 1926, "H": 1989, "R": 2019}[era]
        return pd.Timestamp(
            year=era_start_year + int(era_year) - 1,
            month=int(month),
            day=int(day),
        )

    parsed = pd.to_datetime(text, errors="coerce")
    if pd.isna(parsed):
        raise ValueError(f"MOFの日付を解釈できません: {text}")
    return pd.Timestamp(parsed).normalize()


def _download_yahoo_symbol(symbol: str, indicator: str) -> pd.DataFrame:
    history = yf.Ticker(symbol).history(
        period=HISTORY_PERIOD,
        interval="1d",
        auto_adjust=False,
        actions=False,
    )
    if history.empty or "Close" not in history:
        raise ValueError(f"Yahoo Financeからデータを取得できません: {symbol}")

    values = pd.to_numeric(history["Close"], errors="coerce")
    result = pd.DataFrame({"Date": pd.to_datetime(history.index).date, "Value": values})
    result = result.dropna(subset=["Value"])
    result["Indicator"] = indicator
    result["Symbol"] = symbol
    result["PriceType"] = SYMBOL_PRICE_TYPES[symbol]
    return result[["Date", "Indicator", "Symbol", "Value", "PriceType"]]


def fetch_yahoo_market_data() -> pd.DataFrame:
    """Fetch all configured Yahoo symbols once, including the shared USD/JPY pair."""
    yahoo_indicators = {**US_SYMBOLS, **JP_MARKET_SYMBOLS, **JP_ETF_SYMBOLS}
    rows = []
    errors = []
    for indicator, symbol in yahoo_indicators.items():
        try:
            rows.append(_download_yahoo_symbol(symbol, indicator))
        except Exception as error:  # Keep a partial dashboard if one Yahoo symbol fails.
            errors.append(f"{indicator} ({symbol}): {error}")

    if not rows:
        raise RuntimeError("Yahoo Financeから市場データを1件も取得できませんでした。")
    if errors:
        print("Yahoo Finance取得警告:\n- " + "\n- ".join(errors))
    return pd.concat(rows, ignore_index=True)


def fetch_jgb_from_mof() -> pd.DataFrame:
    """Fetch MOF's full JGB curve and extract the 2/5/10/20/30-year yields."""
    response = pd.io.common.urlopen(MOF_JGB_URL, timeout=30)
    try:
        content = response.read()
    finally:
        response.close()

    source = pd.read_csv(BytesIO(content), encoding="cp932", header=1)
    date_column = source.columns[0]
    source["Date"] = source[date_column].map(_parse_mof_date).dt.date
    years = int(HISTORY_PERIOD.removesuffix("y"))
    cutoff = (pd.Timestamp.today().normalize() - pd.DateOffset(years=years)).date()
    source = source.loc[source["Date"] >= cutoff]

    rows = []
    for tenor, symbol in JGB_SYMBOLS.items():
        column = next(
            (name for name in source.columns if re.fullmatch(rf"\s*{tenor}\s*年\s*", str(name))),
            None,
        )
        if column is None:
            raise ValueError(f"MOF CSVに{tenor}年列がありません。")
        values = pd.to_numeric(source[column].replace("-", pd.NA), errors="coerce")
        tenor_rows = pd.DataFrame({"Date": source["Date"], "Value": values}).dropna(subset=["Value"])
        tenor_rows["Indicator"] = JGB_INDICATORS[symbol]
        tenor_rows["Symbol"] = symbol
        tenor_rows["PriceType"] = "Yield"
        rows.append(tenor_rows)

    return pd.concat(rows, ignore_index=True)[
        ["Date", "Indicator", "Symbol", "Value", "PriceType"]
    ]


def add_market_notes(data: pd.DataFrame) -> pd.DataFrame:
    """Annotate each observation with its gap and change from the prior observation."""
    result = data.sort_values(["Symbol", "Date"]).copy()
    previous_value = result.groupby("Symbol")["Value"].shift(1)
    previous_date = result.groupby("Symbol")["Date"].shift(1)
    current_date = pd.to_datetime(result["Date"])
    previous_date_parsed = pd.to_datetime(previous_date)
    day_gap = (current_date - previous_date_parsed).dt.days
    change = result["Value"] - previous_value
    percent_change = change.div(previous_value.abs().replace(0, pd.NA)) * 100

    notes = []
    for index, row in result.iterrows():
        if pd.isna(previous_value.loc[index]):
            notes.append("初回取得")
            continue
        gap = int(day_gap.loc[index])
        if row["PriceType"] == "Yield":
            notes.append(
                f"前回観測から{gap}日 / 変化: {change.loc[index] * 100:+.1f} bp"
            )
        else:
            notes.append(
                f"前回観測から{gap}日 / 変化: {change.loc[index]:+.4g}"
                f" ({percent_change.loc[index]:+.2f}%)"
            )
    result["Note"] = notes
    return result.sort_values(["Date", "Symbol"]).reset_index(drop=True)


def _remove_isolated_etf_price_spikes(data: pd.DataFrame) -> pd.DataFrame:
    """Drop single-observation ETF price spikes that immediately reverse."""
    symbol = next(iter(JP_ETF_SYMBOLS.values()))
    etf = data.loc[
        (data["Symbol"] == symbol) & (data["PriceType"] == "Price")
    ].sort_values("Date")
    if len(etf) < 3:
        return data

    suspicious_indices = []
    values = etf["Value"].to_numpy(dtype=float)
    for position in range(1, len(etf) - 1):
        previous, current, following = values[position - 1 : position + 2]
        if previous <= 0 or current <= 0 or following <= 0:
            continue
        span = pd.to_datetime(etf.iloc[position + 1]["Date"]) - pd.to_datetime(
            etf.iloc[position - 1]["Date"]
        )
        is_large_move = current < previous * 0.5 or current > previous * 1.5
        immediately_reverses = abs(following / previous - 1) <= 0.1
        if span <= pd.Timedelta(days=7) and is_large_move and immediately_reverses:
            row = etf.iloc[position]
            suspicious_indices.append(row.name)
            print(
                "市場データ品質警告: "
                f"{symbol} の {row['Date']} の値 {current:g} は前後の観測と整合しないため除外します。"
            )

    return data.drop(index=suspicious_indices) if suspicious_indices else data


def fetch_market_data() -> pd.DataFrame:
    """Fetch and normalize Yahoo and MOF observations into a single long table."""
    yahoo_data = fetch_yahoo_market_data()
    jgb_data = fetch_jgb_from_mof()
    combined = pd.concat([yahoo_data, jgb_data], ignore_index=True)
    return add_market_notes(_remove_isolated_etf_price_spikes(combined))