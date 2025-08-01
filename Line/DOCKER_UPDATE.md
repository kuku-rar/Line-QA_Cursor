# 🐳 Docker 配置更新說明

## ✅ **Dockerfile 修正完成**

### 🔧 **修正項目**

1. **工作目錄統一**

   ```dockerfile
   # 修正前
   WORKDIR /app

   # 修正後
   WORKDIR /workspace
   ```

2. **文件複製優化**

   ```dockerfile
   # 修正前
   COPY . .
   COPY ../survey.html .

   # 修正後
   COPY .. .  # 複製整個專案結構
   ```

3. **啟動命令統一**

   ```dockerfile
   # 修正前
   CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]

   # 修正後
   CMD ["sh", "-c", "gunicorn app.app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300"]
   ```

4. **端口配置優化**
   ```dockerfile
   # 新增環境變數支援
   EXPOSE $PORT
   EXPOSE 8080
   ```

### 🎯 **與 Procfile 保持一致**

| 配置項目 | Procfile      | Dockerfile    |
| -------- | ------------- | ------------- |
| 模組路徑 | `app.app:app` | `app.app:app` |
| Workers  | 1             | 1             |
| Timeout  | 300           | 300           |
| 端口     | `$PORT`       | `$PORT`       |

### 📁 **容器內目錄結構**

```
/workspace/
├── app/
│   ├── __init__.py
│   ├── app.py
│   └── Dockerfile
├── scheduler/
│   ├── scheduler.py
│   └── Dockerfile
├── survey.html
├── requirements.txt
├── Procfile
└── ...
```

### 🚀 **測試 Docker 部署**

#### 本地測試：

```bash
# 在 Line/ 目錄下執行
docker build -f app/Dockerfile -t line-survey-app .
docker run -p 8080:8080 --env-file .env line-survey-app
```

#### Docker Compose 測試：

```bash
docker-compose up -d
```

### 🔗 **與 Zeabur 部署的關係**

- **Zeabur 部署**：使用 `Procfile`（主要方式）
- **Docker 部署**：使用 `Dockerfile`（本地開發/其他平台）
- **配置同步**：兩者保持一致的啟動參數

---

**✅ 現在 Dockerfile 與 Procfile 完全同步，支援多種部署方式！**
