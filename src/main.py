"""Run the market data refresh, workbook build, and README dashboard update."""

from __future__ import annotations

from datetime import datetime

import pandas as pd

from .charts import render_market_charts
from .config import (
    CHART_DIR,
    INDICATORS,
    JGB_INDICATORS,
    README_PATH,
    SYMBOL_PRICE_TYPES,
    WORKBOOK_PATH,
)
from .excel_builder import build_workbook
from .fetcher import fetch_market_data


START_MARKER = "<!-- MARKET-DASHBOARD:START -->"
END_MARKER = "<!-- MARKET-DASHBOARD:END -->"
REPORT_START_MARKER = "<!-- AI-DAILY-REPORT:START -->"
REPORT_END_MARKER = "<!-- AI-DAILY-REPORT:END -->"
CHART_GROUP_NAMES = {
    "us-global": "米国・グローバル市場",
    "jp-market": "日本市場",
    "jp-etf": "日本市場・ETF",
    "jgb-yield": "日本国債利回り",
}


def _format_value(value: float, price_type: str) -> str:
    if price_type == "Yield":
        return f"{value:.3f}%"
    if abs(value) >= 100:
        return f"{value:,.2f}"
    return f"{value:.4f}"


def _format_price_type(price_type: str) -> str:
    return {"Price": "価格", "Yield": "利回り"}.get(price_type, price_type)


def _render_readme_section(data: pd.DataFrame, chart_paths) -> str:
    latest = data.sort_values("Date").groupby("Symbol", as_index=False).tail(1)
    previous = data.sort_values("Date").groupby("Symbol").nth(-2).reset_index()
    previous_by_symbol = previous.set_index("Symbol") if not previous.empty else pd.DataFrame()
    latest_by_symbol = {row.Symbol: row for row in latest.itertuples(index=False)}
    indicator_by_symbol = {symbol: name for name, symbol in INDICATORS.items()}
    indicator_by_symbol.update(JGB_INDICATORS)
    lines = [
        "## 市場ダッシュボード",
        "",
        f"最終更新: {datetime.now().astimezone().strftime('%Y年%m月%d日 %H:%M (%Z)')}",
        "",
        "| 指標 | シンボル | 最新値 | 前回値 | 前日比 | 種別 | 注記 |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for symbol, indicator in sorted(indicator_by_symbol.items(), key=lambda item: item[1]):
        row = latest_by_symbol.get(symbol)
        if row is None:
            lines.append(
                f"| {indicator} | `{symbol}` | データなし | — | — "
                f"| {_format_price_type(SYMBOL_PRICE_TYPES[symbol])} | この更新ではデータを取得できませんでした |"
            )
            continue
        prior = previous_by_symbol.loc[row.Symbol] if row.Symbol in previous_by_symbol.index else None
        previous_value = prior.Value if prior is not None else None
        delta = row.Value - previous_value if previous_value is not None else None
        if delta is None:
            change_text = "初回"
        elif row.PriceType == "Yield":
            change_text = f"{delta * 100:+.1f} bp"
        else:
            percent = delta / abs(previous_value) * 100 if previous_value else 0
            change_text = f"{delta:+.4g} ({percent:+.2f}%)"
        note = row.Note.replace("|", "\\|")
        lines.append(
            f"| {row.Indicator} | `{row.Symbol}` | {_format_value(row.Value, row.PriceType)} "
            f"({row.Date}) | {(_format_value(previous_value, row.PriceType) if previous_value is not None else '—')} "
            f"| {change_text} | {_format_price_type(row.PriceType)} | {note} |"
        )
    lines.extend(["", "### 推移", ""])
    for path in chart_paths:
        relative = path.relative_to(README_PATH.parent).as_posix()
        title = CHART_GROUP_NAMES.get(path.stem, path.stem)
        lines.extend([f"#### {title}", "", f"![{title}]({relative})", ""])
    lines.extend(
        [
            "### データソース",
            "",
            "- 市場価格・指数・為替・米国債利回り: Yahoo Finance（`yfinance`）",
            "- 日本国債の利回り曲線: 財務省「国債金利情報」CSV（2・5・10・20・30年）",
            "- 利回りの前日比はbp（1bp = 0.01%）で表示しています。",
            "",
        ]
    )
    return "\n".join(lines)


def _replace_marked_section(content: str, start_marker: str, end_marker: str, section: str) -> str:
    if start_marker in content and end_marker in content:
        start = content.index(start_marker)
        end = content.index(end_marker) + len(end_marker)
        return content[:start] + section + content[end:]
    return content.rstrip() + "\n\n" + section + "\n"


def update_readme_dashboard(data: pd.DataFrame, chart_paths, daily_report: str | None = None) -> None:
    content = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else "# macro-yield-tracker\n"
    dashboard = f"{START_MARKER}\n{_render_readme_section(data, chart_paths)}{END_MARKER}"
    content = _replace_marked_section(content, START_MARKER, END_MARKER, dashboard)
    if daily_report:
        generated_at = datetime.now().astimezone().strftime("%Y年%m月%d日 %H:%M (%Z)")
        report_section = (
            f"{REPORT_START_MARKER}\n## AIマーケット日次レポート\n\n"
            f"生成日時: {generated_at}\n\n{daily_report.strip()}\n\n"
            "※公開情報をもとにした一般的な解説です。特定の個人への投資助言ではありません。\n"
            f"{REPORT_END_MARKER}"
        )
        content = _replace_marked_section(
            content, REPORT_START_MARKER, REPORT_END_MARKER, report_section
        )
    README_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    data = fetch_market_data()
    chart_paths = render_market_charts(data, CHART_DIR)
    build_workbook(data, chart_paths, WORKBOOK_PATH)
    from .report_generator import generate_daily_report

    try:
        daily_report = generate_daily_report(data)
    except RuntimeError as exc:
        print(f"AI日次レポートの生成に失敗したためスキップします: {exc}")
        daily_report = None
    if daily_report is None:
        print("GEMINI_API_KEYが未設定、モデル未対応、またはAPI利用制限により、AI日次レポートはスキップします。")
    update_readme_dashboard(data, chart_paths, daily_report)
    print(f"README、{WORKBOOK_PATH.relative_to(README_PATH.parent)}、グラフを更新しました。")


if __name__ == "__main__":
    main()