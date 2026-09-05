# 模版：IG 輪播製作規範 (IG Carousel Brief)

> 來源：Drive「Ascenity｜IG 轮播视觉与文案制作规范」。行銷部（一語成林）產 IG 輪播時的品牌鐵則。這裡是精簡版，完整 HTML 骨架見原文件。

## 品牌設定（每次固定）
- IG handle：`@JIANLEANG`
- 定位：專為高階決策者與企業領袖打造的頂級高效體態轉型顧問
- 語氣：繁中為主、英文副標裝飾（Cormorant Garamond italic）；以終為始、專業溫暖，**禁 AI 腔**
- 受眾：日理萬機、追求高效與質感的 C-Level 高階主管

## 品牌色（`:root` 變數，只改這三個切換配色）
```
--dark-bg: #557235;  --light-bg: #FEFAE0;  --accent: #DDA15E;   /* 方案A 自然大地 */
--dark-bg: #283618;  --light-bg: #FEFAE0;  --accent: #FFC51D;   /* 方案B 高對比 */
```
文字深 `#283618`／文字淺 `#FEFAE0`。字體：Noto Serif TC(標題) + DM Sans + Noto Sans TC。

## Carousel 結構
| Slide | 內容 |
|---|---|
| 1 封面 | hook + 螢光筆關鍵字 + 照片底圖 / placeholder |
| 2 | 開場 / 承諾（淺底）|
| 3–N | 主要內容，每頁一個重點，深/淺交替 |
| 最後 | 收尾金句 + CTA + `@JIANLEANG` |

## Copy 規則
- 每頁標題短句 + 2–4 字螢光關鍵字；內文 1–3 句、每句 15–30 字。
- CTA 頁先不放，最後才加。

## 輸出
獨立 HTML（400×500、4:5），所有 CSS 內嵌，含滑動/�forward。命名 `carousel-[主題].html`。

## 不要做
❌ 斜體中文　❌ 標題加句號　❌ emoji　❌ 破折號　❌「不是 X，是 Y」句型　❌ 改動已設定的品牌色系
