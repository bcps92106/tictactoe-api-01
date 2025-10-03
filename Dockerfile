# 使用 Python 3.10 slim 版本作為基底
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統層級依賴 (ffmpeg 給 whisper 用，git 給 transformers/datasets 用)
RUN apt-get update && apt-get install -y ffmpeg git build-essential \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt 並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# 複製專案所有檔案
COPY . .

# 開放 FastAPI (8000) 和 Gradio (7860) 兩個 port
EXPOSE 8000
EXPOSE 7860

# 啟動 FastAPI API
CMD uvicorn app.api.app:app --host 0.0.0.0 --port ${PORT:-8000}