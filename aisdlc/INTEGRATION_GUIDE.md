# AISDLC 框架整合指南

## 🚀 將 AISDLC 整合到任何專案

### 一分鐘快速整合

#### 1. 整合框架到專案（推薦使用 Git Submodule）

**推薦方式：使用 Git Submodule**
```bash
cd your-project/
git submodule add <AISDLC-repo-url> aisdlc
git submodule update --init
```

整合後的專案結構：
```
your-project/
├── aisdlc/                   # AISDLC 框架（submodule）
│   ├── agent/               # Agent 配置文件
│   ├── workflow/            # Workflow 流程文件
│   ├── prompts/             # Prompt 模板
│   ├── docs_template/       # 文檔模板
│   └── AISDLC_INIT.md      # 初始化配置
├── src/                     # 你的專案代碼
└── ...
```

**替代方式：直接複製（適合快速測試）**
```bash
# 將 agent/、workflow/、prompts/、docs_template/ 複製到專案根目錄
```

#### 2. 標準使用流程（任何 LLM 工具）

##### Step 1: 載入初始化配置
無論使用什麼 LLM 工具（ChatGPT、Claude、Copilot、Gemini 等），先輸入：

**使用 Submodule 方式：**
```
請載入 aisdlc/AISDLC_INIT.md 文件，建立按需載入的 workflow-agent 映射關係。
```

**使用複製方式：**
```
請載入 AISDLC_INIT.md 文件，建立按需載入的 workflow-agent 映射關係。
```

##### Step 2: 確認載入成功
LLM 應該回應類似：
```
✅ AISDLC 按需載入機制已啟用！
映射表已載入：7個 Workflow → 對應 Agent
省 Token 設計：初始化僅 ~200 tokens
準備接收 workflow 指令！
```

##### Step 3: 執行 Workflow
```
執行 requirements-extraction workflow 分析我的需求：
[貼上你的截圖或需求描述]
```

## 🎯 按需載入優勢

### Token 消耗對比
| 載入方式 | 初始化 | 單個 Workflow | 總計 | 節省率 |
|----------|--------|---------------|------|--------|
| 傳統全載入 | ~2000 tokens | +300 tokens | ~2300 | - |
| 按需載入 | ~200 tokens | +400 tokens | ~600 | **74%** |

### 實際使用場景
```yaml
場景一_只用單個workflow:
  傳統方式: 載入全部 7 個 workflow 配置
  按需方式: 只載入需要的 1 個
  節省: 85% tokens

場景二_使用多個workflow:
  傳統方式: 一次載入全部
  按需方式: 逐步載入 + 智能緩存
  節省: 40-60% tokens
```

## 🔧 整合到不同 LLM 工具

### ChatGPT (OpenAI)
```
1. 開始新對話
2. 上傳或貼入 AISDLC_INIT.md 內容  
3. 說：「載入此 AISDLC 配置」
4. 開始使用：「執行 [workflow名稱]」
```

### Claude (Anthropic)
```
1. 開始新對話
2. 貼入 AISDLC_INIT.md 內容
3. 說：「請載入這個 AISDLC 初始化配置」  
4. 執行：「我要使用 [workflow名稱] 分析需求」
```

### Copilot Chat (Microsoft)
```
1. 在專案根目錄開啟 Copilot Chat
2. 輸入：「@workspace 載入 AISDLC_INIT.md」
3. 確認載入成功後使用 workflow
```

### 其他 LLM 工具
```
通用步驟：
1. 確保 LLM 可以讀取 AISDLC_INIT.md
2. 要求載入該配置文件  
3. 等待確認載入成功
4. 開始使用 workflow
```

## ✅ 驗證整合正確性

### 載入後檢查清單
使用以下問題測試 LLM 是否正確載入：

#### 基本映射測試
```
問：「requirements-extraction workflow 需要哪些 agent？」
正確答案：sa-analyst (主要) + ba-business-analyst (支援)
```

#### 按需載入測試  
```
問：「我要執行 api-specification workflow」
正確回應應包含：
- 🔄 正在載入相關配置...
- ✅ 載入 sd-architect (Marcus)
- ✅ 載入 qa-tester (Quincy)
```

#### 規則執行測試
```
執行任何 workflow 時應該：
✅ 有明確的確認點
✅ 遵循「不確定就問」原則  
✅ 產出符合 AISDLC 格式的文檔
```

## 🔍 常見整合問題

### 問題 1：LLM 沒有按需載入
**症狀**：直接執行 workflow，沒有顯示載入過程
**解決**：
```
提醒 LLM：「請按照 AISDLC_INIT.md 的按需載入流程，
先載入對應的 agent 配置再執行 workflow」
```

### 問題 2：跳過確認點
**症狀**：LLM 沒有在標記為 🔴 的點暫停確認
**解決**：
```
提醒：「請嚴格執行所有 MANDATORY 確認點，
在每個 🔴 標記處等待我的確認」
```

