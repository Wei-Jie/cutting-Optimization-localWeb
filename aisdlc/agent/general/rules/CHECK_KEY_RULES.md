# AI 檢核規則庫 (AI_RULES.md)

## 🎯 文件目的

本文件定義了 AI 掃描器 (Scanner) 在分析專案原始碼時，必須尋找的「物證特徵」(Patterns)。

AI 掃描器將**獨立**於 Owner 填寫的 `KEY_INVENTORY.md` 運作。AI 的任務是根據本規則檔，產生一份「物證清單」(Evidence List)。

**治理流程：** `(AI 掃描器產生的物證清單) - (Owner 填寫的 KEY_INVENTORY.md) = 需立即處理的風險`

---

## 🔬 檢核規則 (AI Reasoning Rules)

### (1) 身分認證 (Identity)

**[規則 1.1] 關鍵字/函式庫 (Keywords / Libraries)**
* **描述：** 尋找所有已知的身分認證相關模組。
* **特徵 (Patterns)：**
    * `import jwt`
    * `using System.IdentityModel.Tokens.Jwt`
    * `using Microsoft.AspNetCore.Identity`
    * `using System.Web.Security`
    * `import oauth2`
    * `ldap_bind`
    * `new JwtSecurityTokenHandler()`

---

### (2) 傳輸加密 (Transport)

**[規則 2.1] 安全傳輸協定 (Secure Protocols)**
* **描述：** 尋找 SSL/TLS, SFTP 等安全傳輸的實作。
* **特徵 (Patterns)：**
    * `using System.Net.Security.SslStream`
    * `import javax.net.ssl`
    * `SftpClient`
    * `"-----BEGIN CERTIFICATE-----"` (偵測 .pem 憑證檔案)

**[規則 2.2] 不安全傳輸 (Insecure Protocols)**
* **描述：** 尋找並示警不安全的傳輸 (HTTP, FTP)。
* **特徵 (Patterns)：**
    * `FtpWebRequest`
    * `http://` (出現在 URL 字串中，需排除 localhost)

---

### (3) 資料加密 (Data-at-Rest)

**[規則 3.1] 加密演算法 (Crypto Libraries)**
* **描述：** 尋找所有已知的對稱/非對稱加密演算法函式庫。
* **特徵 (Patterns)：**
    * `using System.Security.Cryptography`
    * `AES.Create()`
    * `CreateEncryptor()`
    * `RsaCryptoServiceProvider`
    * `import org.bouncycastle`

---

### (4) 訂閱帳號 / 外部 API Key (External APIs)

**[規則 4.1] API 金鑰格式 (API Key Regex)**
* **描述：** 透過正規表示式 (Regex) 尋找已知第三方 API Key 的獨特格式。
* **特徵 (Patterns)：**
    * **Google API Key:** `AIza[0-9A-Za-z\\-_]{35}`
    * **AWS Access Key:** `(A3T[A-Z0-9]|AKIA|AGPA|AROA|AIDA)[A-Z0-9]{16}`
    * **Stripe API Key:** `sk_live_[0-9a-zA-Z]{24}`
    * **GitHub Token:** `ghp_[0-9a-zA-Z]{36}`

**[規則 4.2] 外部端點 (External Endpoints)**
* **描述：** 尋找程式碼中呼叫的已知高風險 API 網域。
* **特徵 (Patterns)：**
    * `maps.googleapis.com`
    * `api.push.apple.com`
    * `graph.facebook.com`

---

### (5) 其他 (Secrets)

**[規則 5.1] 硬編碼密碼 (Hardcoded Passwords - Regex)**
* **描述：** 尋找格式符合密碼、連線字串的字串。
* **特徵 (Patterns)：**
    * `[Pp]assword\s*=\s*['"](.)+['"]`
    * `ConnectionStrings?\[['"]`
    * `User ID\s*=\s*...`

**[規則 5.2] 私鑰格式 (Private Key Formats)**
* **描述：** 尋找私鑰的 PEM 標頭。
* **特徵 (Patterns)：**
    * `-----BEGIN RSA PRIVATE KEY-----`
    * `-----BEGIN EC PRIVATE KEY-----`
    * `-----BEGIN OPENSSH PRIVATE KEY-----`

**[規則 5.3] 高熵值字串 (High Entropy Strings)**
* **描述：** (進階規則) 尋找隨機性高、看起來像密碼的長字串。
* **特徵 (Patterns)：**
    * `[a-zA-Z0-9/+]{20,}` (範例：簡易的 Base64 偵測)