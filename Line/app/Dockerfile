# 使用官方的 Python 3.10 slim 映像檔作為基礎
FROM python:3.10-slim

# 設定工作目錄為根目錄，與 Procfile 一致
WORKDIR /workspace

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt
COPY ../requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個專案結構
COPY .. .

# 暴露端口 (使用環境變數)
EXPOSE $PORT
EXPOSE 8080

# 設定環境變數
ENV FLASK_APP=app.app:app
ENV FLASK_ENV=production

# 啟動命令 (與 Procfile 一致)
CMD ["sh", "-c", "gunicorn app.app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300"]