### 問題 3：Agent 文件讀取失敗
**症狀**：顯示「無法載入 [agent].yaml」
**解決**：
1. 確認框架目錄是否完整（submodule: `aisdlc/`，複製: 根目錄）
2. 檢查文件路徑是否正確（submodule: `aisdlc/agent/`，複製: `agent/`）
3. 若使用 submodule，確認已執行 `git submodule update --init`
4. 確保 LLM 有讀取文件權限

### 問題 4：沒有套用 Agent 規則
**症狀**：執行風格不符合 Agent 人格設定
**解決**：

**使用 Submodule 方式：**
```
要求 LLM 重新載入：「請重新讀取 aisdlc/agent/sa-analyst.yaml
並嚴格按照其中的 core_principles 執行」
```

**使用複製方式：**
```
要求 LLM 重新載入：「請重新讀取 agent/sa-analyst.yaml
並嚴格按照其中的 core_principles 執行」
```

## 📊 整合效果驗證

### 成功整合的標準
- ✅ 可以按需載入指定 Agent
- ✅ 嚴格執行確認點
- ✅ 產出符合模板的文檔
- ✅ 遵循 Agent 人格規則

### 效能指標
```yaml
載入效率:
  傳統方式: 2-3 秒載入全部配置
  按需方式: 0.5 秒載入映射 + 1 秒載入需要的 agent

記憶體使用:
  傳統方式: 保持 7 個 workflow + 6 個 agent 在內存
  按需方式: 只保持當前使用的配置

用戶體驗:
  傳統方式: 初始等待時間長，後續執行快
  按需方式: 初始快速載入，執行時動態載入
```

## 🔧 Git Submodule 管理（推薦方式）

### 為什麼使用 Git Submodule？

**優勢：**
- ✅ **版本控制** - 精確追蹤使用的框架版本
- ✅ **輕鬆更新** - 一行指令更新到最新版本
- ✅ **保持獨立** - 框架與專案代碼分離
- ✅ **團隊同步** - 所有成員使用相同版本

### 常用操作

#### 初始整合
```bash
# 添加 AISDLC 為 submodule
git submodule add <AISDLC-repo-url> aisdlc
git commit -m "Add AISDLC framework as submodule"
```

#### 團隊成員初始化
```bash
# Clone 專案後初始化 submodule
git clone <your-project-url>
git submodule update --init --recursive
```

#### 更新框架版本
```bash
# 更新到最新版本
cd aisdlc
git pull origin master
cd ..
git add aisdlc
git commit -m "Update AISDLC to latest version"
```

#### 切換到特定版本
```bash
cd aisdlc
git checkout v1.2.0  # 切換到特定 tag
cd ..
git add aisdlc
git commit -m "Pin AISDLC to v1.2.0"
```

### 多倉庫協作（前後端分離）

當專案有多個開發倉庫時，可共享同一份文檔：

```
project-backend/
├── src/                     # 後端代碼
└── aisdlc/                  # 文檔 submodule

project-frontend/
├── src/                     # 前端代碼
└── aisdlc/                  # 同一個 submodule
```

**優勢**：
- 所有團隊共用同一份 PRD/FRD
- 確保需求理解一致
- 文檔變更自動同步

## 🚀 進階整合技巧

### 技巧 1：預設 Workflow 綁定
在特定類型專案中，可以預設常用的 workflow：
```
# 在專案 README 中加入
## AISDLC 預設配置
- 需求分析：requirements-extraction  
- 系統設計：user-story-design
- API 規格：api-specification
```

### 技巧 2：自訂 Agent 配置
整合框架後，可以調整 Agent 配置以符合團隊風格：

**使用 Submodule 方式（推薦）：**
```bash
# Fork AISDLC 倉庫後，在你的 fork 中修改
# 然後將 submodule 指向你的 fork
git submodule set-url aisdlc <your-fork-url>
git submodule update --remote
```

**使用複製方式：**
```yaml
# 直接修改 agent/sa-analyst.yaml 的 core_principles
core_principles:
  - "Human-Centric Validation"
  - "[你的團隊特定原則]"
  - "[你的品質標準]"
```


## 💡 最佳實踐

### DO（推薦做法）
- ✅ 每次使用前載入 AISDLC_INIT.md
- ✅ 讓 LLM 顯示載入過程，確認配置正確  
- ✅ 耐心配合所有確認點
- ✅ 定期檢查產出文檔是否符合模板

### DON'T（避免做法）
- ❌ 跳過初始化直接使用 workflow
- ❌ 催促 LLM 跳過確認點
- ❌ 修改核心 workflow 文件
- ❌ 在沒有完整 agent 配置時強行執行

---

## 🔄 持續改進

AISDLC 框架會持續演進，建議：
1. 定期更新框架文件
2. 根據團隊需求調整 Agent 配置
3. 分享使用經驗和改進建議

**記住**：AISDLC 的價值在於標準化和自動化軟體開發生命週期中的需求分析階段，讓團隊能專注於創造價值而非重複性工作。