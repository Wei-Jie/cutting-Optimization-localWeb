# 開發安全規範：應用程式安全與組態管理實作

**版本**: 3.0
**日期**: 2025-09-03
**適用範圍**: `application_secure_infa_design.md v3.0` 中描述之原則的程式碼實作。

## 1. 組態與環境變數 (Configuration & Environment)

### CG-SEC-008: 【強制】嚴禁在程式碼中硬編碼 IP 位址或主機名稱
- **規範**:
  1.  程式碼中**不應**出現任何寫死的 IP 位址或主機名稱字串（例如 `"10.20.30.40"`, `"api.example.com"`）。
  2.  所有外部服務的連線資訊，**必須**透過組態檔或環境變數讀取。

- **風險**: 硬編碼會導致應用程式失去彈性，在更換環境或 IP 變更時，需要重新修改、編譯和部署程式碼，極易造成部署錯誤與管理混亂。

- **範例 (Spring Boot `application.properties`)**:
  ```properties
  # 不合規的寫法 (Java Code)
  # String url = "[http://10.20.30.40:8080/api/v1/data](http://10.20.30.40:8080/api/v1/data)";

  # 合規的寫法 (Properties File)
  external.service.url=[http://10.20.30.40:8080/api/v1/data](http://10.20.30.40:8080/api/v1/data)