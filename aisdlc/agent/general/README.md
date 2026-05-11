# 通用檢核規則庫使用說明

## 概述

本文件說明如何使用通用檢核規則庫系統，透過 AI 掃描器自動化檢核專案原始碼中的安全風險物證。此系統分為兩大部分：**檢核規則庫** (`CHECK_KEY_RULES.md`) 和 **金鑰盤點清冊** (`KEY_INVENTORY.md`)，可協助系統負責人全面掌握專案中的金鑰、憑證和敏感資訊。

## 規則庫結構

```
agent/general/rules/
├── CHECK_KEY_RULES.md    # AI 檢核規則庫（AI 掃描器使用的規則）
└── KEY_INVENTORY.md       # 系統金鑰與憑證盤點清冊（Owner 填寫的事實基礎）
```

## 第一部分：AI 檢核規則庫 (CHECK_KEY_RULES.md)

AI 檢核規則庫定義了 AI 掃描器在分析專案原始碼時，必須尋找的「物證特徵」(Patterns)。

### 文件目的

- **獨立運作**：AI 掃描器將獨立於 Owner 填寫的 `KEY_INVENTORY.md` 運作
- **產生物證清單**：AI 的任務是根據本規則檔，產生一份「物證清單」(Evidence List)
- **風險識別**：透過比對物證清單與盤點清冊，識別未被納管的風險

**治理流程：** `(AI 掃描器產生的物證清單) - (Owner 填寫的 KEY_INVENTORY.md) = 需立即處理的風險`

### 檢核規則分類

#### (1) 身分認證 (Identity)

**規則 1.1：關鍵字/函式庫 (Keywords / Libraries)**
- **描述**：尋找所有已知的身分認證相關模組
- **特徵範例**：
  - `import jwt`
  - `using System.IdentityModel.Tokens.Jwt`
  - `using Microsoft.AspNetCore.Identity`
  - `import oauth2`
  - `ldap_bind`
  - `new JwtSecurityTokenHandler()`

#### (2) 傳輸加密 (Transport)

**規則 2.1：安全傳輸協定 (Secure Protocols)**
- **描述**：尋找 SSL/TLS, SFTP 等安全傳輸的實作
- **特徵範例**：
  - `using System.Net.Security.SslStream`
  - `import javax.net.ssl`
  - `SftpClient`
  - `"-----BEGIN CERTIFICATE-----"`

**規則 2.2：不安全傳輸 (Insecure Protocols)**
- **描述**：尋找並示警不安全的傳輸 (HTTP, FTP)
- **特徵範例**：
  - `FtpWebRequest`
  - `http://` (出現在 URL 字串中，需排除 localhost)

#### (3) 資料加密 (Data-at-Rest)

**規則 3.1：加密演算法 (Crypto Libraries)**
- **描述**：尋找所有已知的對稱/非對稱加密演算法函式庫
- **特徵範例**：
  - `using System.Security.Cryptography`
  - `AES.Create()`
  - `CreateEncryptor()`
  - `RsaCryptoServiceProvider`
  - `import org.bouncycastle`

#### (4) 訂閱帳號 / 外部 API Key (External APIs)

**規則 4.1：API 金鑰格式 (API Key Regex)**
- **描述**：透過正規表示式 (Regex) 尋找已知第三方 API Key 的獨特格式
- **特徵範例**：
  - Google API Key: `AIza[0-9A-Za-z\\-_]{35}`
  - AWS Access Key: `(A3T[A-Z0-9]|AKIA|AGPA|AROA|AIDA)[A-Z0-9]{16}`
  - Stripe API Key: `sk_live_[0-9a-zA-Z]{24}`
  - GitHub Token: `ghp_[0-9a-zA-Z]{36}`

**規則 4.2：外部端點 (External Endpoints)**
- **描述**：尋找程式碼中呼叫的已知高風險 API 網域
- **特徵範例**：
  - `maps.googleapis.com`
  - `api.push.apple.com`
  - `graph.facebook.com`

#### (5) 其他 (Secrets)

**規則 5.1：硬編碼密碼 (Hardcoded Passwords - Regex)**
- **描述**：尋找格式符合密碼、連線字串的字串
- **特徵範例**：
  - `[Pp]assword\s*=\s*['"](.)+['"]`
  - `ConnectionStrings?\[['"]`
  - `User ID\s*=\s*...`

**規則 5.2：私鑰格式 (Private Key Formats)**
- **描述**：尋找私鑰的 PEM 標頭
- **特徵範例**：
  - `-----BEGIN RSA PRIVATE KEY-----`
  - `-----BEGIN EC PRIVATE KEY-----`
  - `-----BEGIN OPENSSH PRIVATE KEY-----`

**規則 5.3：高熵值字串 (High Entropy Strings)**
- **描述**：(進階規則) 尋找隨機性高、看起來像密碼的長字串
- **特徵範例**：
  - `[a-zA-Z0-9/+]{20,}` (簡易的 Base64 偵測)

## 第二部分：系統金鑰與憑證盤點清冊 (KEY_INVENTORY.md)

系統金鑰與憑證盤點清冊是系統負責人 (Owner) 填寫的「事實基礎 (Ground Truth)」，用於與 AI 掃描結果進行交叉比對。

### 文件目的

- **事實基礎**：作為 AI 檢核的「事實基礎 (Ground Truth)」
- **風險識別**：AI 將以此清冊進行交叉比對，主動示警「未被納管」或「帳實不符」的潛在風險
- **全面盤點**：協助系統負責人全面盤點本系統中所有與「加解密」、「身分認證」及「外部憑證」相關的模組與功能

### 盤點項目分類

