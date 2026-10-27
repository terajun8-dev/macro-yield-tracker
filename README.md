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

最終更新: 2026年10月27日 05:36 (UTC)

| 指標 | シンボル | 最新値 | 前回値 | 前日比 | 種別 | 注記 |
|---|---|---:|---:|---:|---|---|
| MSCI ACWI | `ACWI` | 157.57 (2026-10-26) | 156.80 | +0.77 (+0.49%) | 価格 | 前回取得日比: 3日 / 前日比: +0.77 (+0.49%) |
| NASDAQ総合 | `^IXIC` | 26,169.38 (2026-10-26) | 25,955.34 | +214 (+0.82%) | 価格 | 前回取得日比: 3日 / 前日比: +214 (+0.82%) |
| NYダウ | `^DJI` | 52,361.58 (2026-10-26) | 52,215.16 | +146.4 (+0.28%) | 価格 | 前回取得日比: 3日 / 前日比: +146.4 (+0.28%) |
| S&P 500 | `^GSPC` | 7,676.77 (2026-10-26) | 7,623.68 | +53.09 (+0.70%) | 価格 | 前回取得日比: 3日 / 前日比: +53.09 (+0.70%) |
| TOPIX | `^TPX` | データなし | — | — | 価格 | この更新ではデータを取得できませんでした |
| TOPIX連動ETF (NEXT FUNDS TOPIX連動型上場投信) | `1306.T` | 420.40 (2026-10-27) | 418.40 | +2 (+0.48%) | 価格 | 前回取得日比: 1日 / 前日比: +2 (+0.48%) |
| VIX指数 | `^VIX` | 18.3900 (2026-10-26) | 19.4500 | -1.06 (-5.45%) | 価格 | 前回取得日比: 3日 / 前日比: -1.06 (-5.45%) |
| ドルインデックス | `DX-Y.NYB` | 102.09 (2026-10-27) | 101.96 | +0.131 (+0.13%) | 価格 | 前回取得日比: 1日 / 前日比: +0.131 (+0.13%) |
| ドル円 (USD/JPY) | `USDJPY=X` | 157.64 (2026-10-27) | 156.83 | +0.81 (+0.52%) | 価格 | 前回取得日比: 1日 / 前日比: +0.81 (+0.52%) |
| 日本国債10年利回り | `MOF:JGB:10Y` | 3.057% (2026-09-30) | 3.082% | -2.5 bp | 利回り | 前回取得日比: 1日 / 前日比: -2.5 bp |
| 日本国債20年利回り | `MOF:JGB:20Y` | 3.877% (2026-09-30) | 3.887% | -1.0 bp | 利回り | 前回取得日比: 1日 / 前日比: -1.0 bp |
| 日本国債2年利回り | `MOF:JGB:2Y` | 1.952% (2026-09-30) | 1.976% | -2.4 bp | 利回り | 前回取得日比: 1日 / 前日比: -2.4 bp |
| 日本国債30年利回り | `MOF:JGB:30Y` | 4.098% (2026-09-30) | 4.126% | -2.8 bp | 利回り | 前回取得日比: 1日 / 前日比: -2.8 bp |
| 日本国債5年利回り | `MOF:JGB:5Y` | 2.399% (2026-09-30) | 2.425% | -2.6 bp | 利回り | 前回取得日比: 1日 / 前日比: -2.6 bp |
| 日経平均株価 | `^N225` | 63,285.04 (2026-10-27) | 62,189.65 | +1095 (+1.76%) | 価格 | 前回取得日比: 1日 / 前日比: +1095 (+1.76%) |
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

生成日時: 2026年10月27日 05:36 (UTC)

### 今日の市場をひとことで
日本市場では、TOPIX連動ETFが2026年10月27日に420.40となり、前営業日（2026年10月26日）から0.48%上昇しました。日経平均株価も同日に63285.04と1.76%の大幅高となりました。これは、米国株がAI関連への期待から反発した流れを引き継いだものと見られます。米国市場では、S&P 500が2026年10月26日に7676.77と0.70%上昇し、NYダウも52361.58と0.28%高となりました。ドル円は157.64円と円安方向に推移し、日米の金利差が意識される動きでした。

チャート全期間（TOPIX連動ETFは2024年10月28日から2026年10月27日、S&P 500は2024年10月28日から2026年10月26日）では、TOPIX連動ETFが約50.84%上昇、S&P 500が約31.82%上昇と、両市場ともに長期的な上昇傾向を示しています。当日の日本株の上昇は、この長期傾向と同じ方向への動きと言えます。ニュースでは、米国のAI企業Anthropicの新規株式公開（IPO）申請が報じられ、これがハイテク株の買い戻しにつながったとされていますが、値動きとの因果は、市場全体のセンチメント改善という範囲で捉える必要があります。総じて、AI関連への期待が市場を押し上げた局面ですが、中東情勢や米中間選挙の動向には引き続き注意が必要です。

