# Wikimedia Commons Photo Challenge Tally Tool

這是一個專為維基共享資源（Wikimedia Commons）每月照片挑戰設計的自動化計票工具，旨在精確解析 MediaWiki 語法並根據社群規則計算得分與排名。

## 1. 挑戰資訊：工廠內部 (Factory interiors)
* [cite_start]**投票截止時間：** 2026 年 1 月 31 日 UTC 午夜 [cite: 1]。
* [cite_start]**挑戰主題：** Factory interiors [cite: 1]。
* **原始資料來源：** `2025-12-Factory Interior.mw`。

## 2. 統計邏輯與規則

### 評分機制
* **得分 (Score)：** $3*/2*/1*$ 票數之加權總和（權重分別為 3, 2, 1 分）。
* **支持度 (Support)：** $3*/2*/1*$ 票數與 $0*$ 高度推薦票的總計數。
* **排名判定：** 優先比較 **Score**，若分數相同則以 **Support** 進行 Tie-break。

### 投票資格過濾
1.  **基本門檻：** 註冊滿 10 天且編輯數超過 50 次，或該次挑戰的參賽者。
2.  **誠實原則：** 禁止投給自己的作品。
3.  **格式修正：** 同一投票者若對多張照片投下重複的 1/2/3 名等級，除第一筆外皆自動轉換為 0 分（高度推薦）。

## 3. 現有資料統計結果

依據原始 wikitext 解析之最終排名如下：

* Number of contributors: 65 (Constraint: Author data missing)
* Number of voters:       17
* Number of images:       65

The Score is the sum of the 3*/2*/1* votes. The Support is the count of 3*/2*/1* votes and 0* likes. In the event of a tie vote, the support decides the rank.

