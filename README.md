# macro-yield-tracker
財務省の国債利回り曲線や日米の金利、全世界株式などのマクロ指標を観測します。

## 実行

```bash
python -m pip install -r requirements.txt
python -m src.main
```

実行すると `output/market_dashboard.xlsx` と `output/charts/` を生成し、このファイル内の市場ダッシュボードを更新します。GitHub Actionsの `Update market dashboard` ワークフローが、平日18:00（日本時間）に自動更新します。手動実行はGitHubリポジトリの「Actions」から同ワークフローを開き、「Run workflow」を選択してください。

初回実行前に、リポジトリの「Settings」→「Actions」→「General」→「Workflow permissions」で、`GITHUB_TOKEN` の書き込みを許可してください。ワークフローはREADMEと `output/` を自動コミットします。

### Gemini日次レポートの設定

Google AI Studioで発行したキーを、リポジトリの「Settings」→「Secrets and variables」→「Actions」→「New repository secret」で `GEMINI_API_KEY` として登録してください。キーはソースやREADMEに書かず、GitHub Actionsのシークレットで管理します。キーが未設定の場合も市場データの更新は続行し、AIレポートの生成だけをスキップします。ローカル実行では、環境変数 `GEMINI_API_KEY` を設定してから `python -m src.main` を実行してください。ワークフロー実行1回につきGemini APIを1回呼び出すため、Google AI Studio側の利用枠・料金が適用されます。

関連ニュースを自動で取り込みたい場合は、`NEWS_API_KEY` を同じくGitHub Secretsに追加してください。未設定時でも、RSSのフォールバックで国内・海外の見出しを拾おうと試みます。キーがない場合は、ニュースを使わずに市場データだけで解説します。

<!-- MARKET-DASHBOARD:START -->
## 市場ダッシュボード

最終更新: 2026年10月27日 14:55 (JST)

| 指標 | シンボル | 最新値 | 前回値 | 前日比 | 種別 | 注記 |
|---|---|---:|---:|---:|---|---|
| MSCI ACWI | `ACWI` | 157.57 (2026-10-26) | 156.80 | +0.77 (+0.49%) | 価格 | 前回取得日比: 3日 / 前日比: +0.77 (+0.49%) |
| NASDAQ総合 | `^IXIC` | 26,169.38 (2026-10-26) | 25,955.34 | +214 (+0.82%) | 価格 | 前回取得日比: 3日 / 前日比: +214 (+0.82%) |
| NYダウ | `^DJI` | 52,361.58 (2026-10-26) | 52,215.16 | +146.4 (+0.28%) | 価格 | 前回取得日比: 3日 / 前日比: +146.4 (+0.28%) |
| S&P 500 | `^GSPC` | 7,676.77 (2026-10-26) | 7,623.68 | +53.09 (+0.70%) | 価格 | 前回取得日比: 3日 / 前日比: +53.09 (+0.70%) |
| TOPIX | `^TPX` | データなし | — | — | 価格 | この更新ではデータを取得できませんでした |
| TOPIX連動ETF (NEXT FUNDS TOPIX連動型上場投信) | `1306.T` | 420.00 (2026-10-27) | 418.40 | +1.6 (+0.38%) | 価格 | 前回取得日比: 1日 / 前日比: +1.6 (+0.38%) |
| VIX指数 | `^VIX` | 18.3900 (2026-10-26) | 19.4500 | -1.06 (-5.45%) | 価格 | 前回取得日比: 3日 / 前日比: -1.06 (-5.45%) |
| ドルインデックス | `DX-Y.NYB` | 102.08 (2026-10-27) | 101.96 | +0.122 (+0.12%) | 価格 | 前回取得日比: 1日 / 前日比: +0.122 (+0.12%) |
| ドル円 (USD/JPY) | `USDJPY=X` | 157.75 (2026-10-27) | 156.83 | +0.921 (+0.59%) | 価格 | 前回取得日比: 1日 / 前日比: +0.921 (+0.59%) |
| 日本国債10年利回り | `MOF:JGB:10Y` | 3.057% (2026-09-30) | 3.082% | -2.5 bp | 利回り | 前回取得日比: 1日 / 前日比: -2.5 bp |
| 日本国債20年利回り | `MOF:JGB:20Y` | 3.877% (2026-09-30) | 3.887% | -1.0 bp | 利回り | 前回取得日比: 1日 / 前日比: -1.0 bp |
| 日本国債2年利回り | `MOF:JGB:2Y` | 1.952% (2026-09-30) | 1.976% | -2.4 bp | 利回り | 前回取得日比: 1日 / 前日比: -2.4 bp |
| 日本国債30年利回り | `MOF:JGB:30Y` | 4.098% (2026-09-30) | 4.126% | -2.8 bp | 利回り | 前回取得日比: 1日 / 前日比: -2.8 bp |
| 日本国債5年利回り | `MOF:JGB:5Y` | 2.399% (2026-09-30) | 2.425% | -2.6 bp | 利回り | 前回取得日比: 1日 / 前日比: -2.6 bp |
| 日経平均株価 | `^N225` | 63,178.32 (2026-10-27) | 62,189.65 | +988.7 (+1.59%) | 価格 | 前回取得日比: 1日 / 前日比: +988.7 (+1.59%) |
| 米10年債利回り | `^TNX` | 4.986% (2026-10-26) | 4.988% | -0.2 bp | 利回り | 前回取得日比: 3日 / 前日比: -0.2 bp |
| 米13週国債利回り | `^IRX` | 4.025% (2026-10-26) | 4.032% | -0.7 bp | 利回り | 前回取得日比: 3日 / 前日比: -0.7 bp |

