# Docker 容器化部署指南

## 專案架構

此專案使用 Docker Compose 來管理多個容器服務：

- **mysql**: MySQL 8.0 資料庫服務
- **web**: Flask Web 應用服務 (PORT: 8080)
- **scheduler**: 排程和提醒服務

## 快速啟動

### 1. 準備環境變數

```bash
# 複製環境變數範例檔案
cp .env.docker .env

# 編輯 .env 檔案，填入您的 LINE Channel Access Token
nano .env
```

### 2. 啟動所有服務

```bash
# 在 Line/ 目錄下執行
docker-compose up -d
```

### 3. 檢查服務狀態

```bash
# 查看所有容器狀態
docker-compose ps

# 查看服務日誌
docker-compose logs -f web
docker-compose logs -f scheduler
docker-compose logs -f mysql
```

### 4. 驗證部署

```bash
# 測試健康檢查端點
curl http://localhost:8080/health

# 測試問卷頁面
curl http://localhost:8080/survey
```

## 詳細操作指令

### 容器管理

```bash
# 啟動服務 (背景模式)
docker-compose up -d

# 啟動服務 (前景模式，查看即時日誌)
docker-compose up

# 停止服務
docker-compose down

# 停止服務並刪除 volumes (會清除資料庫資料)
docker-compose down -v

# 重新建構映像檔
docker-compose build

# 重新建構並啟動
docker-compose up --build -d
```

### 日誌查看

```bash
# 查看所有服務日誌
docker-compose logs

# 查看特定服務日誌
docker-compose logs web
docker-compose logs scheduler
docker-compose logs mysql

# 即時跟蹤日誌
docker-compose logs -f web
```

### 除錯和維護

```bash
# 進入 web 容器
docker-compose exec web bash

# 進入 scheduler 容器
docker-compose exec scheduler bash

# 進入 MySQL 容器
docker-compose exec mysql mysql -u root -p

# 重啟特定服務
docker-compose restart web
docker-compose restart scheduler
```

## 服務端點

啟動成功後，可存取以下端點：

- **Web 應用**: http://localhost:8080
- **健康檢查**: http://localhost:8080/health
- **問卷頁面**: http://localhost:8080/survey
- **MySQL 資料庫**: localhost:3306

## 環境變數說明

| 變數名稱                    | 預設值   | 說明                          |
| --------------------------- | -------- | ----------------------------- |
| `MYSQL_USER`                | root     | MySQL 使用者名稱              |
| `MYSQL_PASSWORD`            | admin123 | MySQL 密碼                    |
| `MYSQL_DATABASE`            | zeabur   | 資料庫名稱                    |
| `LINE_CHANNEL_ACCESS_TOKEN` | (必填)   | LINE Bot Channel Access Token |

## 資料持久化

- MySQL 資料儲存在 Docker Volume `mysql_data` 中
- 即使容器重啟，資料庫資料也會保持

## 故障排除

### 常見問題

1. **容器啟動失敗**

   ```bash
   # 檢查容器狀態
   docker-compose ps

   # 查看錯誤日誌
   docker-compose logs [service_name]
   ```

2. **資料庫連線失敗**

   ```bash
   # 確認 MySQL 容器健康狀態
   docker-compose exec mysql mysqladmin ping -h localhost

   # 檢查網路連線
   docker-compose exec web ping mysql
   ```

3. **端口衝突**

   - 修改 docker-compose.yml 中的端口映射
   - 確保 8080 和 3306 端口未被其他服務占用

4. **權限問題**

   ```bash
   # 給予執行權限
   chmod +x Line/test_health.py

   # 檢查檔案權限
   ls -la Line/
   ```

### 清理和重置

```bash
# 完全清理 (刪除容器、映像檔、網路、volumes)
docker-compose down -v --rmi all

# 清理未使用的 Docker 資源
docker system prune -a
```

## 生產環境注意事項

1. **安全性**

   - 修改預設的資料庫密碼
   - 使用 Docker Secrets 管理敏感資訊
   - 限制對外暴露的端口

2. **效能調優**

   - 調整 gunicorn workers 數量
   - 配置 MySQL 記憶體設定
   - 使用外部負載平衡器

3. **監控和日誌**
   - 整合日誌收集系統
   - 設定健康檢查警報
   - 監控資源使用情況
