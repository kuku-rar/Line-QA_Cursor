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

# 複製排程器主程式
COPY . .

# 設定環境變數
ENV PYTHONUNBUFFERED=1

# 啟動命令
CMD ["python", "scheduler.py"]