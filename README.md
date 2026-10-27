# macro-yield-tracker
財務省の国債利回り曲線や日米の金利、全世界株式などのマクロ指標を観測します。

## 実行

```bash
python -m pip install -r requirements.txt
python -m src.main
```

実行すると `output/market_dashboard.xlsx` と `output/charts/` を生成し、このファイル内の市場ダッシュボードを更新します。GitHub Actionsの `Update market dashboard` ワークフローが、平日18:00（日本時間）に自動更新します。手動実行はGitHubリポジトリの「Actions」から同ワークフローを開き、「Run workflow」を選択してください。
日本市場では、2026年10月27日の日経平均株価が前営業日比1.757%高の63282.179688円となり、TOPIX連動ETFも0.478%上昇しました。これは、前日の米国株式市場でAI関連への巨額投資を巡る懸念が和らぎ、株価が上昇した流れを引き継いだものと見られます。ドル円は157円台半ばで推移し、ドルインデックスも小幅に上昇しました。チャート全期間では、日経平均株価が2024年10月28日から2026年10月27日までに63.92%上昇しており、当日の変化は長期傾向と同じ方向です。ニュースでは、ロシアとウクライナの局地停戦合意が報じられていますが、これが直接的な市場の値動きに与える影響は限定的と捉える必要があります。総じて、AI関連株への安心感からリスクオンの動きが見られた局面ですが、米国の経済指標や金融政策の動向には引き続き注意が必要です。

関連ニュースを自動で取り込みたい場合は、`NEWS_API_KEY` を同じくGitHub Secretsに追加してください。未設定時でも、RSSのフォールバックで国内・海外の見出しを拾おうと試みます。キーがない場合は、ニュースを使わずに市場データだけで解説します。

<!-- MARKET-DASHBOARD:START -->
## 市場ダッシュボード

最終更新: 2026年10月27日 14:42 (JST)

| 指標 | シンボル | 最新値 | 前回値 | 前日比 | 種別 | 注記 |
|---|---|---:|---:|---:|---|---|
| MSCI ACWI | `ACWI` | 157.57 (2026-10-26) | 156.80 | +0.77 (+0.49%) | 価格 | 前回取得日比: 3日 / 前日比: +0.77 (+0.49%) |
| NASDAQ総合 | `^IXIC` | 26,169.38 (2026-10-26) | 25,955.34 | +214 (+0.82%) | 価格 | 前回取得日比: 3日 / 前日比: +214 (+0.82%) |
| NYダウ | `^DJI` | 52,361.58 (2026-10-26) | 52,215.16 | +146.4 (+0.28%) | 価格 | 前回取得日比: 3日 / 前日比: +146.4 (+0.28%) |
| S&P 500 | `^GSPC` | 7,676.77 (2026-10-26) | 7,623.68 | +53.09 (+0.70%) | 価格 | 前回取得日比: 3日 / 前日比: +53.09 (+0.70%) |
| TOPIX | `^TPX` | データなし | — | — | 価格 | この更新ではデータを取得できませんでした |
| TOPIX連動ETF (NEXT FUNDS TOPIX連動型上場投信) | `1306.T` | 420.40 (2026-10-27) | 418.40 | +2 (+0.48%) | 価格 | 前回取得日比: 1日 / 前日比: +2 (+0.48%) |
| VIX指数 | `^VIX` | 18.3900 (2026-10-26) | 19.4500 | -1.06 (-5.45%) | 価格 | 前回取得日比: 3日 / 前日比: -1.06 (-5.45%) |
| ドルインデックス | `DX-Y.NYB` | 102.10 (2026-10-27) | 101.96 | +0.14 (+0.14%) | 価格 | 前回取得日比: 1日 / 前日比: +0.14 (+0.14%) |
| ドル円 (USD/JPY) | `USDJPY=X` | 157.65 (2026-10-27) | 156.83 | +0.821 (+0.52%) | 価格 | 前回取得日比: 1日 / 前日比: +0.821 (+0.52%) |
| 日本国債10年利回り | `MOF:JGB:10Y` | 3.057% (2026-09-30) | 3.082% | -2.5 bp | 利回り | 前回取得日比: 1日 / 前日比: -2.5 bp |
| 日本国債20年利回り | `MOF:JGB:20Y` | 3.877% (2026-09-30) | 3.887% | -1.0 bp | 利回り | 前回取得日比: 1日 / 前日比: -1.0 bp |
| 日本国債2年利回り | `MOF:JGB:2Y` | 1.952% (2026-09-30) | 1.976% | -2.4 bp | 利回り | 前回取得日比: 1日 / 前日比: -2.4 bp |
| 日本国債30年利回り | `MOF:JGB:30Y` | 4.098% (2026-09-30) | 4.126% | -2.8 bp | 利回り | 前回取得日比: 1日 / 前日比: -2.8 bp |
| 日本国債5年利回り | `MOF:JGB:5Y` | 2.399% (2026-09-30) | 2.425% | -2.6 bp | 利回り | 前回取得日比: 1日 / 前日比: -2.6 bp |
| 日経平均株価 | `^N225` | 63,282.18 (2026-10-27) | 62,189.65 | +1093 (+1.76%) | 価格 | 前回取得日比: 1日 / 前日比: +1093 (+1.76%) |
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

