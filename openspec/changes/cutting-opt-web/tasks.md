## 1. 核心引擎開發 (Core Engine)

- [x] 1.1 實作 `engine.py` 中的 `Rect` 與 `Bin` 類別，包含瑕疵分割 (MER) 邏輯。
- [x] 1.2 實作 `Optimizer` 類別，包含帶有剪枝與 `lru_cache` 的遞迴搜尋演算法。
- [x] 1.3 編寫單元測試驗證切割準確度與瑕疵避開功能。

## 2. 後端 API 與排程 (Backend & Scheduling)

- [x] 2.1 建立 `server.py`，使用 FastAPI 定義運算請求介面。
- [x] 2.2 實作 `TaskManager` 類別與背景工作隊列，確保任務循序執行。
- [x] 2.3 整合引擎與 API，支援非同步查詢計算狀態與結果。

## 3. 前端介面開發 (Frontend Dashboard)

- [x] 3.1 建立 `index.html` 與 `style.css`，設計簡潔且專業的排版介面。
- [x] 3.2 使用 HTML5 Canvas 實作 `visualizer.js`，負責渲染切割結果。
- [x] 3.3 實作互動邏輯，支援點擊標記瑕疵與提交運算任務。

## 4. 系統整合與優化

- [x] 4.1 進行 5-8 種產品組合的壓力測試，優化搜尋效能。
- [x] 4.2 驗證多使用者併發下的任務排隊行為。
