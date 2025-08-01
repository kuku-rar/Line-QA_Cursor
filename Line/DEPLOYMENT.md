# Zeabur 部署指南

## 專案架構

此專案包含兩個主要服務：

- **Web 服務**: Flask 應用程式 (`app/app.py`)
- **排程服務**: 問卷建立和提醒功能 (`scheduler/scheduler.py`)

## 環境變數清單

在 Zeabur 專案的 "Variables" 頁面，需要設定以下環境變數：

### 必要環境變數

```bash
# MySQL 資料庫設定
MYSQL_HOST=mysql.zeabur.internal
MYSQL_USER=root
MYSQL_PASSWORD=<您的資料庫密碼>
MYSQL_DATABASE=zeabur

# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN=<您的 LINE Channel Access Token>
```

### 可選環境變數

```bash
# Web 服務埠號 (通常由 Zeabur 自動設定)
PORT=8080
```

## 部署步驟

### 1. 準備 GitHub 儲存庫

```bash
git add .
git commit -m "準備部署到 Zeabur"
git push origin main
```

### 2. 在 Zeabur 建立專案

1. 登入 [Zeabur Dashboard](https://zeabur.com)
2. 點擊 "New Project"
3. 選擇 "Import from GitHub"
4. 選擇此儲存庫

### 3. 配置服務

Zeabur 會根據 `Procfile` 自動建立以下服務：

- **web**: 主要的 Flask 應用程式
- **worker**: 排程和提醒服務

### 4. 新增 MySQL 服務

1. 在專案中點擊 "Add Service"
2. 選擇 "MySQL"
3. 等待服務啟動完成

### 5. 設定環境變數

在專案的 "Variables" 頁面新增所有必要的環境變數。

### 6. 取得應用程式 URL

部署完成後，您的應用程式將可在以下網址存取：

```
https://<your-project>.zeabur.app
```

### 7. 設定 LINE LIFF

1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 選擇您的 Channel
3. 在 LIFF 設定中，將 Endpoint URL 設為：
   ```
   https://<your-project>.zeabur.app/survey
   ```

## 驗證部署

### 檢查 Web 服務

訪問健康檢查端點：

```
https://<your-project>.zeabur.app/health
```

應該回傳：

```json
{
  "status": "healthy",
  "timestamp": "2024-..."
}
```

### 檢查排程服務

在 Zeabur 的服務日誌中應該看到：

```
🚀 排程服務已啟動:
   - 每日 00:00 自動建立問卷記錄
   - 每日 20:00 發送提醒訊息
```

## 故障排除

### 常見問題

1. **資料庫連線失敗**

   - 確認 MySQL 服務已啟動
   - 檢查環境變數是否正確設定

2. **LINE Bot 無法發送訊息**

   - 確認 `LINE_CHANNEL_ACCESS_TOKEN` 是否正確
   - 檢查 Token 是否有正確的權限

3. **排程任務未執行**
   - 檢查 worker 服務是否正常運行
   - 確認時區設定 (Asia/Taipei)

### 日誌查看

在 Zeabur Dashboard 的服務頁面中，可以查看即時日誌來診斷問題。

## 手動測試

如需手動觸發排程任務進行測試，可以在 scheduler.py 中取消相關註解：

```python
# 取消註解以立即測試
create_daily_surveys()
remind_users()
```