生成日時: 2026年10月27日 14:42 (JST)

日本市場では、2026年10月27日の日経平均株価が前営業日比1.757%高の63282.179688円となり、TOPIX連動ETFも0.478%上昇しました。これは、前日の米国株式市場でAI関連への巨額投資を巡る懸念が和らぎ、株価が上昇した流れを引き継いだものと見られます。ドル円は157円台半ばで推移し、ドルインデックスも小幅に上昇しました。チャート全期間では、日経平均株価が2024年10月28日から2026年10月27日までに63.92%上昇しており、当日の変化は長期傾向と同じ方向です。ニュースでは、ロシアとウクライナの局地停戦合意が報じられていますが、これが直接的な市場の値動きに与える影響は限定的と捉える必要があります。総じて、AI関連株への安心感からリスクオンの動きが見られた局面ですが、米国の経済指標や金融政策の動向には引き続き注意が必要です。
### 主な指標の動き
2026年10月27日、日経平均株価は63282.179688円で、前営業日（2026年10月26日）から1092.53125円（1.757%）の大幅な上昇となりました。TOPIX連動ETF（1306.T）は420.399994円で、前営業日（2026年10月26日）から2.0円（0.478%）上昇しました。TOPIX指数そのもののデータは取得できませんでした。

米国市場では、2026年10月26日のS&P 500が7676.77002ポイントで、前回の観測日（2026年10月23日）から53.089844ポイント（0.696%）上昇しました。NYダウは52361.578125ドルで、前回の観測日（2026年10月23日）から146.417969ドル（0.28%）上昇、NASDAQ総合は26169.380859ポイントで、前回の観測日（2026年10月23日）から214.041016ポイント（0.825%）上昇しました。

為替市場では、ドル円（USD/JPY）が2026年10月27日に157.651001円となり、前営業日（2026年10月26日）から0.820999円（0.523%）のドル高円安に推移しました。ドルインデックスは102.099998で、前営業日（2026年10月26日）から0.139999ポイント（0.137%）上昇しています。

金利市場では、日本国債10年利回りが2026年9月30日時点で3.057%と、前回の観測日（2026年9月29日）から-0.025%（-2.5ベーシスポイント、bp）低下しました。ベーシスポイント（bp）とは、金利の変動幅を示す単位で、1bpは0.01%に相当します。他の日本国債利回り（2年、5年、20年、30年）も同様に2026年9月30日時点のデータであり、前回の観測日（2026年9月29日）からそれぞれ-2.4bp、-2.6bp、-1.0bp、-2.8bp低下しています。米国10年債利回りは2026年10月26日時点で4.986%と、前回の観測日（2026年10月23日）から-0.002%（-0.2bp）低下しました。米13週国債利回りも2026年10月26日時点で4.025%と、前回の観測日（2026年10月23日）から-0.007%（-0.7bp）低下しています。

市場の不確実性を示すVIX指数は、2026年10月26日に18.389999ポイントとなり、前回の観測日（2026年10月23日）から-1.060001ポイント（-5.45%）低下しました。VIX指数は「恐怖指数」とも呼ばれ、数値が高いほど市場の不安心理が強いことを示します。

株式市場では、前日の米国株高が東京市場に波及し、特にAI・半導体関連株が買われる展開となりました。ドル円は米金利の失速により伸び悩む場面も見られましたが、全体としては堅調に推移しています。日本国債利回りは9月末のデータであり、最新の市場動向とは異なる可能性がある点に留意が必要です。

