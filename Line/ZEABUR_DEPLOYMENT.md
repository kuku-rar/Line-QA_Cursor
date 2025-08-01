# Zeabur 部署指南 (更新版)

## 🚀 **快速部署步驟**

### 1. 準備 GitHub 儲存庫

```bash
git add .
git commit -m "優化 Zeabur 部署配置"
git push origin main
```

### 2. 在 Zeabur 建立專案

1. 登入 [Zeabur Dashboard](https://zeabur.com)
2. 點擊 "New Project"
3. 選擇 "Import from GitHub"
4. 選擇此儲存庫

### 3. 設定 MySQL 服務

1. 在專案中點擊 "Add Service"
2. 選擇 "MySQL"
3. 等待服務啟動完成
4. 記錄 MySQL 的連線資訊

### 4. 設定環境變數

在專案的 "Variables" 頁面新增以下環境變數：

#### 必要環境變數

```bash
# MySQL 資料庫設定
MYSQL_HOST=<你的 MySQL 主機>        # 例如：mysql.zeabur.internal
MYSQL_USER=root
MYSQL_PASSWORD=<你的資料庫密碼>
MYSQL_DATABASE=zeabur

# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN=<你的 LINE Channel Access Token>
```

#### 可選環境變數

```bash
# Web 服務埠號 (通常由 Zeabur 自動設定)
PORT=8080
```

### 5. 部署服務

Zeabur 會自動偵測 `Procfile` 並建立以下服務：

- **web**: 主要的 Flask 應用程式 (埠號：8080)
- **scheduler**: 排程和提醒服務 (背景工作者)

### 6. 驗證部署

#### 檢查 Web 服務

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

#### 檢查排程服務

在 Zeabur 的服務日誌中應該看到：

```
🚀 排程服務已啟動:
   - 每日 00:00 自動建立問卷記錄
   - 每日 20:00 發送提醒訊息
```

### 7. 設定 LINE LIFF

1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 選擇您的 Channel
3. 在 LIFF 設定中，將 Endpoint URL 設為：
   ```
   https://<your-project>.zeabur.app/survey
   ```

## 🔧 **進階設定**

### 自訂域名

在 Zeabur 專案設定中可以綁定自訂域名，提升專業度。

### 監控和日誌

- 在 Zeabur Dashboard 中可以即時查看服務日誌
- 建議定期檢查 health 端點確保服務正常

### 安全性

- 絕不在程式碼中硬編碼敏感資訊
- 使用 Zeabur 的環境變數管理功能
- 定期更新依賴包

## ⚠️ **常見問題**

### 1. 資料庫連線失敗

**檢查項目：**

- MySQL 服務是否已啟動
- 環境變數 `MYSQL_*` 是否正確設定
- 網路連線是否正常

### 2. LINE Bot 無法發送訊息

**檢查項目：**

- `LINE_CHANNEL_ACCESS_TOKEN` 是否正確
- Token 是否有正確的權限
- LINE Developers Console 設定是否正確

### 3. 排程任務未執行

**檢查項目：**

- Scheduler 服務是否正常運行
- 時區設定是否正確 (Asia/Taipei)
- 資料庫中是否有活躍使用者

### 4. 服務無法啟動

**檢查項目：**

- 依賴包是否正確安裝
- 環境變數是否齊全
- 檢查服務日誌中的錯誤訊息

## 📞 **支援**

如遇到部署問題，可以：

1. 檢查 Zeabur Dashboard 的服務日誌
2. 使用 `test_health.py` 腳本測試服務狀態
3. 查看本文件的故障排除章節
