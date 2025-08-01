# LINE 健康問卷系統

這是一個基於 LINE Bot 的健康問卷系統，支援定時提醒和問卷填寫功能。

## 🌟 **主要功能**

- **LINE LIFF 問卷填寫**：透過 LINE App 填寫每日健康問卷
- **自動排程**：每日自動建立問卷記錄，每晚提醒未完成使用者
- **資料管理**：使用 MySQL 資料庫儲存使用者資料和問卷結果
- **健康檢查**：提供服務狀態監控端點

## 🚀 **快速開始**

### 本地開發

1. **安裝依賴**

   ```bash
   pip install -r requirements.txt
   ```

2. **設定環境變數**

   ```bash
   cp .env.example .env
   # 編輯 .env 檔案，填入您的配置
   ```

3. **啟動服務**

   ```bash
   # 啟動 Web 服務
   cd app && python app.py

   # 啟動排程服務 (另一個終端)
   cd scheduler && python scheduler.py
   ```

### Docker 部署

使用 Docker Compose 快速啟動完整系統：

```bash
docker-compose up -d
```

詳見 [Docker 部署指南](DOCKER_DEPLOYMENT.md)

### Zeabur 雲端部署

**推薦的生產環境部署方式**

```bash
git push origin main
# 然後在 Zeabur Dashboard 匯入此儲存庫
```

詳見 [Zeabur 部署指南](ZEABUR_DEPLOYMENT.md)

## 🔧 **環境變數設定**

| 變數名稱                    | 必要 | 說明                          |
| --------------------------- | ---- | ----------------------------- |
| `MYSQL_HOST`                | ✅   | MySQL 主機位址                |
| `MYSQL_USER`                | ✅   | MySQL 使用者名稱              |
| `MYSQL_PASSWORD`            | ✅   | MySQL 密碼                    |
| `MYSQL_DATABASE`            | ✅   | 資料庫名稱                    |
| `LINE_CHANNEL_ACCESS_TOKEN` | ✅   | LINE Bot Channel Access Token |
| `PORT`                      | ❌   | Web 服務埠號 (預設：8080)     |

## 📋 **系統架構**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LINE LIFF     │    │   Flask Web     │    │   MySQL DB      │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│   (Storage)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Scheduler     │
                       │   (Worker)      │
                       └─────────────────┘
```

### 服務說明

- **Web 服務**：Flask 應用程式，提供 API 和靜態檔案
- **Scheduler 服務**：背景排程服務，處理定時任務
- **MySQL 資料庫**：儲存使用者和問卷資料

## 🧪 **測試**

使用內建的健康檢查腳本：

```bash
# 測試本地服務
python test_health.py http://localhost:8080

# 測試線上服務
python test_health.py https://your-project.zeabur.app
```

## 📁 **專案結構**

```
Line/
├── app/                    # Flask Web 應用
│   ├── app.py             # 主要應用程式
│   └── Dockerfile         # Web 服務 Docker 配置
├── scheduler/             # 排程服務
│   ├── scheduler.py       # 排程主程式
│   ├── Dockerfile         # Scheduler 服務 Docker 配置
│   └── zeabur.json       # Scheduler 專用 Zeabur 配置
├── survey.html           # 問卷前端頁面
├── requirements.txt      # Python 依賴
├── Procfile             # Zeabur/Heroku 進程配置
├── docker-compose.yml   # Docker Compose 配置
├── test_health.py       # 健康檢查腳本
├── .env.example         # 環境變數範例
└── README.md           # 本檔案
```

## 🔒 **安全性**

- 🚫 **絕不在程式碼中硬編碼敏感資訊**
- 🔐 **使用環境變數管理機密配置**
- 🛡️ **定期更新依賴包避免安全漏洞**
- 📊 **監控服務狀態和異常日誌**

## 📚 **API 文件**

### 健康檢查

```
GET /health
```

### 使用者同步

```
POST /api/user/sync
Content-Type: application/json

{
  "lineId": "使用者LINE ID",
  "name": "使用者姓名"
}
```

### 問卷提交

```
POST /api/survey/submit
Content-Type: application/json

{
  "lineId": "使用者LINE ID",
  "slot": "10:00|13:00|17:00",
  "q1": "V|X",
  "q2": "V|X",
  "q3": "V|X",
  "q4": "V|X",
  "remark": "備註 (選填)"
}
```

## 🆘 **故障排除**

### 常見問題

1. **資料庫連線失敗**

   - 檢查 MySQL 服務狀態
   - 驗證環境變數設定
   - 確認網路連線

2. **LINE Bot 無法發送訊息**

   - 驗證 `LINE_CHANNEL_ACCESS_TOKEN`
   - 檢查 LINE Developers Console 設定

3. **排程任務未執行**
   - 檢查 Scheduler 服務日誌
   - 確認時區設定 (Asia/Taipei)

## 🤝 **貢獻**

歡迎提交 Issue 和 Pull Request 來改善此專案！

## 📄 **授權**

此專案採用 MIT 授權條款。
