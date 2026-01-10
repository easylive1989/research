# Google Embedding MVP

這是一個使用 Google Generative AI (Gemini) API 進行文字嵌入 (Embedding) 的最小可行性產品 (MVP)。

## 功能

- 連接 Google Generative AI API
- 使用 `text-embedding-004` 模型
- 將範例文字轉換為向量 (Embedding)

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

## 執行

執行 Python 腳本：

```bash
python embedding_demo.py
```

如果設定正確，你將看到生成的嵌入向量資訊。
