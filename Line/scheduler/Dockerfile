# 使用官方的 Python 3.10 slim 映像檔作為基礎
FROM python:3.10-slim

# 在容器中設定工作目錄
WORKDIR /app

# 複製函式庫需求清單到容器中
COPY requirements.txt .

# 安裝所有必要的 Python 函式庫
RUN pip install --no-cache-dir -r requirements.txt

# 複製排程器主程式到容器中
COPY scheduler.py .

# 注意：這裡不需要 CMD 或 ENTRYPOINT，因為執行的指令將由 zeabur.json 提供