| Image | Author | Rank | Score | Support |
| :--- | :--- | :--- | :--- | :--- |
| `[[File:Metallurgical Furnace in Guwahati, Assam.jpg|120px]]` | Unknown | 1 | 20 | 10 |
| `[[File:Augsburg Wasserwerk.jpg|120px]]` | Unknown | 2 | 9 | 9 |
| `[[File:Vie12-292 Seidenfabrik.jpg|120px]]` | Unknown | 3 | 8 | 7 |
| `[[File:Briquette press 1006-0229.jpg|120px]]` | Unknown | 4 | 7 | 7 |
| `[[File:Fabriek ZW.jpg|120px]]` | Unknown | 5 | 7 | 4 |
| `[[File:Rr11-087 Kokerei-Hansa.jpg|120px]]` | Unknown | 6 | 6 | 4 |
| `[[File:Huta Pokój walcownia 2019 (3).jpg|120px]]` | Unknown | 7 | 5 | 4 |
| `[[File:Huta Pokój walcownia 2019 (2).jpg|120px]]` | Unknown | 8 | 4 | 6 |
| `[[File:Museum Industriekultur.jpg|120px]]` | Unknown | 9 | 4 | 4 |
| `[[File:Glückauf-Brauerei in Gersdorf, Sachsen 2H1A0139WI.jpg|120px]]` | Unknown | 10 | 3 | 3 |
| `[[File:16-136 Zigarrenfabrik-Kuba.jpg|120px]]` | Unknown | 10 | 3 | 3 |
| `[[File:Blast furnace 2204-0092.jpg|120px]]` | Unknown | 12 | 3 | 2 |
| `[[File:Affoltern-Emmental-Dairy.jpg|120px]]` | Unknown | 13 | 2 | 6 |
| `[[File:Control room pumped storage plant 1909-1420.jpg|120px]]` | Unknown | 14 | 2 | 2 |
| `[[File:Sharpener in the forge.jpg|120px]]` | Unknown | 14 | 2 | 2 |
| `[[File:T23-029 Derix.jpg|120px]]` | Unknown | 14 | 2 | 2 |
| `[[File:Factory interiors 002 2005 10 13.jpg|120px]]` | Unknown | 17 | 2 | 1 |
| `[[File:Hergiswil-Glass-Factory.2.jpg|120px]]` | Unknown | 17 | 2 | 1 |
| `[[File:Schakelruimte.jpg|120px]]` | Unknown | 19 | 1 | 4 |
| `[[File:Diatomite factory Skåne Sweden.jpg|120px]]` | Unknown | 20 | 1 | 2 |
| `[[File:Steam engine in Boxberg.jpg|120px]]` | Unknown | 21 | 1 | 1 |
| `[[File:Склад.jpg|120px]]` | Unknown | 21 | 1 | 1 |
| `[[File:Huta Pokój walcownia 2019 (4).jpg|120px]]` | Unknown | 23 | 0 | 4 |
| `[[File:Factory interiors 001 2005 10 13.jpg|120px]]` | Unknown | 24 | 0 | 3 |
| `[[File:La fosse Arenberg de la Compagnie des mines d'Anzin.jpg|120px]]` | Unknown | 24 | 0 | 3 |
| `[[File:Bamberg Wasserwerk Pumpen-20180317-RM-154208.jpg|120px]]` | Unknown | 26 | 0 | 2 |
| `[[File:Brauerei Ulm 03.jpg|120px]]` | Unknown | 26 | 0 | 2 |
| `[[File:Factory interiors 004 2008 04 18.jpg|120px]]` | Unknown | 26 | 0 | 2 |
| `[[File:Hergiswil-Glass-Factory.1.jpg|120px]]` | Unknown | 26 | 0 | 2 |
| `[[File:In the mill.jpg|120px]]` | Unknown | 26 | 0 | 2 |
| `[[File:Bianco-site.jpg|120px]]` | Unknown | 31 | 0 | 1 |
| `[[File:Glückauf-Brauerei in Gersdorf, Sachsen 2H1A0125WI.jpg|120px]]` | Unknown | 31 | 0 | 1 |
| `[[File:Kläranlagen bei Chemnitz, Sachsen. 2H1A3555WI.jpg|120px]]` | Unknown | 31 | 0 | 1 |
| `[[File:Nabburg Neusath Freilandmuseum Rauberweihermühle-20190823-RM-123306.jpg|120px]]` | Unknown | 31 | 0 | 1 |
| `[[File:Working mechanism.jpg|120px]]` | Unknown | 31 | 0 | 1 |
| `[[File:Balutola sky view January.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Bergamo atelier artisanal de ferronnier Via San Lorenzo (2).jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Borassus tree.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Brauerei Ulm 01.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Ceiling of China Industrial Museum in Shenyang.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Corn field Balutola.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Cricova winery (Oct 2025) 3.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Factory interiors 003 2005 10 13.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Glückauf-Brauerei in Gersdorf, Sachsen 2H1A0105WI.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Hergiswil-Glass-Factory.3.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Huta Pokój walcownia 2019 (1).jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:In the fishing port.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Inside vacant factory in Duluth Minnesota.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Interior of China Industrial Museum in Shenyang.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Interior of a mill.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Interior of the Pumphouse in Winnipeg Manitoba.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Machine outer body.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Machinery in industry.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Nabburg Neusath Freilandmuseum Sägemühle-20190823-RM-121417.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Nailing Machine.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Opening of a machine.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Production for beer in Qingdao.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Production lines for beer in Qingdao.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Ships_under_construction_at_Chantiers_de_l'Atlantique_shipyard,_2025_(1).jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Ships_under_construction_at_Chantiers_de_l'Atlantique_shipyard,_2025_(4).jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Ships_under_construction_at_Chantiers_de_l'Atlantique_shipyard,_2025_(5).jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Simri Bakhtiyarpur railway station front view.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Trélon Interior of glass factories in Atelier Musée du Verre.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Turbines pumped storage plant 1909-1416.jpg|120px]]` | Unknown | 36 | 0 | 0 |
| `[[File:Villeneuve d'Ascq Cog wheels interiror of Moulin des Oliaux.jpg|120px]]` | Unknown | 36 | 0 | 0 |

## 4. 推薦程式架構

### 技術棧 (Suggested Tech Stack)
* **Language:** Python 3.10+
* **MediaWiki Parser:** `mwparserfromhell`
* **API Client:** `Pywikibot` 或原生 `requests`
* **Data Analysis:** `Pandas`

### 程式流程圖 (Mermaid)

```mermaid
graph TD
    Start[讀取 .mw 檔案] --> Parse[解析 === 標題與投票模板]
    Parse --> API_Check{API 驗證資格}
    API_Check -- 通過 --> Logic{檢查規則}
    API_Check -- 不通過 --> Discard[剔除投票]
    Logic -- 自投/重複 --> Modify[修正為 0 分]
    Logic -- 正常 --> Calc[加總 Score/Support]
    Calc --> Sort[執行 Tie-break 排序]
    Sort --> Output[生成 Markdown 報表]


5. API 整合參考
本工具需串接 Wikimedia Commons API 進行動態驗證：
用戶資格： action=query&list=users&usprop=editcount|registration
參賽者確認： action=query&prop=revisions&titles=File:NAME.jpg