1. **身分認證 (Identity Authentication)**
   - 系統登入、API 存取、JWT 驗證、OAuth、LDAP 帳號等

2. **傳輸加密 (Transmission Encryption)**
   - HTTPS (SSL/TLS), FTPS, SFTP, API 呼叫的 mTLS 憑證等

3. **資料加密 (Data-at-Rest Encryption)**
   - 對資料庫欄位、檔案、或備份資料進行的加解密

4. **訂閱帳號 / 外部 API Key (Subscriptions / External APIs)**
   - 雲端服務 (AWS/GCP/Azure)、第三方 API (Google Maps)、Apple 開發者帳號、軟體授權 (License Key) 等

5. **其他 (Others)**
   - 其他未歸類於上述項目，但仍具備金鑰、密碼、憑證性質的項目

## 如何使用檢核規則庫

### 1. 執行 AI 掃描

使用以下 Prompt 來指導 AI 執行掃描：

```
請根據 @CHECK_KEY_RULES.md 中的檢核規則，掃描 @src 目錄（或指定目錄）找出可能的物證。

要求：
1. 根據規則庫中的特徵 (Patterns) 逐一檢查所有程式碼檔案
2. 列出所有符合特徵的檔案和行數
3. 根據檢核規則的分類（身分認證、傳輸加密、資料加密、外部 API Key、其他）進行分類
4. 將結果匯出成 Scanner.md 文件

輸出格式：
- 每個物證需包含：檔案路徑、行數、匹配的特徵、規則編號
- 按照規則分類組織結果
- 標示風險等級（高/中/低）
```

### 2. 掃描流程

1. **載入規則庫**：確保 AI 已載入 `CHECK_KEY_RULES.md`
2. **指定掃描範圍**：明確指定要掃描的目錄（通常是 `src` 或專案根目錄）
3. **執行掃描**：AI 根據規則庫中的特徵逐一檢查程式碼
4. **產生物證清單**：將掃描結果整理成 `Scanner.md`
5. **交叉比對**：將 `Scanner.md` 與 `KEY_INVENTORY.md` 進行比對
6. **風險識別**：識別未被納管或帳實不符的風險項目

### 3. 解讀掃描結果

掃描結果 (`Scanner.md`) 將包含：

- **檔案清單**：所有符合特徵的檔案路徑
- **行數標示**：每個物證的具體行數
- **特徵分類**：根據檢核規則的分類進行組織
- **風險等級**：根據物證類型標示風險等級

### 4. 風險處理流程

1. **比對物證清單與盤點清冊**
   - 找出 `Scanner.md` 中有但 `KEY_INVENTORY.md` 中沒有的項目
   - 找出 `KEY_INVENTORY.md` 中有但 `Scanner.md` 中沒有的項目（可能已移除或變更）

2. **評估風險等級**
   - **高風險**：硬編碼密碼、私鑰、API Key 洩露
   - **中風險**：使用不安全傳輸協定、缺少加密實作
   - **低風險**：使用認證模組但未發現明顯風險

3. **處理建議**
   - 立即處理高風險項目
   - 將新發現的物證納入 `KEY_INVENTORY.md`
   - 更新或移除已不存在的項目

## Prompt 範例

### 基本掃描 Prompt

```
請根據 @agent/general/rules/CHECK_KEY_RULES.md 中的檢核規則，掃描專案中的 @src 目錄（如果不存在，請掃描整個專案），找出所有符合規則特徵的物證。

要求：
1. 逐一檢查 CHECK_KEY_RULES.md 中定義的所有特徵 (Patterns)
2. 列出所有符合特徵的檔案和行數
3. 根據規則分類（身分認證、傳輸加密、資料加密、外部 API Key、其他）進行分類
4. 標示每個物證的風險等級（高/中/低）
5. 將結果匯出成 Scanner.md 文件

輸出格式請參考 Scanner.md 的結構。
```

### 進階掃描 Prompt（包含比對）

```
請執行以下任務：

1. 根據 @agent/general/rules/CHECK_KEY_RULES.md 掃描 @src 目錄，找出所有物證
2. 將掃描結果與 @agent/general/rules/KEY_INVENTORY.md 進行交叉比對
3. 識別以下風險：
   - Scanner.md 中有但 KEY_INVENTORY.md 中沒有的項目（未被納管）
   - KEY_INVENTORY.md 中有但 Scanner.md 中沒有的項目（可能已移除）
4. 產生風險報告，包含：
   - 未被納管的風險項目清單
   - 建議處理方式
   - 優先級排序
```

## 最佳實踐

1. **定期掃描**：建議每個 Sprint 或重要更新後執行掃描
2. **及時更新**：發現新物證後立即更新 `KEY_INVENTORY.md`
3. **風險優先**：優先處理高風險項目（硬編碼密碼、私鑰等）
4. **版本控制**：將 `Scanner.md` 和 `KEY_INVENTORY.md` 納入版本控制
5. **團隊協作**：確保系統負責人定期審查和更新盤點清冊

## 注意事項

1. **掃描範圍**：明確指定掃描目錄，避免掃描不必要的檔案（如 node_modules、.git 等）
2. **誤報處理**：某些特徵可能產生誤報，需要人工審查確認
3. **敏感資訊**：掃描結果可能包含敏感資訊，請妥善保管 `Scanner.md`
4. **持續更新**：隨著專案發展，可能需要更新檢核規則庫以涵蓋新的風險類型
5. **工具整合**：可考慮將此流程整合到 CI/CD 流程中，實現自動化檢核

---

透過使用這套檢核規則庫系統，可以確保專案中的金鑰、憑證和敏感資訊得到全面盤點和有效管理，降低因金鑰/憑證效期管理不當而導致的系統中斷風險。