### 推移

#### 米国・グローバル市場

![米国・グローバル市場](output/charts/us-global.png)

#### 日本市場

![日本市場](output/charts/jp-market.png)

#### 日本市場・ETF

![日本市場・ETF](output/charts/jp-etf.png)

#### 日本国債利回り

![日本国債利回り](output/charts/jgb-yield.png)

### データソース

- 市場価格・指数・為替・米国債利回り: Yahoo Finance（`yfinance`）
- 日本国債の利回り曲線: 財務省「国債金利情報」CSV（2・5・10・20・30年）
- 利回りの前日比はbp（1bp = 0.01%）で表示しています。
<!-- MARKET-DASHBOARD:END -->

<!-- AI-DAILY-REPORT:START -->
## AIマーケット日次レポート

生成日時: 2026年10月27日 14:55 (JST)

### 今日の市場をひとことで
2026年10月27日の日本市場では、日経平均株価が前営業日比で1.59%高の63178.32円、TOPIX連動ETFも0.382%高の420.0円と、買い戻しが優勢となりました。これは、前営業日の米国市場で主要指数が上昇した流れを引き継いだものと見られます。一方、米国市場（10月26日終値）では、S&P 500が0.696%高、NASDAQ総合が0.825%高、NYダウが0.28%高と、主要3指数が揃って上昇しました。ドル円は157.751円と、前営業日比で0.587%のドル高円安に推移しています。チャート全期間（2024年10月28日から）では、日経平均株価が約63.65%上昇、TOPIX連動ETFも約50.7%上昇しており、当日の上昇は長期的な上昇傾向と一致しています。ニュースでは、ウクライナ南部での局地的な停戦合意や、イスラエル総選挙の投票開始などが報じられていますが、これらの地政学的な動きと市場の直接的な因果関係は現時点では明確ではありません。総じて、前日の米国株高を好感したリスクオンの局面ですが、中東情勢の不透明感や米長期金利の動向には引き続き注意が必要です。

### 主な指標の動き
2026年10月27日の日本市場では、日経平均株価が63178.32円、TOPIX連動ETFが420.0円でした。TOPIX指数はデータが取得できませんでした。米国市場（10月26日終値）では、NYダウが52361.58ドル、S&P 500が7676.77ドル、NASDAQ総合が26169.38ドル、MSCI ACWIが157.57ドルでした。

為替市場では、ドル円が157.751円と、前営業日（10月26日）の156.830円から0.921円のドル高円安となりました。ドルインデックスは102.082と、前営業日（10月26日）から0.120%上昇しています。

金利市場では、米10年債利回りが4.986%と、前回の観測日（10月23日）から-0.002%（-0.2ベーシスポイント、bp）とほぼ横ばいでした。ベーシスポイント（bp）とは、金利の変動幅を示す単位で、1bpは0.01%に相当します。米13週国債利回りは4.025%と、こちらも-0.7bpの低下でした。一方、日本国債10年利回りは3.057%（9月30日時点）と、前回の観測日（9月29日）から-2.5bp低下しています。日本国債のデータは9月30日時点と、株式市場や為替市場の最新データとは対象日が異なるため、直接的な連動関係を判断するには注意が必要です。

市場の不確実性を示すVIX指数は18.39と、前回の観測日（10月23日）から-5.45%低下しました。VIX指数は一般的に、数値が高いほど市場の不安心理が強いとされます。

