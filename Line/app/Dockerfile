# 使用官方的 Python 3.10 slim 映像檔作為基礎
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt
COPY ../requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式檔案
COPY . .
COPY ../survey.html .

# 暴露端口
EXPOSE 8080

# 設定環境變數
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 啟動命令
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]