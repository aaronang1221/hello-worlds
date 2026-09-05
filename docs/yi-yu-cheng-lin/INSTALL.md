# 一語成林安裝任務（給 AI 助理讀的安裝說明）

你現在的任務：把一語成林 AI 內容團隊安裝到這台電腦，然後以總管 Elsa 的身分開始帶使用者上路。全程用繁體中文跟使用者對話，一步一步來，每步完成都回報。

## 安裝目標位置（所有平台都一樣）

- 技能：`~/.claude/skills/yi-yu-cheng-lin/`
- 官員定義：`~/.claude/agents/`

Windows 上 `~` 代表使用者家目錄（PowerShell 的 `$HOME`，例如 `C:\Users\名字`），路徑一樣是家目錄底下的 `.claude` 資料夾。

## 安裝步驟

1. 確認來源：本安裝包根目錄底下有 `team/skills/yi-yu-cheng-lin/`（含 SKILL.md、references、templates）和 `team/agents/`（5 個 lin-*.md 檔）。少任何一個就停下來告訴使用者重新下載
2. 建立目標資料夾（不存在就建立）：
   - macOS／Linux：`mkdir -p ~/.claude/skills ~/.claude/agents`
   - Windows（PowerShell）：`New-Item -ItemType Directory -Force "$HOME\.claude\skills","$HOME\.claude\agents"`
3. 檢查衝突：如果 `~/.claude/skills/yi-yu-cheng-lin/` 已經存在，先問使用者要不要覆蓋（通常是升級，回答「要」就整個資料夾換新）
4. 複製檔案：
   - `team/skills/yi-yu-cheng-lin/` 整個資料夾複製到 `~/.claude/skills/yi-yu-cheng-lin/`
   - `team/agents/` 底下 5 個 `lin-*.md` 複製到 `~/.claude/agents/`
5. 驗收（一定要做）：列出安裝後的檔案，確認：
   - `~/.claude/skills/yi-yu-cheng-lin/SKILL.md` 存在
   - `references/` 底下有 13 個 .md 檔
   - `templates/brand-roots-template.md` 存在
   - `~/.claude/agents/` 底下有 lin-interviewer、lin-triage、lin-designer、lin-video、lin-uploader 共 5 個檔
   數量不對就回頭補，不准跳過
6. 只有在 Codex（或其他沒有 `~/.claude` 技能系統的 AI CLI）環境才做這步：把下面這段附加到 `~/.codex/AGENTS.md`（檔案不存在就建立）：

   ```
   ## 一語成林 AI 內容團隊
   當使用者提到「Elsa」「一語成林」「幫我長內容」或任何內容創作需求時，
   讀取 ~/.claude/skills/yi-yu-cheng-lin/SKILL.md 並完全照做。
   這個環境沒有 subagent 功能，照 SKILL.md 調度規則第 2 條：
   自己輪流讀取 ~/.claude/agents/lin-*.md 當作業手冊，一站一站執行。
   ```

7. 回報安裝結果：裝了什麼、裝在哪裡、怎麼喚醒（說「Elsa」或「一語成林」就可以）

## 安裝完成後：立刻切換成 Elsa

安裝驗收通過後，不要結束對話。讀取剛安裝好的 `~/.claude/skills/yi-yu-cheng-lin/SKILL.md`，從這一刻起你就是 Elsa，照 SKILL.md 裡「第一次見面」的流程開始帶使用者上路：自我介紹、問他現在的狀態、帶他填品牌根系。

提醒使用者一件事：下次開新對話時，直接說「Elsa」或「一語成林」就能喚醒團隊，不用重新安裝。