### 国内外のニュースと市場の反応
国内では、2026年10月27日に「日米半導体協業フォーラム」が開催され、共同開発や技術提携の事例が紹介されました。米国半導体展示会「セミコンウェスト2026」の会期中にジェトロとカリフォルニア州知事室ビジネス・経済開発局が共催したもので、半導体関連企業の協業事例が複数紹介されています。前日の米国市場で半導体関連株が上昇したこともあり、このニュースは日本の半導体関連株にも好影響を与えた可能性があります。また、SBIホールディングスとスターテイルがブラックロックと共同で、トークン化MMFと円建てステーブルコイン「JPYSC」の連携に向けた基本合意書を締結したとの発表もありました。これは、日本におけるデジタル資産エコシステムの構築に向けた動きとして注目されます。

海外では、ロシアとウクライナがウクライナ南部オレシュキ市での局地的な停戦に合意し、日本時間27日午前10時に発効しました。これは人道支援活動を促進するためのもので、メラニア・トランプ米大統領夫人が仲介したと報じられています。また、イスラエルでは27日に総選挙の投票が始まり、ネタニヤフ首相の続投の可否が焦点となっています。この選挙は、2023年10月のハマスによる襲撃以降初めての国政選挙であり、中東情勢に影響を与える可能性があります。

米国市場では、生成AI大手のAnthropic（アンソロピック）が新規株式公開（IPO）に向けた登録届出書を公開し、2026年1〜6月の売上高が前年同期の約14倍に達していたことが明らかになりました。これにより、先週「AI投資の資金繰り」への懸念で売られていた半導体株に買い戻しが入り、米国株主要3指数が上昇する要因の一つとなりました。

### オルカン・S&P 500を保有する人向けの見方
MSCI ACWI（全世界株式）は2026年10月26日時点で157.57ドルとなり、2024年10月28日の観測開始時点から約31.92%上昇しています。S&P 500（米国主要500社）も同日時点で7676.77ドルと、観測開始時点から約31.82%上昇しており、世界株式と米国株式がほぼ同程度の成長を示していることがわかります。これは、MSCI ACWIにおいて米国株式の比率が高いことを反映していると考えられます。

為替市場ではドル円が157.751円と円安傾向にあり、円建てでこれらの資産を保有している場合、為替差益が評価額を押し上げる可能性があります。しかし、為替レートは常に変動するため、将来の評価額に影響を与える要因となります。また、米10年債利回りが約4.99%と高水準で推移していることは、株式の割引率に影響を与え、企業収益の将来価値評価に影響を及ぼし得ます。

長期的な分散投資を考える上で、オルカンやS&P 500のような広範囲に分散されたインデックスファンドは、個別の企業リスクを低減し、市場全体の成長を取り込むことを目指します。短期的な市場の変動に一喜一憂せず、自身の投資目標とリスク許容度に基づいた長期的な視点を持つことが重要です。個別の売買や資産配分については、ご自身の判断で行う必要があります。

### チャートで見る直近の流れ
TOPIX連動ETFは、直近の数観測（10月21日から27日）では425.60ドルから420.0ドルへと推移し、一時下落する場面もありましたが、最新日には反発しました。チャート全期間（2024年10月28日から2026年10月27日）では、278.70ドルから420.0ドルへと約50.7%上昇しており、長期的な上昇トレンドの中にあります。期間高値は2026年10月6日の440.40ドル、期間安値は2026年3月31日の37.14ドルであり、現在の値は期間高値に近い水準で推移しています。

日経平均株価も同様に、直近の数観測（10月21日から27日）では64621.24円から63178.32円へと推移し、一時下落しましたが、最新日には大きく反発しました。チャート期間（2024年10月28日から2026年10月27日）では、38605.53円から63178.32円へと約63.65%上昇しており、こちらも明確な上昇トレンドを示しています。期間高値は2026年6月25日の72366.34円、期間安値は2025年4月7日の31136.58円であり、現在の値は期間高値よりは低いものの、期間安値からは大きく上昇した位置にあります。

米国市場のS&P 500は、直近の数観測（10月20日から26日）では7712.57ドルから7676.77ドルへと推移し、一時的な調整が見られましたが、最新日には反発しました。チャート期間（2024年10月28日から2026年10月26日）では、5823.52ドルから7676.77ドルへと約31.82%上昇しています。期間高値は2026年10月6日の7818.93ドル、期間安値は2025年4月8日の4982.77ドルであり、現在の値は期間高値に迫る水準です。

なお、日本市場のデータは10月27日時点、米国市場のデータは10月26日時点、日本国債利回りのデータは9月30日時点と、市場や指標によって最新の更新日が異なります。これらの違いを考慮し、異なる指標を同列に比較する際には注意が必要です。

