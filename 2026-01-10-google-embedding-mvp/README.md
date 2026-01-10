# Google Embedding MVP

這是一個使用 Google Generative AI (Gemini) API 進行文字嵌入 (Embedding) 的最小可行性產品 (MVP)。此版本包含一個 Streamlit 網頁應用程式，支援上傳文件與圖片。

## 功能

- **Streamlit 介面**：簡單易用的網頁介面。
- **支援多種格式**：
    - **文字 (.txt, .md)**：直接讀取並嵌入。
    - **PDF (.pdf)**：自動擷取文字內容並嵌入。
    - **圖片 (.jpg, .png)**：使用 Gemini 1.5 Flash 模型生成圖片描述，再將描述轉換為嵌入向量 (Embedding)。
- **嵌入模型**：預設使用 `text-embedding-004`。

## 安裝

1. 確保已安裝 Python 3.9+

2. 安裝相依套件：

   ```bash
   pip install -r requirements.txt
   ```

## 設定

你需要一個 Google API Key。

1. 在專案目錄下建立 `.env` 檔案
2. 加入以下內容：

   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

   或者，你也可以直接在應用程式介面上輸入 API Key。

## 執行應用程式

執行 Streamlit 應用程式：

```bash
streamlit run app.py
```

這將會在你的瀏覽器中開啟應用程式 (通常是 http://localhost:8501)。

## 專案結構

- `app.py`: Streamlit 主程式。
- `utils.py`: 處理檔案讀取、圖片描述生成與嵌入的邏輯。
- `requirements.txt`: 專案依賴套件列表。
- `test_utils.py`: 用於測試 `utils.py` 邏輯的單元測試。

## 注意事項

- 本專案使用 `google-generativeai` 函式庫。
- 圖片嵌入是透過「圖片 -> 文字描述 -> 嵌入」的方式間接實現的，因為標準 Text Embedding 模型不直接支援圖片輸入。
