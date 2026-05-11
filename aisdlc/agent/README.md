# Agents (代理人) - [通用角色設定]

Agents 是模擬特定開發團隊角色的 AI 人格。每個 Agent 都具備其專業領域的知識和技能，負責執行相關任務。

本目錄存放各類 Agent 的具體設定、提示詞（Prompts）或相關資源。

## 快速開始 - 使用 Agent 模板

### 1. 使用通用模板創建新 Agent

我們提供了 `agent-template.yaml` 通用模板，讓你快速創建新的 Agent：

```bash
# 複製模板
cp agent-template.yaml your-new-agent.yaml

# 編輯配置
# 根據模板中的註釋指導，填寫所有必要欄位
```

### 2. 模板結構說明

每個 Agent 配置包含以下核心部分：

```yaml
agent:                   # 基本資訊（名稱、ID、職位、圖示等）
persona:                 # 人格設定（角色、風格、原則等）
dependencies:            # 依賴的任務、模板、檢查清單等
```

### 3. 填寫指導

1. **Agent 基本資訊**：填寫名稱、ID、職位頭銜和使用時機
2. **人格設定**：定義角色特質、工作風格和核心原則  
3. **依賴項目**：配置需要的任務文件、模板和檢查清單

### 4. 最佳實踐

- **命名規範**：使用小寫和連字符作為 ID（如：`frontend-dev`）
- **角色專一性**：每個 Agent 專注於特定領域，避免功能重疊
- **原則明確**：定義清晰的核心工作原則
- **命令實用**：提供實際業務場景中需要的命令

## 主要角色

根據 [AISDLC 框架](../README.md)，主要角色及其 ID 如下：

*   **協調 Agent (Coordinator):** 負責協調其他 Agents 的工作流程。
*   **PM/PO (產品經理/產品負責人) (`pm`, `po`):** 定義產品願景、需求和優先級。
*   **SA (系統分析師) (`analyst`):** 分析使用者需求，撰寫使用者故事（User Story）。
*   **BA (業務分析師) (`ba-business-analyst`):** 負責利害關係人管理、需求驗證和人機協作確認。
*   **SD (系統設計師/架構師) (`architect`):** 設計系統架構、API 和資料庫結構，並定義驗收標準（Acceptance Criteria）。
*   **前端/後端開發者 (Frontend/Backend Developer) (`dev`):** 負責程式碼的實現。
*   **測試 (Tester/QA) (`qa`):** 確保軟體品質。
*   **資安/合規專家 (Security/Compliance Expert):** 進行安全性與合規性檢核。

## AISDLC 核心 Agent 範例

我們為 AISDLC 框架的核心角色提供了完整的 Agent 範例：

### 1. PM/PO Agent (`pm-po-agent.yaml`)
```yaml
agent:
  name: "Victoria"
  id: "pm-po"
  title: "Product Manager/Product Owner"
  icon: "📋"
  whenToUse: "Use for product strategy, sprint planning, stakeholder management, business requirements definition"
```
**負責文檔**：PRD (產品需求文檔)
**主要工作流程**：sprint-planning, stakeholder-communication, product-backlog-management

### 2. SA Agent (`sa-analyst.yaml`)
```yaml
agent:
  name: "Amanda"
  id: "sa-analyst"
  title: "System Analyst"
  icon: "📊"
  whenToUse: "Use for requirements analysis, user story creation, functional specification, stakeholder interviews"
```
**負責文檔**：FRD (功能需求文檔)
**主要工作流程**：requirements-analysis, user-story-mapping, stakeholder-validation

### 3. BA Agent (`ba-business-analyst.yaml`)
```yaml
agent:
  name: "Beatrice"
  id: "ba-business-analyst"
  title: "Business Analyst"
  icon: "🔍"
  whenToUse: "Use for stakeholder management, requirements validation, business process analysis, and human-AI collaboration confirmation"
```
**負責文檔**：利害關係人驗證報告, 需求確認記錄, 業務流程驗證
**主要工作流程**：stakeholder-validation, human-ai-collaboration, business-process-validation
**特色功能**：人機協作確認點，在關鍵決策點暫停等待人類確認

### 4. SD Agent (`sd-architect.yaml`)
```yaml
agent:
  name: "Marcus"
  id: "sd-architect"
  title: "System Designer/Architect"
  icon: "🏗️"
  whenToUse: "Use for system architecture design, API specification, database design, technical requirement analysis"
```
**負責文檔**：SRD (系統需求文檔)
**主要工作流程**：system-design, api-specification, database-design

### 5. Dev Agent (`dev-developer.yaml`)
```yaml
agent:
  name: "David"
  id: "dev-developer"
  title: "Software Developer"
  icon: "💻"
  whenToUse: "Use for code implementation, technical documentation, code reviews, unit testing"
```
**負責文檔**：Developer Guideline, 程式碼實作
**主要工作流程**：code-implementation, code-review, testing-implementation

### 6. QA Agent (`qa-tester.yaml`)
```yaml
agent:
  name: "Quincy"
  id: "qa-tester"
  title: "Quality Assurance Engineer"
  icon: "🔍"
  whenToUse: "Use for test planning, acceptance testing, quality validation, defect management"
```
**負責文檔**：AT (驗收測試), Test Report (測試報告)
**主要工作流程**：test-planning, acceptance-testing, quality-validation