### 国内外のニュースと市場の反応
国内では、2026年10月27日の東京株式市場で日経平均株価が一時1400円を超える大幅な上昇を見せました。これは、前日の米国株式市場でAI関連への巨額投資を巡る懸念が和らぎ、株価が上昇した流れを引き継いだためと報じられています。特に、AI開発企業アンソロピックが株式上場に向けた目論見書を公表し、予定通りに進む見通しとなったことで、市場に安心感が広がったことが背景にあるとされています。東京市場では、これまで売られていたAI・半導体銘柄が買い戻される動きが顕著でした。

海外では、ロシアとウクライナが、ロシアが占領するウクライナ南部ヘルソン州オレシュキ市において人道支援活動を促進するための一時停戦に合意し、日本時間27日午前10時に発効したと報じられています。この停戦は、米国ファーストレディのメラニア・トランプ氏の仲介で調整されたとされています。また、米中間選挙が11月3日に実施される予定であり、トランプ政権の政策運営や米国株、米金利、ドル円相場への影響が注目されています。特に、下院では民主党が優勢との見方が強まっており、共和党は豊富な資金を投じて巻き返しを図っている状況です。

これらのニュースと市場データとの関係としては、AI関連株への安心感が日米の株式市場を押し上げた主要因と考えられます。一方で、ロシア・ウクライナの停戦合意は地政学リスクの一時的な緩和要因となり得るものの、市場全体への直接的な影響は限定的と見られます。米中間選挙の動向は、今後の米国の財政政策や金利動向を通じて、為替や株式市場に中長期的な影響を与える可能性があります。

### オルカン・S&P 500を保有する人向けの見方
MSCI ACWI（全世界株式）は2026年10月26日時点で157.570007ドル、S&P 500は同日時点で7676.77002ポイントでした。MSCI ACWIは2024年10月28日の119.440002ドルから2026年10月26日までに31.924%上昇しており、S&P 500も同期間に5823.52002ポイントから31.824%上昇しています。両指数ともに長期的に堅調な上昇トレンドを示しており、世界株と米国株の重なりや違いを理解することは重要です。S&P 500は米国の大手500社の株価指数であり、MSCI ACWIは先進国と新興国の大型・中型株を網羅する世界的な指数です。米国株は世界株の中でも大きな比重を占めるため、両者の値動きには強い相関が見られます。

為替のドル円は157円台半ばで推移しており、日本円ベースでの資産評価に影響を与えます。円安は海外資産を円換算した際の評価額を押し上げる要因となります。また、日米の金利差も重要です。米国10年債利回りが4.986%であるのに対し、日本国債10年利回りは3.057%（9月末時点）と、依然として金利差は開いています。金利は企業の資金調達コストや将来のキャッシュフローの割引率に影響するため、株式の評価にも間接的に影響し得ます。

短期的な市場の変動は避けられないものですが、オルカンやS&P 500のような広範な指数への長期分散投資は、個別の企業や国のリスクを軽減し、世界経済の成長を取り込むことを目指すものです。日々の値動きに一喜一憂せず、自身の投資目標とリスク許容度に基づいた長期的な視点を維持することが重要です。個別の売買判断や資産配分については、ご自身の判断で行う必要があります。

### チャートで見る直近の流れ
TOPIX連動ETFの直近の数観測では、2026年10月21日の425.600006円から10月23日には416.299988円まで下落した後、10月27日には420.399994円へと反発しています。チャート期間（2024年10月28日から2026年10月27日）では、最初の観測値278.700012円から最新値420.399994円へと50.843%上昇しており、長期的な上昇トレンドにあります。期間高値は2026年10月6日の440.399994円、安値は2026年3月31日の37.139999円であり、現在値は期間高値に近い水準で推移しています。

MSCI ACWIの直近の数観測では、2026年10月20日の158.770004ドルから10月23日には156.800003ドルまで下落した後、10月26日には157.570007ドルへと反発しました。チャート期間（2024年10月28日から2026年10月26日）では、最初の観測値119.440002ドルから最新値157.570007ドルへと31.924%上昇しており、こちらも長期的な上昇トレンドです。期間高値は2026年8月13日の162.479996ドル、安値は2025年4月8日の103.589996ドルであり、現在値は期間高値からやや下落した位置にあります。

ドル円の直近の数観測では、2026年10月21日の158.268005円から10月23日には156.494003円まで下落した後、10月27日には157.651001円へと反発しています。チャート期間（2024年10月28日から2026年10月27日）では、最初の観測値152.951996円から最新値157.651001円へと3.072%上昇しており、緩やかな円安トレンドが続いています。期間高値は2026年7月29日の163.863998円、安値は2025年4月22日の140.876007円であり、現在値は期間高値よりは低いものの、中程度の水準に位置しています。