### 主な指標の動き
2026年10月27日、TOPIX連動ETFは420.40で取引を終え、前日比2.00ポイント（0.48%）の上昇となりました。日経平均株価は63285.04と、前日比1095.39ポイント（1.76%）の大幅高を記録しました。一方、TOPIX指数はデータが取得できませんでした。

米国市場では、2026年10月26日、S&P 500が7676.77（前日比0.70%高）、NYダウが52361.58（同0.28%高）、NASDAQ総合が26169.38（同0.83%高）と、主要3指数が揃って反発しました。為替市場では、ドル円が157.64円となり、前日比0.81円（0.52%）の円安ドル高に動きました。

金利市場を見ると、日本国債10年利回りは2026年9月30日時点で3.057%と、前日比-0.025%（-2.5ベーシスポイント、bp）の低下となりました。ベーシスポイント（bp）とは、金利の変動幅を示す単位で、1bpは0.01%に相当します。米国10年債利回りは2026年10月26日時点で4.986%と、前日比-0.002%（-0.2bp）とわずかに低下しました。米国の短期金利を示す米13週国債利回りは4.025%で、前日比-0.007%（-0.7bp）の低下です。日米の金利差は依然として大きく、これがドル円の円安傾向を支える要因の一つと考えられます。市場の不確実性を示すVIX指数は2026年10月26日に18.39と、前日比-1.06ポイント（-5.45%）低下し、市場の警戒感がやや和らいだことを示唆しています。

### 国内外のニュースと市場の反応
国内市場では、2026年10月27日の東京市場が反発して始まったことが報じられています。特に、米国のAI企業Anthropicの新規株式公開（IPO）申請を好感し、AI関連や半導体関連株に買いが先行しました。この動きは、前日26日の東京市場で半導体株が売られ、日経平均を押し下げた流れを反転させる形となりました。

海外では、複数の重要なニュースが確認できます。
まず、米国では2026年11月3日に中間選挙が実施されます。連邦下院は民主党が優勢と予測されており、上院の多数派争いも焦点となっています。中間選挙の結果は、トランプ政権の今後の政策運営、特に財政政策やAI規制に影響を与え、米国株や米金利、ドル円相場にも波及する可能性があります。例えば、共和党が上下両院を維持すれば拡張的な財政政策が進みやすく、米長期金利の上昇を通じてドル高・円安が進む可能性が指摘されています。

次に、ロシアとウクライナの間で、ウクライナ南部ヘルソン州オレシュキでの局地的な一時停戦が2026年10月27日午前10時（日本時間）に発効しました。この停戦は、人道支援物資の搬入や住民の避難を目的としており、米国のメラニア・トランプ大統領夫人が仲介しました。ロシア側は、今回の停戦が他の地域での停戦の「前例になり得る」との認識を示しています。このニュースは地政学リスクの緩和に寄与する可能性がありますが、市場全体への直接的な影響は限定的と見られます。

さらに、イスラエルでは2026年10月27日に総選挙が投開票されます。ネタニヤフ首相の続投が最大の争点であり、中東情勢に影響を与える可能性があります。世論調査では与党が劣勢とされていますが、多党制のため連立交渉が難航する可能性も指摘されています。

### オルカン・S&P 500を保有する人向けの見方
MSCI ACWI（全世界株式）は2026年10月26日時点で157.57ドルとなり、直前観測日である2026年10月23日から0.49%上昇しました。チャート全期間（2024年10月28日から2026年10月26日）では、約31.92%の上昇と、堅調な推移を見せています。S&P 500も2026年10月26日に7676.77ドルと、直前観測日である2026年10月23日から0.70%上昇しました。チャート全期間（2024年10月28日から2026年10月26日）では約31.82%の上昇であり、MSCI ACWIとほぼ同等の成長率を示しています。これは、MSCI ACWIに占める米国株の割合が大きいことを反映していると考えられます。

ドル円は157.64円と円安傾向にあり、円ベースで全世界株式や米国株式を保有している投資家にとっては、為替差益が評価額を押し上げる要因となり得ます。また、米国10年債利回りが4.986%と高水準で推移していることは、企業の資金調達コストや将来のキャッシュフローの割引率に影響を与える可能性があります。

