# Cutting Optimizer Web

這是一個基於 Python FastAPI 與 HTML5 Canvas 開發的二維最佳化切割（2D Bin Packing）系統，支援無界限裝箱 (Unbounded) 與瑕疵避開 (Defect Avoidance) 演算法。

## 專案功能
* **核心演算法**：最佳化非一刀切 (Non-Guillotine) 二維裝箱，並支援跳過指定座標的矩形瑕疵。
* **背景任務排程**：透過後端背景 Worker，防止複雜運算 (Timeout) 塞爆 API 伺服器，支援非同步進度查詢。
* **互動視覺化介面**：使用純 Vanilla JS 與 HTML5 Canvas，提供視覺化拖曳標記瑕疵、快速增刪產品數量與即時排版繪圖。
* **無界限模式 (Unbounded)**：支援設定每種產品的「最低產量 (Min Qty)」，也可勾選「無限數量」自動找出最高利用率的無限擴展組合。
* **結果匯出**：可一鍵匯出包含各產品座標尺寸的 `.csv` 報表供後續利用。

## 環境安裝與執行

本專案使用 `uv` 進行虛擬環境與相依套件管理：

1. **建立環境並安裝套件**：
   ```bash
   uv venv
   uv pip install fastapi uvicorn
   ```

2. **啟動伺服器**：
   ```bash
   uv run uvicorn src.server:app --reload
   ```

3. **開啟網頁版儀表板**：
   在瀏覽器中前往 [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 測試
執行並發與壓力測試（排隊機制驗證）：
```bash
uv run python -m unittest tests.test_stress
```
