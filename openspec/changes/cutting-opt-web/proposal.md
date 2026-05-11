## Why

2011 年的二維切割最佳化演算法（王韋傑碩士論文）在處理多種產品組合（5 組以上）時存在嚴重的效能瓶頸（運算過慢）。此外，原始實作缺乏現代化的 Web 展示介面與穩定的任務排程機制，無法支援多使用者併發計算而不導致系統崩潰。

## What Changes

本變更將重現並優化該演算法，並包裝為一個現代化的 Web 應用程式：

1. **演算法優化**：利用 Python 3.11+ 的 `lru_cache` 記憶化搜尋與高效的剪枝邏輯，解決組合爆炸問題。
2. **空間管理**：引入「最大空矩形 (MER)」分割演算法，精確避開指定座標的矩形瑕疵。
3. **Web 化**：建立基於 FastAPI 的後端服務，提供非同步運算 API。
4. **任務排程**：實作生產者-消費者模式的工作佇列，限制併發運算量以防止系統 Crash。
5. **看板介面**：使用 HTML5 Canvas 實現互動式切割佈局預覽。

## Capabilities

### New Capabilities

- `cutting-engine`: 核心二維切割最佳化引擎，支援瑕疵避開與效能優化。
- `task-queue`: 處理 CPU 密集型運算的背景排程系統。
- `visualization-board`: 提供 Web 端互動操作與 Canvas 渲染切割圖形。

### Modified Capabilities

- 無

## Impact

- **新增模組**: `src/engine.py`, `src/server.py`, `static/index.html`, `static/app.js`
- **相依性**: 引入 `pypdf`, `cryptography`, `fastapi`, `uvicorn` 等 Python 庫。
- **架構**: 從單機指令碼升級為 Client-Server 架構。