日本国債利回りのデータは2026年9月30日までのものであり、最新の株式や為替のデータとは更新日が異なるため、同列に比較する際にはその時間差を考慮する必要があります。直近の数観測では、日本国債10年利回りは2026年9月28日の3.082%から9月30日には3.057%へと低下しています。チャート期間（2024年10月28日から2026年9月30日）では、最初の観測値0.981%から最新値3.057%へと207.6bp上昇しており、長期的に金利上昇トレンドが続いています。期間高値は2026年9月28日の3.082%、安値は2024年11月5日の0.944%であり、現在値は期間高値に近い水準です。

米国市場（S&P 500, NYダウ, NASDAQ総合, MSCI ACWI, 米国債利回り, VIX指数）の最新データは2026年10月26日時点であり、日本市場（日経平均株価, TOPIX連動ETF, ドル円, ドルインデックス）の2026年10月27日時点のデータとは更新日に1日の差があります。このため、日本市場の当日の動きは、前日の米国市場の動向を織り込んでいる可能性があります。

### 参照したニュース・資料
- [livedoor.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEEYhmnHBQtZeY10WMpOJc5FgpGA-QyeBnqDlPxeryu1yHDdek6sA-dzC0lDVngxl3K2J2Or2fzwJnKWJbPm5DWZHsjdVeRezBa5t67wIgQSOuvSA2hvAyo6Xs5EwcOAjAg65TJXwvGJZvkNu4=)
- [kabutan.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHiGJFFIf6R4UWFjlkw7Vsp2U6B5v2Vsgk-kowmbUbc5cUKnDb2lJUGb_eFKxGTCCFjaHYai3Z7IcFc9oSmUGGAz665FWpm6U9RVNULEBK7YZXgJUIBOyQGu2Y6xTLeBzEhn75HhKEmflIgaJpNQg==)
- [kabutan.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGRAozJD7agLj2Oz3nIRb02QdhJ9Fm2qOH6yW7wskX5AqQTEbCOajnsyTBkPHcvE5mk8G8zA1BRNkgIyhvAoSmrTqGXk9UzpZLIjcdkNHPeZnmWk-qQKNaiuiZYRjxD2v73V2Q=)
- [chiba-tv.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEJkrWlx7VWXUmBR8WtRoqI4LRPqOmIHgRj6gCs4zpIR9vpHX-pBqAmpw3sICwDuh2TH_zVecBEkLyPdyJEkTqyUZ9HqsgG9nULP--FyyRy_m_NHLGkbVtx6p8WH6-3DHBBQv4zm3uvmp_g2nhp)
- [oanda.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFYI--hMwFrZTvf3WM-pwPcOkLOdhc7oaFrTb3tSn72_X1ib45fii2JqRH5O9EKlnFerMVCoTrskv2Wh40kTk5bKgxg4STISbGHNYgUFiqADXuYSzENgfvx6YHXfitUVDzRJWo6F2rRQUZCv3T7Fh_xYbvvIeeTNq-_L1thVO5hMZZA)
- [kabutan.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHL6R6fv5aPnABO0SQ1sB2wZQE-DAB1VOEvGl_Zz2JBed7CT42VJGScr88PmsovFSTcDqGT1AxcKSX6NdZKcAvCVdlHOzTheNagvMosLRrFT5Hk7pqP2NK1EFDaibRDigCRjFx0z3wxj2qVyiOOAQ==)
- [kab.co.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEbG2mtS2jaeWlKbg3b0RF1EQR-gt7QWn03ClKVNO_rrFbZHdLdyh1PfwbdPk3aEqgNA0fvFW5lHNTq8Yu2PUjy3nDpiza7bHEUAr0lifQbpa62yNQz8m0LWNqvsq8vnRxM43693IY=)
- [oanda.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFkhcRohvLXEmg82LU6zxIs74KslOyiB_JtpSe3nwmj5BwjMOEBRMlvNIYvyCG817w_OuN2iBu4FpRWxebc3Pw5xIgifAYqgbdhquYvgMytYZvR2xse5u7QQQt1z4Q2hyxn_vrfEpBQnKnPpM-3nVgKsqwVpxCMxmFDddg=)
- [kabutan.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQES_0_W-WaLycV7czsqwTEYzO6PXHG-sAkM9bkKuFEN4BW9E5zjx4OF_rD38t21NGfEtafpzUePcmn6_qF2OrkhHUyhys9ce5gQtbmBBpQ0cTJKt6idVQ9c9NV_mxtp-k3NuILk6vIW0pQpKJy_TQ==)
- [investing.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEEOPTqOUMTQRwv8SxQwFjirqdG504DtT_ItFAHmYd6PjzxyJSPqSiQrGhDyzRrQcpJicZiJWL-aYXlMplfpewZzJYR1TeQH5l_naP7ZFrlSVud55bo7dSVkgGHWMlV8BHrIlVMdl_KLkwZKRtTWmuEfWqo)
- [zaikei.co.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFmNJNT9zIMsYUlkas789AKKnTiaZoJSUYPf__g_lA1JRihZNUBiKFE6m7_-39iYRbvnB_g8UO6Y_ADmKkgHVq9v_8EjhdD0CI_W-CbkKF4lEmVfY-YfR6aPnbdIGhBdPV6w0evhOPuSgwesTVa6fpc)
- [note.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFfT9j7TCwNV3SfIhRi0_zqCA_i1J5f90KjbhLwyRpk3e5NwzsqiLx_CGvyFN-UrhQ8qYJ_d8doHbtTWZWTBy_Ehm9laom3syTUKWXk8a6mREiSZFqMA6hfe69C3Voa29okKnuULPcfwg==)
- [kabutan.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHqeCwsJ-30JdZX9H0m2YA8rYIY7pTHo2hmIfu_A-RpB5xhCCN_RjEI5wJF8Dg42BiSo_-Wt0rmGnsfc7pAV3b4gX9yYW3vN4awnzpPVo6Q8ufqpzxhO6smbV40fb4zUOEX7TCQu0JicQBjBftHVA==)
- [yahoo.co.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQECztZSpGegZLe9YjrolrhNQYBCcQMCdLbuvMgp2lN4YIYJFWrknVdE2vJHga77jt3ZY_rvqSjTIwVjylELxjtMe6L8pZxVM3SfkuDqy3T3wqVmG3AnFiKSNxBXmxlaDie7h9qJbhUhLRfs8Dwgmog1VgBUwJbh6gHji1pUUFYfwps9A0ct2BqVBBPT)
- [minkabu.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEtyqhkIrlmEo5NTYiPOZJYuUGgCiKMe0gzRTSbVUrBvjTFe1WK0FzSCR4S6fOk-zD_VoxfYA2o0obmi3kIA7pgSLsDEn_fYZ7mwFu2eZiTdfsiaFGKTd_TnoYgRQ==)
- [kabutan.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHCGDW9UNIZ2kEmimyU1wL9BJIme9uuQ92NZO709DLH1kEixexlh_-EgEVNDqaPF7aWux7jwJenELMGsklrvjAdGDFMFa3M1DJ9TJ8NbH7H_kLyDWHaDBMnAoWJm9fc2q4EmLA=)
- [oanda.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF9XdW8DGtnR-ey0sBk7nICdJW4SNKg1pnJqJB4k8Ast81iyqATH6bhlaIZXeHlT3SkP9J0nDuoYU0Wkk5hgmG41tsTOokaDH5C4YNonSeJjBOTC7dWEVh33T4VATtNo1n4qYEfzxd-CpyKDB6nADN-TCjSkF2ACCWm5zo2fxizAgyo)
- [gaitame.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG9cW5bNHPxEbdeuYSQ5Jp6Qsc1gwtfVobl53TKajThGBREuelRIKju-Cii0E2Mpi8Vn2HVOWH5HtvQwSVrjE4m9UpVV_EobVAAEcvPcnUEwY5JFOjq-RTs2earRkRFA5yPPR1C6yKR3fyZ535v1jMS)
- [oanda.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFirdToF3BXAdKRNqhhPDMQKj1boNYAFEVLva8HYj1SZDIQvM-Ii3y1Gmc2zQE3JKzddOQLwF_Y2-NQ6Isx7wEvYi0UPOPaj5zD2Rk8w22SJeZfshHDKiDhQD4As5au01AuKCqUX8WSPZY7gchufpxl1gA6CUt4TAIy7XTn)
- [fnn.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHpFOoY1CvC_GwNmBL7xCepcdqNlV_G6YOih-DVgrlLOh5aFiMDmdNa8IZ5UWhmWZIMcEuPj7_y4n5TqOR9nr1M0Ni4b5vWMdkxkPEewMkYnWmNHVAdiZwRlgtvHjgOXM8=)
- [livedoor.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHnDt3zkS-IYUINCMyVoMxAbntCW3eUG9G1xgjULHAV4GDjiry7JsPYuU2nuwOnBlGeKSHKofSVO1SSDA960NxHgXzUdEbqTabxLU9YGczsDzW3LQkAArtQ4xGooXX0iTwcVrMcs3JPNi47Jn4=)
- [investing.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFQNh0BLA8VRFcLUJB_D_p2sLlR9-JLNEwi1kiRViTrDH46us4KaZduOFjPOqUAWg0_oSCfwn7onnMuIwbpaDl5y3WLVcmOM-tpncVKM4OKOSzL5PDSgh2lQ8sNTiGyQKdSxmawTxG0res9ASitZj-F8OSfHTM=)
- [laodong.vn](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGLQc6IENb6G2raywXqQbAKkVGunSikJcPfdI8Z4gkhUnWUDQCb1P5d66nT2vMgxWhHDbAdrvJV0ZO97kRFLN3eyeuBnCxitlMK9DEay4n7yKXpb9u0FpIC5K1lqFuHLHmb-fvfXoPcPvJ1V5kgsr3BjJwVVs3SW_JZY_GwyUhCqXZf4jeEq1zLckm2FP1Rseoh2_FSFmHybkwQ9u1CzXFqAUwyyfSI6ThCftxXy12iBvhLGXq6T1vxUsBHOKg=)
- [ukrinform.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHewVR86LnzC7dBuqHDu2qK0T9ZBrlNZl521rRoew2y9KVJyKp5uRo4AMjorDM8SPvROJcTFLsnz2kFkl_HENn2xLosa9UnNK8JNXCoafcMV5u4ObtzmBhBYCSICn5tk3_unbaReXhR3RJEwFq00DTphZPvo5x4B2VhxBU5jir8uYCr3wzY9gO3S6gf6jjkEscD-bQWnbZrOnS9vBT9mWPuh9GjitwJzAmNLsVP3T8uVJ5ZkNjIRxtwPA==)
- [minkabu.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEf58N_tTfnxgt1UrHsr-ugCkCkOBZ5MOBHQtYHTTY_wEkObvvew_U5eK2IZPA_D10v84A_pcjiJk24qB5YF88Nr2ijB5XFVQHcoQKfCAUTIEbyLsSCBv1ukgyuMw==)
- [gaitame.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF_4IOnzg7aMhJlTcDmw_W8wyGy4qPmDt9tU3f2nVlN7zgwA-wnVocaKJLftD_wocObWpsfwxIyWKVhZkXaCznLGc8u1aSZhf_QUARmDAJD7Ly5fiylTf80TfurmH_7bsm2vu6x6WTpieYdw4ZcHBuK)
- [seikyoonline.com](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFSRvY9cmFcCEzkqEIHQ-4O-L5gSWfZLLzJnx2DOdPeWVhsaULY3bazzGVBPOua2tIE5kU9SKSJNkDVHN2_Doccwq6n2EPtIyhoyatte76EeXBRBWeSqut5GaQ6KWfzcTItnqlc964Y-yHJyD_er1xMpgLv2AuepQHRF16UYl1KeA==)
- [mainichi.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH9HIxUgExZYxrP8BJGI5ovy5lXwxwLBzT-A52omYeJmpeQ3WKQYg4VGuimLe6x4kCJ1BY7YkoeFsNJCUXL3RZZacJr_96UZUcOHQo2sZSH4R0w0OXnrTLDDGhenmRes6jbOsMxo_R4ordtn9x9NAVHfWEUkQ==)
- [mainichi.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGg99z50lq-wFgZPrE5B1OmUysR0nIfPZ4M5wn3gT3x4q1pQg31QBC4uXaEWADHbImOrqUtm_JSod0Ajp76gtblCQMBy0-R-HlCGSr2DtsS6F-nRxkedZUuSu3Evoyhz7jNOY9W-AgBR7isaToCay9meFsQRQ==)
- [dlri.co.jp](https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGhDMcLd3v5itpJjHm9MGvgsBuNXcAzCfIM_-TfQH4_D6QCfe7y7rBbSPE1kU7ELXVvr0Bx0PN_n8hQbyD-E44Rn0AuFoChkXqys-VnNuixA5i4vQ6v2A9k5LQJuhD77t-L5iisB2bbfSQC)

※公開情報をもとにした一般的な解説です。特定の個人への投資助言ではありません。
<!-- AI-DAILY-REPORT:END -->