長期的な分散投資を志向するオルカンやS&P 500の保有者にとって、短期的な市場の変動は避けられないものです。AI関連のニュースによる市場の反応や地政学的なイベントは、一時的な値動きをもたらすことがありますが、これらは長期的な資産形成の目標とは切り離して考えることが重要です。個別の売買判断や短期的な市場予測に惑わされず、自身の投資目標とリスク許容度に基づいたポートフォリオを維持することが、引き続き推奨されます。

### チャートで見る直近の流れ
TOPIX連動ETFは、直近の数観測（2026年10月21日から27日）では425.60から420.40へと推移し、一時的な下落の後、最新日には反発しました。チャート期間全体（2024年10月28日から2026年10月27日）では、278.70から420.40へと大きく上昇しており、約50.84%のプラス成長です。期間高値は2026年10月6日の440.40、安値は2026年3月31日の37.14であり、現在値は期間高値に比較的近い水準にあります。

S&P 500は、直近の数観測（2026年10月20日から26日）では7712.57から7676.77へと推移し、一時的な下落の後、最新日には反発しました。チャート期間全体（2024年10月28日から2026年10月26日）では、5823.52から7676.77へと上昇しており、約31.82%のプラス成長です。期間高値は2026年10月6日の7818.93、安値は2025年4月8日の4982.77であり、現在値は期間高値に近い位置にあります。

MSCI ACWIは、直近の数観測（2026年10月20日から26日）では158.77から157.57へと推移し、S&P 500と同様に一時的な下落後に反発しました。チャート期間全体（2024年10月28日から2026年10月26日）では、119.44から157.57へと上昇しており、約31.92%のプラス成長です。期間高値は2026年8月13日の162.48、安値は2025年4月8日の103.59であり、こちらも期間高値に近い水準で推移しています。

なお、日本市場のデータは2026年10月27日時点、米国市場およびMSCI ACWIのデータは2026年10月26日時点と、更新日に差があるため、同列での厳密な比較には注意が必要です。

