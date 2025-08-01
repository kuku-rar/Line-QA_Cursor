# 🔧 Zeabur 環境變數設置指南

## 📊 **根據您的 MySQL 設置**

根據您提供的 MySQL 連線資訊，以下是需要在 Zeabur 中設置的環境變數：

### 🗄️ **MySQL 資料庫環境變數**

在 Zeabur Dashboard 的 **Web 服務** Variables 頁面新增：

```bash
# MySQL 資料庫設定
MYSQL_HOST=tpe1.clusters.zeabur.com
MYSQL_PORT=30982
MYSQL_USER=root
MYSQL_PASSWORD=MT2zP4VbW1nlIc7tLy89U6q35C0Hfoi
MYSQL_DATABASE=zeabur

# LINE Bot 設定 (請替換為您的實際 Token)
LINE_CHANNEL_ACCESS_TOKEN=你的LINE_CHANNEL_ACCESS_TOKEN
```

### 🔄 **Worker 服務環境變數**

在 Zeabur Dashboard 的 **Worker 服務** Variables 頁面新增：

```bash
# MySQL 資料庫設定 (與 Web 服務相同)
MYSQL_HOST=tpe1.clusters.zeabur.com
MYSQL_PORT=30982
MYSQL_USER=root
MYSQL_PASSWORD=MT2zP4VbW1nlIc7tLy89U6q35C0Hfoi
MYSQL_DATABASE=zeabur

# LINE Bot 設定 (與 Web 服務相同)
LINE_CHANNEL_ACCESS_TOKEN=你的LINE_CHANNEL_ACCESS_TOKEN
```

## 🎯 **設置步驟**

### 步驟 1：進入 Web 服務設定

1. 在 Zeabur Dashboard 點擊您的 **Web 服務**
2. 切換到 **"Variables"** 頁籤
3. 點擊 **"Add Variable"**

### 步驟 2：逐一新增環境變數

對於每個環境變數：

1. **Name**: 輸入變數名稱 (如：`MYSQL_HOST`)
2. **Value**: 輸入對應的值 (如：`tpe1.clusters.zeabur.com`)
3. 點擊 **"Add"** 確認

### 步驟 3：重複設置 Worker 服務

對 Worker 服務重複相同的步驟

## ✅ **驗證設置**

### 確認清單：

- [ ] Web 服務包含所有 6 個環境變數
- [ ] Worker 服務包含所有 6 個環境變數
- [ ] LINE_CHANNEL_ACCESS_TOKEN 已設為您的實際 Token
- [ ] 密碼複製正確，無額外空格

### 測試連線：

```bash
# 部署完成後測試
curl https://your-project.zeabur.app/health

# 預期回應
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-..."
}
```

## 🚀 **部署**

設置完環境變數後：

```bash
git add .
git commit -m "根據 MySQL 設置更新資料庫配置"
git push origin main
```

## 🔍 **故障排除**

### 如果仍然出現 "App failed to load"：

1. **檢查環境變數拼寫**

   - 確保變數名稱完全正確
   - 確保沒有多餘的空格

2. **檢查 MySQL 連線**

   - 確認 MySQL 服務正在運行
   - 確認網路連線正常

3. **檢查服務日誌**
   - 在 Zeabur Dashboard 查看詳細錯誤訊息
   - 尋找具體的錯誤原因

## 📋 **完整環境變數清單**

### Web 服務：

```
MYSQL_HOST=tpe1.clusters.zeabur.com
MYSQL_PORT=30982
MYSQL_USER=root
MYSQL_PASSWORD=MT2zP4VbW1nlIc7tLy89U6q35C0Hfoi
MYSQL_DATABASE=zeabur
LINE_CHANNEL_ACCESS_TOKEN=<您的實際Token>
```

### Worker 服務：

```
MYSQL_HOST=tpe1.clusters.zeabur.com
MYSQL_PORT=30982
MYSQL_USER=root
MYSQL_PASSWORD=MT2zP4VbW1nlIc7tLy89U6q35C0Hfoi
MYSQL_DATABASE=zeabur
LINE_CHANNEL_ACCESS_TOKEN=<您的實際Token>
```

---

**💡 重要：請確保 LINE_CHANNEL_ACCESS_TOKEN 替換為您的實際 LINE Bot Token！**