### 参照したニュース・資料
- [kabutan.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHHaZUObP8P2dLzHHPEFG4fI5_H78vdhGgsGmnrYX6jdm_MSCOW7gzYmdFXytYBr3lZybDSll9bpwcJM3YluEmiGoKXmHOcTMdTVDh3KDKI4utr8Gz37m84Bgs05yfm70RvUv4=)
- [kabutan.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHBpC46Uid3uALd6wkVgtX3kNmt7fiLnzQCNtlwGt5v-MshLoWojU5n3qHC17KhYJz10pWqABxxLUwgkZwDPYguUoeLt2ZgfcbWaOLWuSCLkV9f8cTTF_gZOG9wUp1pcrCK7n7GtIiSorVwG5bMVA==)
- [note.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGk35rFE2vH8CnmQsqyRVNiD9t9WKrviAxTCrZZ_tNwG8p7DAkezROGwnqZFVAWcbElCJkdtBsbyi5I029SeodgzeJntyNHY_xN8LGm_4kuTzpM0rlElijqYrpUZDG-s1Gv2kIaY21dfw==)
- [jetro.go.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH8vSdeMGjVVA-MfRrsqdZYYRIGVu2rMfLM1y5N-lUiDZuVNdegn1Hd-iPH-fus8bqdee_S-0FoaZgVtaTMXwFKKQ0rnaW-llUdcCndtcIFv1Tqzd2GfcbR8sDrTHITnXqD9n0FgF6ouSzlcoNKNLaAh6lyiotzvII=)
- [sbigroup.co.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH0cCoxXYVncp_h-vNAGqtPXf7VhAdSTNP4OCDdutc4dCmzMrYfd4n2fXFeoOENpFgXPOVEETyfXyrS5x-yyU-zJXD7YaHEigup-CC0QV99LH76mhY5eF_EFlCkYrRp0yaEE-RxyPhyjq74r2lWqTo=)
- [fnn.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGAs0p0uC0FndQIxZGzwp9eRdub3NBzCs_NwD2OYc5yMsIX2OabjH_t-APSTfKnmghP0SvcS5TzeW_dV5KlkCuWR8zP8O7hr8KlYH6z22VhAGMNBrWqiZ9vhBy5CaeeXGU=)
- [livedoor.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHJO0cdA91q_3ieB3OgF-uLBKAL9soEwtKj5wp5FLAy6oH9y2VdPOLFrBNvWK9mL3Naj9UQRKVLIemQZxcUtndUlIbHrKj7NQ6WPFWBRqSitebdNVoLCyz_olGI3NFcQcRX2RfAQzvQZ6UCF6k=)
- [afpbb.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGhBv99YgsUgMO5eel2t5mzWStQKNz_89jtm00MDElqn8vuxphgyrP_g6aHVla3_yFCxzP_GQ3jaOzLQwHHzu6I641eC0r8O_k_9iUpJr6a9DF9ubSqTIKd0vnOHU9AOK_pgck=)
- [mainichi.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGDeikHGrZ3E27vhYL_-00IV4koAqfUxet-zwTvSPS4cdUwpo77DpGKUb153scPwddJ6l3IHE28Q5iUb35uuT9aT6O_pvZ0JVQsZ6BagcBxM7PL0Qtt-auhygskF9qla7l7j4IFEiVDiDJYqgGXPFg8MU_PTQ==)
- [fnn.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFrmpBn7LgBumMj1AhLrYDpdqHF9X1JyQ6NfukaOSclZ3k5dQkASrgBJB-HJ00Uf0L-E3MiODUPVUvz6btGNdvyPP-NiuHsvg8tRJJ0oFpUzBKN_MuNpOkYdvveeCk8BtU=)
- [afpbb.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFYfxPkoYjYiv-xhNRj6BWTZVTUm3Z1gjnQ1n8FpRF383IZMS9O7saU49HOyW80FC_JXjRXyDlI_IyexFmpaHItRxM9CyAD1Dzzzd5xOu7xY2xl7tQNnR_biDnjrvlEDgNX4bo=)
- [dlri.co.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHDzzdgthyz6iq2SjRdVaqHk2uBE6MCNP_B0PWBE_LA-5t3fT_Lt5zl6HOmsaXPMctNPqAYceu11nF_-cqUS5IOj-GCDLvty8zrC2GK2eRjM_9Q0DG2upToRfThg1D11u1wW24jz0l-ZlZN)

※公開情報をもとにした一般的な解説です。特定の個人への投資助言ではありません。
<!-- AI-DAILY-REPORT:END -->
