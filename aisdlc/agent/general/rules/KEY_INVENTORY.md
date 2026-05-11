# 系統金鑰與憑證盤點清冊 (AI 檢核輔助)

## 🎯 文件目的

本文件旨在協助 AI 自動化檢核機制，全面盤點本系統中所有與「加解密」、「身分認證」及「外部憑證」相關的模組與功能。

**背景：** 為了防止因金鑰/憑證效期管理不當而導致的系統中斷 (Outage)，AI 將自動掃描程式碼以發現潛在的金鑰。**這份盤點表將作為 AI 檢核的「事實基礎 (Ground Truth)」**。

請系統負責人 (Owner) 詳實填寫以下表格，AI 將以此清冊進行交叉比對，主動示警「未被納管」或「帳實不符」的潛在風險。

---

## 📝 系統基本資料

* **系統名稱：** `[請填寫系統名稱]`
* **系統 Owner：** `[請填寫主要負責人]`
* **最後更新日期：** `[YYYY-MM-DD]`

---

## 🔒 盤點項目

### (1) 身分認證 (Identity Authentication)

*包含：系統登入、API 存取、JWT 驗證、OAuth、LDAP 帳號等*

| 項目名稱 | 功能描述 | 使用模組/技術 | 金鑰/憑證類型 | 管理方式/位置 | 是否有已知效期? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `範例：後台登入` | `後台管理員登入驗證` | `JWT (HS256)` | `JWT Secret` | `[Config檔] /secrets/jwt-secret` | 否 |
| `範例：SSO 整合` | `串接公司 AD 進行單一簽核` | `LDAP` | `Service Account Pwd` | `[金鑰庫] Vault-AD-Prod` | 是 (90天) |
| | | | | | |
| | | | | | |

---

### (2) 傳輸加密 (Transmission Encryption)

*包含：HTTPS (SSL/TLS), FTPS, SFTP, API 呼叫的 mTLS 憑證等*

| 項目名稱 | 功能描述 | 使用模組/技術 | 金鑰/憑證類型 | 管理方式/位置 | 是否有已知效期? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `範例：系統入口網站` | `提供使用者 HTTPS 服務` | `Nginx + SSL` | `SSL Certificate (.pfx)` | `[地端] IIS 憑證庫` | 是 (1 年) |
| `範例：報表上傳` | `每日定時上傳報表至財會主機` | `SFTP` | `SSH Private Key (.ppk)` | `[Config檔] /app/keys/sftp.ppk` | 否 |
| | | | | | |
| | | | | | |

---

### (3) 資料加密 (Data-at-Rest Encryption)

*包含：對資料庫欄位、檔案、或備份資料進行的加解密*

| 項目名稱 | 功能描述 | 使用模組/技術 | 金鑰/憑證類型 | 管理方式/位置 | 是否有已知效期? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `範例：個資欄位` | `加密 DB 中的身分證字號欄位` | `AES-256 (GCM)` | `AES Key (對稱金鑰)` | `[金鑰庫] Azure Key Vault` | 否 |
| `範例：設定檔加密` | `加密 Web.config 中的連線字串` | `aspnet_regiis` | `Machine Key` | `[OS] 系統金鑰` | 否 |
| | | | | | |
| | | | | | |

---

### (4) 訂閱帳號 / 外部 API Key (Subscriptions / External APIs)

*包含：雲端服務 (AWS/GCP/Azure)、第三方 API (Google Maps)、Apple 開發者帳號、軟體授權 (License Key) 等*

| 項目名稱 | 功能描述 | 使用模組/技術 | 金鑰/憑證類型 | 管理方式/位置 | 是否有已知效期? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `範例：Apple 推播` | `iOS APP 的 APNs 推播` | `APNs` | `.p8 Auth Key` | `[手動] Apple Developer 網站` | 是 (不一定) |
| `範例：地址轉換` | `呼叫 Google Maps API 轉經緯度` | `REST API` | `API Key` | `[Config檔] app.settings` | 否 |
| `範例：物件儲存` | `存取 AWS S3 儲存圖片` | `AWS SDK` | `Access Key / Secret` | `[K8s] Secret` | 否 (但可輪替) |
| | | | | | |

---

### (5) 其他 (Others)

*其他未歸類於上述項目，但仍具備金鑰、密碼、憑證性質的項目*

| 項目名稱 | 功能描述 | 使用模組/技術 | 金鑰/憑證類型 | 管理方式/位置 | 是否有已知效期? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `範例：DB 連線` | `系統連線至 MS SQL 資料庫` | `ADO.NET` | `DB User / Password` | `[Config檔] ConnectionStrings` | 是 (180天) |
| | | | | | |
| | | | | | |