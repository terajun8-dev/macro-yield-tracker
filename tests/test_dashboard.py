from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pandas as pd
from openpyxl import load_workbook

from src.excel_builder import build_workbook
from src.fetcher import _parse_mof_date, add_market_notes, fetch_yahoo_market_data
from src.main import _render_readme_section


class FetcherTests(unittest.TestCase):
    def test_parse_mof_era_dates(self):
        self.assertEqual(_parse_mof_date("S49.9.24").date(), date(1974, 9, 24))
        self.assertEqual(_parse_mof_date("R8.10.1").date(), date(2026, 10, 1))

    def test_yield_note_uses_basis_points(self):
        observations = pd.DataFrame(
            [
                {"Date": date(2026, 10, 1), "Indicator": "JGB 10Y", "Symbol": "MOF:JGB:10Y", "Value": 1.0, "PriceType": "Yield"},
                {"Date": date(2026, 10, 2), "Indicator": "JGB 10Y", "Symbol": "MOF:JGB:10Y", "Value": 1.05, "PriceType": "Yield"},
            ]
        )
        noted = add_market_notes(observations)
        self.assertEqual(noted.iloc[1]["Note"], "前回取得日比: 1日 / 前日比: +5.0 bp")

    def test_yahoo_fetch_includes_topix_etf_separately(self):
        from unittest.mock import patch

        def fake_download(symbol, indicator):
            return pd.DataFrame(
                [{"Date": date(2026, 10, 1), "Indicator": indicator, "Symbol": symbol, "Value": 420.0, "PriceType": "Price"}]
            )

        with patch("src.fetcher._download_yahoo_symbol", side_effect=fake_download) as download:
            data = fetch_yahoo_market_data()

        self.assertIn("1306.T", data["Symbol"].values)
        self.assertIn(
            "TOPIX連動ETF (NEXT FUNDS TOPIX連動型上場投信)",
            data.loc[data["Symbol"] == "1306.T", "Indicator"].values,
        )
        download.assert_any_call("1306.T", "TOPIX連動ETF (NEXT FUNDS TOPIX連動型上場投信)")


class ExcelBuilderTests(unittest.TestCase):
    def test_workbook_contains_formula_dashboard_and_required_sheets(self):
        observations = pd.DataFrame(
            [
                {"Date": date(2026, 10, 1), "Indicator": "日本国債2年利回り", "Symbol": "MOF:JGB:2Y", "Value": 1.0, "PriceType": "Yield", "Note": "初回取得"},
                {"Date": date(2026, 10, 2), "Indicator": "日本国債2年利回り", "Symbol": "MOF:JGB:2Y", "Value": 1.05, "PriceType": "Yield", "Note": "前日比: +5.0 bp"},
            ]
        )
        with TemporaryDirectory() as directory:
            output_path = build_workbook(observations, [], Path(directory) / "dashboard.xlsx")
            workbook = load_workbook(output_path, data_only=False)
            self.assertEqual(workbook.sheetnames, ["Dashboard", "History", "Charts", "MarketData"])
            dashboard = workbook["Dashboard"]
            row = next(
                index
                for index in range(2, dashboard.max_row + 1)
                if dashboard.cell(index, 2).value == "MOF:JGB:2Y"
            )
            self.assertIn("MAXIFS", dashboard.cell(row, 3).value)
            self.assertIn("MarketData[Symbol]", dashboard.cell(row, 5).value)
            self.assertIn(f"(E{row}-F{row})*100", dashboard.cell(row, 8).value)


class ReadmeTests(unittest.TestCase):
    def test_unavailable_symbol_is_listed_explicitly(self):
        observations = pd.DataFrame(
            [
                {"Date": date(2026, 10, 1), "Indicator": "日経平均株価", "Symbol": "^N225", "Value": 60000.0, "PriceType": "Price", "Note": "初回取得"},
            ]
        )
        section = _render_readme_section(observations, [])
        topix_row = next(line for line in section.splitlines() if "`^TPX`" in line)
        self.assertIn("| 種別 | 注記 |", section)
        self.assertIn("| 価格 |", next(line for line in section.splitlines() if "`^N225`" in line))
        self.assertIn("データなし", topix_row)
        self.assertIn("価格", topix_row)
        etf_row = next(line for line in section.splitlines() if "`1306.T`" in line)
        self.assertIn("TOPIX連動ETF", etf_row)
        self.assertIn("NEXT FUNDS TOPIX連動型上場投信", etf_row)


if __name__ == "__main__":
    unittest.main()