"""Matplotlib charts used by the README and Excel workbook."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import pandas as pd

from .config import CHART_DIR, CHART_GROUPS


CHART_LABELS = {
    "^GSPC": "S&P 500",
    "^IXIC": "NASDAQ Composite",
    "^DJI": "Dow Jones Industrial Average",
    "^VIX": "VIX Index",
    "^TNX": "US 10Y Treasury Yield",
    "^IRX": "US 13W Treasury Yield",
    "ACWI": "MSCI ACWI",
    "USDJPY=X": "USD/JPY",
    "DX-Y.NYB": "US Dollar Index",
    "^N225": "Nikkei 225",
    "^TPX": "TOPIX",
    "1306.T": "TOPIX ETF (NEXT FUNDS 1306)",
    "MOF:JGB:2Y": "JGB 2Y Yield",
    "MOF:JGB:5Y": "JGB 5Y Yield",
    "MOF:JGB:10Y": "JGB 10Y Yield",
    "MOF:JGB:20Y": "JGB 20Y Yield",
    "MOF:JGB:30Y": "JGB 30Y Yield",
}


def configure_japanese_font() -> None:
    candidates = (
        "Noto Sans CJK JP",
        "Noto Sans JP",
        "IPAexGothic",
        "IPAGothic",
        "Yu Gothic",
        "Meiryo",
    )
    installed = {font.name for font in font_manager.fontManager.ttflist}
    selected = next((name for name in candidates if name in installed), None)
    if selected:
        plt.rcParams["font.family"] = selected
    plt.rcParams["axes.unicode_minus"] = False


def _indicator_name(symbol: str) -> str:
    return CHART_LABELS.get(symbol, symbol)


def render_market_charts(data: pd.DataFrame, output_dir: Path = CHART_DIR) -> list[Path]:
    """Render grouped small-multiple charts with portable labels and date axes."""
    configure_japanese_font()
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for group_name, symbols in CHART_GROUPS.items():
        present = [symbol for symbol in symbols if symbol in set(data["Symbol"])]
        if not present:
            continue
        columns = 2
        rows = (len(present) + columns - 1) // columns
        figure, axes = plt.subplots(rows, columns, figsize=(13, 3.2 * rows), squeeze=False)
        flat_axes = axes.ravel()
        for axis, symbol in zip(flat_axes, present):
            series = data.loc[data["Symbol"] == symbol].sort_values("Date")
            dates = pd.to_datetime(series["Date"])
            axis.plot(dates, series["Value"], color="#176b87", linewidth=1.6)
            axis.set_title(_indicator_name(symbol), loc="left", fontsize=10, fontweight="bold")
            axis.grid(axis="y", color="#d9e1e5", linewidth=0.7)
            axis.spines[["top", "right"]].set_visible(False)
            axis.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=6))
            axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
            axis.tick_params(axis="x", labelrotation=25, labelsize=8)
            axis.tick_params(axis="y", labelsize=8)
        for axis in flat_axes[len(present):]:
            axis.set_visible(False)

        figure.suptitle(group_name.replace("-", " ").upper(), x=0.03, ha="left", fontsize=13)
        figure.tight_layout(rect=(0, 0, 1, 0.96))
        path = output_dir / f"{group_name}.png"
        figure.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
        plt.close(figure)
        paths.append(path)
    return paths