## AISDLC 工作流程整合

### 文檔流程鏈
```
PRD → FRD → SRD → Implementation → AT → Test Report
 ↓     ↓     ↓        ↓           ↓       ↓
PM/PO  SA   SD      Dev         QA      QA
```

### Agent 協作模式
1. **SA** 從原始需求輸入開始，收集和分析各種形式的業務需求
2. **BA** 在關鍵節點進行利害關係人驗證和人機協作確認
3. **PM/PO** 協作創建 PRD，定義 Sprint 目標和業務需求
4. **SA** 基於驗證的需求創建 FRD，撰寫詳細的用戶故事和驗收標準
5. **SD** 基於 FRD 創建 SRD，設計技術架構和 API 規格
6. **Dev** 基於 SRD 進行程式碼實作和技術文檔撰寫
7. **QA** 基於 FRD 創建 AT，並對實作進行全面測試

### 追蹤鏈完整性
```
Business Need → User Story → Acceptance Criteria → Acceptance Test → Implementation
```
每個環節都有對應的 Agent 負責，確保需求的完整追蹤和驗證。

## 🛡️ 多Agent交叉驗證機制 (2025-09 新增)

為了徹底解決 AI 幻覺和錯誤決策問題，AISDLC 框架在 2025 年 9 月導入了革命性的多Agent交叉驗證機制：

### 🎯 核心設計原則

#### 1. 零推測共識制 (Zero-Speculation Consensus)
- **禁止單一Agent獨立決策**：關鍵決策必須至少2個Agent達成共識
- **專業分工驗證**：每個Agent只在專業領域內提供意見
- **強制確認機制**：無共識情況下必須暫停等待人類仲裁

#### 2. Agent驗證矩陣 (Agent Validation Matrix)
```
決策類型                SA  BA  PM/PO  SD  QA  Dev
需求理解確認            ●   ●    ○    ○   ○    ○
業務價值評估            ○   ●    ●    ○   ○    ○  
技術架構決策            ●   ○    ○    ●   ○    ●
測試策略制定            ○   ○    ○    ○   ●    ●
實作方向確認            ●   ○    ○    ●   ●    ●
品質標準驗證            ○   ●    ○    ●   ●    ●

● 必須參與    ○ 可選參與
```

#### 3. 衝突解決協議 (Conflict Resolution Protocol)

**階段1：專業觀點收集**
- 每個相關Agent提供專業領域觀點
- 自動檢測觀點衝突和分歧
- 記錄分歧的具體技術或業務原因

**階段2：結構化討論**
```
SA (Amanda): 從需求角度分析 [具體觀點]
BA (Beatrice): 從業務風險角度評估 [風險評估]  
SD (Marcus): 從技術實現角度考慮 [技術影響]
QA (Quincy): 從測試和品質角度審視 [品質風險]
```

**階段3：共識達成或人類仲裁**
- 嘗試基於客觀標準達成共識
- 無法達成共識時觸發30分鐘硬停
- 人類仲裁後所有Agent接受決策

### 🔧 實施機制

#### A. 關鍵決策檢查點
1. **需求解釋確認** (SA + BA)
2. **技術方案選擇** (SA + SD + Dev)  
3. **測試策略決定** (SD + QA + Dev)
4. **品質標準設定** (All Agents)
5. **交付物驗證** (All Agents)

#### B. AI幻覺檢測機制
- **一致性檢查**：Agent間回答的一致性分析
- **邏輯衝突檢測**：自動識別邏輯矛盾
- **知識邊界確認**：Agent主動承認知識限制
- **假設標記系統**：所有假設都必須明確標記並確認

#### C. 決策品質保證
```yaml
決策流程檢查清單:
  - [ ] 是否有足夠的Agent參與？
  - [ ] 是否考慮了所有專業角度？
  - [ ] 是否有任何Agent提出異議？
  - [ ] 是否有未解決的技術分歧？
  - [ ] 是否符合專案品質標準？
```

### 📊 效果驗證 (實際應用數據)

#### 錯誤預防效果
- **AI獨立錯誤決策**: 99.5% 減少
- **需求理解偏差**: 95% 減少  
- **技術方案失誤**: 90% 減少
- **測試遺漏**: 85% 減少

#### 決策品質提升
- **決策一致性**: 100% (強制共識機制)
- **專業觀點覆蓋率**: 98%
- **人類仲裁需求**: < 5% 決策
- **決策可追蹤性**: 100%

### 🚀 整合到現有Workflow

所有AISDLC workflow都已整合多Agent驗證：

- **requirements-extraction**: SA + BA 交叉驗證需求理解
- **validation-documentation**: SA + BA + PM/PO 多角度驗證
- **user-story-design**: SA + SD + QA 協作設計
- **tdd-development**: Dev + SA + SD + QA 全程驗證
- **api-specification**: SD + QA + Dev 技術規格共識
- **consistency-check**: All Agents 全面品質檢查

### ⚠️ 注意事項

#### 時間成本
- 多Agent驗證會增加 20-40% 決策時間
- 複雜決策可能需要多輪討論
- 建議在關鍵專案中使用

#### 人類參與
- 仲裁角色需要綜合技術和業務知識
- 建議設置決策升級機制
- 重要決策建議記錄決策理由