### 参照したニュース・資料
- [livedoor.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGtLHUVebmivNC8Mx7dRwFSqpTcOuaFTqMMN4G2UgWuNLycFW-vhrPEm1Nf9q3AnX1iu6_fymf-qAhMPHBsRpV5bDNuCMpeUDY_IiReNBfN_H2R3WSa9ObC-RC_kfaB7JH5_AQP1ZgrH_FcVA==)
- [kabutan.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGUC4wvpHylxA8f9aWynoJRlrKG29UitDbuiOAfThiB96Q_zpGhDyg-Km6go_hDbA5T1v8Oe6cZTPlC2h_fU_Tb1YWfT-jvYmtVRQ9tRjUcliWjlDoZ7TEzuOBsHplgsZw_Ir7HrJKw0e2n-1zz)
- [kabutan.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGAnripHMjSUM5wkY-PfOusIbQ99M0RgRjCmqVngZ6nK25EjNxMK7oIsM_oxW7-MVyUuyJGZ5ein9CIoxy8SAc6UT6w6Co37k9FOkl_cbDiHz-ZULeyij3b-65hKSgHo0oWXA2s1j4tWnpwJt7e)
- [note.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFfHY-Kf9umzQ-sUyWYTbBr9OJvie3tbp70MiuyIyZGyOuTjmbqXsxVkwmRNHukIiPynYsfLbifLP6-Am7xDvvL55YVxKtCe95wCa0_QiMmJY_jpniJJRLhoFS6viysCvOdV512MbJW)
- [note.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGF2DIRQheros3Qs7WtK7tN8t8cdLdlWtjLWaUlHRtP4L5crO3htxTOs7yz7NKo-An-D9TFsDTRsyJg3QEFp5LSeiBEi-EOhvd3vXwwTy21dY2wLvgITDC9ANggsIFVCgbkZFZd9FQH)
- [rakuten-sec.net](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG_JdKaabK6AAttPJEVmAD8fa1Mqj_QxGV61N3LUKbmpaxzsWlPtS7aCYoIimXVL_GgJ7IuUrK8VzQppZP3MhCfyI7cCcuZknW1_I7rFjrx3TlCBt29qMKnkvyJEnp4pPYzz00f9tl4Rg==)
- [gaitame.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGWTJbLzEGG6kghNTw-A2fp5ub0bGsFycB7bQVbVY90PLrMKLNrayvhi_6FOsiSQCRehJgA0t7cOW1R1m2anCiqbOJrpf2A-hyyDo88cqvrsPlYMkHfoKTGZsLW7TGxsGnKMTSNQiLaglFP889tR3Y=)
- [dlri.co.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGdCR4ewViWnVCKrv4LER7ogHgSMli-wGp9fpIdXqYD6t6EPsvUizX4h4jNEVGWCC7CfKkhxqrcDsDd7gBTnYvlYca2d6-Kx-4YAk_weLMpMC90WmjueHuYn6CaRU0t3oJHQe_nFFCGesY=)
- [jetro.go.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFIU99ux322l8BQU_Matq6KMx2JGNdtS8iDWwX7GKbA3tHiwS5AFwODFQLakTUdW-GxUASo_UpBJlMS0HDOGP-86m9b1Ncg6_PTF3Vt0L2Bx_J7vbCIZKbMfLFRn_7Tn80j4eY60Cfb9sTLERbalimMHdlgqJGirQ==)
- [fnn.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG5i-1MIsNF3ujOfwCKba9pkcicRxs6Ua7yVLJnA-1uoPGtqmkA9jLSF06padjCnwSp7LAopQF0SyHMLGpNj45f2HnDM-v0wnRKH4JLBLEDK8Wmeu2bPU9yp35xXRqiPg==)
- [gate.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHuZuk0FF244CSO45JG3NZt1JpjmwWD35iGuLKB3pKouI5M1GQYlx0mQKLCRuvAU3d7OjSM0wt135RA4hDzBqCgKZ_WFKsPdb5lI7VR9VMBwEN_au5C3g0qgqLgk5CFmKFCK0M8WM13Bomf0HckBTJvv3bHSMsyZVrxtbQUa312TVyDYhwsjQ6qa7Prydn92mLBpbET3zu6eGLcvykDiD4BOdYrvKpPX9tv)
- [ukrinform.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGP226a9mYIyvb90IxqxTjUg7PdNAfGJKhMD7NoR2dy535G3jQwMEi9yQ5-fbyQVkTdBSFQomqV2o1olqsUo2y6J4iTDR0JEcxLfv714mDfcoBxdqtTQ5qrjVTAyFx89wF6VfESV_Ea9hca1mjsjH23-RX2L-Ym7id-YIdQDi14suGNVJRnC6dZ1rzd7rVuTXjmUYdbq2I6i8tPMLnePsn5DbJY-95sjlhqPIlAW9PQbvmxPE1jhs8L)
- [youtube.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHQDKnGV8HEFa65qsXu0f2ag9J8UavcAbK0K3zqGw-OEeQofTTUDd7Ro4M5qRw8J4fvcIxLHBvgEzm6nNPbvKMBpJjEc-D6T7OHOqBoubBv6nO80xTyAXG8l5mv-8MiFFPzHg==)
- [mainichi.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGSLPppDHfej-YwPX82WA3-PgQ07qGrAKtrsSFhEa2YxlihfzVVG4lgBN7U_s6WtsitWta82Oz_YMtkwEInvLiytGxNWbuMIwd2heiXm-pfCP6Q-2rFo3XAWpmLRoZgokunc5LRQd4iMFcdg3cjTysxMY_D)
- [novaist.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFSnPzHhC_6CHd4UAar-fcZONfCn5hs9ujNQEG34tNZIc-4u6pyC0JnsZ2PwHkyVOOspXMcFTbjHGqxBV2pUiFmpRG-RXLpHxnKvZtwvE5P7Owea7EqY70F7fb537hCVZ14tKNLHSv-4_lzMH_6SjUtMpj5)
- [fnn.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFyYb_-QE62Lcv0YaKOR4-w8Y1SZ-yCe4ND9bGHXZbnit-_k3vaGdlfd_h4vHjpDdhqK4-BpNOgnfNrvQTk7N9EGqwdMyGg2kY8tixeJPYXZf_0yE9zqq2IEqySDae4XQ==)
- [dlri.co.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEYGFE61EOkEMXeLEuiM8E_DyWzF-EIdtCZ_IAOkJlZYpEVNpOY7kRtwraOa_OHeG1noGBuLcWH7diVmnNVVCW7VOquxLr79O-wAc9Leywk6EID18NhRxFuA1eANW4f-6malVLVxNeOLbI=)
- [note.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFFec0wVmbXNM9bW_04Dm1ddICfat2-3cnInHXiY1sEm_K5LNLJeVyzWMvw5MKFo0hJfXCYH7HMa9pgB40P_k6VBy6_QnRouHJ_N5_4Ewm5c84RxN1N5k5YSPGoxUnLaIzrNtcwpye-)

※公開情報をもとにした一般的な解説です。特定の個人への投資助言ではありません。
<!-- AI-DAILY-REPORT:END -->
