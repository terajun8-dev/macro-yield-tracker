"""Project configuration for the market dashboard."""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT_DIR / "output"
CHART_DIR = OUTPUT_DIR / "charts"
WORKBOOK_PATH = OUTPUT_DIR / "market_dashboard.xlsx"
README_PATH = ROOT_DIR / "README.md"

HISTORY_PERIOD = "2y"
JAPAN_TIMEZONE = "Asia/Tokyo"
US_TIMEZONE = "America/New_York"
GEMINI_MODEL = "gemini-2.5-flash"
MOF_JGB_URL = "https://www.mof.go.jp/jgbs/reference/interest_rate/data/jgbcm_all.csv"
JGB_TENORS = (2, 5, 10, 20, 30)

US_SYMBOLS = {
    "S&P 500": "^GSPC",
    "NASDAQ総合": "^IXIC",
    "NYダウ": "^DJI",
    "VIX指数": "^VIX",
    "米10年債利回り": "^TNX",
    "米13週国債利回り": "^IRX",
    "MSCI ACWI": "ACWI",
    "ドル円 (USD/JPY)": "USDJPY=X",
    "ドルインデックス": "DX-Y.NYB",
}

JP_MARKET_SYMBOLS = {
    "日経平均株価": "^N225",
    "TOPIX": "^TPX",
    "ドル円 (USD/JPY)": "USDJPY=X",
}

JP_ETF_SYMBOLS = {
    "TOPIX連動ETF (NEXT FUNDS TOPIX連動型上場投信)": "1306.T",
}

JGB_SYMBOLS = {tenor: f"MOF:JGB:{tenor}Y" for tenor in JGB_TENORS}
JGB_INDICATORS = {
    JGB_SYMBOLS[tenor]: f"日本国債{tenor}年利回り" for tenor in JGB_TENORS
}

INDICATORS = {**US_SYMBOLS, **JP_MARKET_SYMBOLS, **JP_ETF_SYMBOLS}
SYMBOL_TO_INDICATOR = {symbol: name for name, symbol in INDICATORS.items()}
SYMBOL_PRICE_TYPES = {
    symbol: ("Yield" if symbol in {"^TNX", "^IRX"} else "Price")
    for symbol in SYMBOL_TO_INDICATOR
}
SYMBOL_PRICE_TYPES.update({symbol: "Yield" for symbol in JGB_SYMBOLS.values()})
SYMBOL_UNITS = {
    "^GSPC": "指数ポイント",
    "^IXIC": "指数ポイント",
    "^DJI": "指数ポイント",
    "^VIX": "指数ポイント",
    "^TNX": "%",
    "^IRX": "%",
    "ACWI": "USD/口",
    "USDJPY=X": "JPY/USD",
    "DX-Y.NYB": "指数ポイント",
    "^N225": "指数ポイント",
    "^TPX": "指数ポイント",
    "1306.T": "JPY/口",
    **{symbol: "%" for symbol in JGB_SYMBOLS.values()},
}

CHART_GROUPS = {
    "us-global": tuple(US_SYMBOLS.values()),
    "jp-market": tuple(JP_MARKET_SYMBOLS.values()),
    "jp-etf": tuple(JP_ETF_SYMBOLS.values()),
    "jgb-yield": tuple(JGB_SYMBOLS.values()),
}