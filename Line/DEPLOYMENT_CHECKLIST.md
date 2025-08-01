# Zeabur 部署檢查清單

## 📋 **部署前檢查**

### ✅ **程式碼準備**

- [x] 移除敏感資訊的硬編碼
- [x] 確認 `requirements.txt` 包含所有依賴
- [x] 檢查 `zeabur.json` 配置正確
- [x] 確認 `Procfile` 服務定義
- [x] 程式碼推送到 GitHub

### ✅ **Zeabur 專案設定**

1. **建立專案**

   - [ ] 在 Zeabur Dashboard 建立新專案
   - [ ] 連接 GitHub 儲存庫
   - [ ] 選擇正確的分支 (main)

2. **新增 MySQL 服務**

   - [ ] 點擊 "Add Service" → "MySQL"
   - [ ] 等待 MySQL 服務完全啟動
   - [ ] 記錄資料庫連線資訊

3. **設定環境變數**

   在專案的 "Variables" 頁面設定以下環境變數：

   ```bash
   # 必要環境變數
   MYSQL_HOST=<MySQL服務的內部主機名>
   MYSQL_USER=root
   MYSQL_PASSWORD=<MySQL密碼>
   MYSQL_DATABASE=zeabur
   LINE_CHANNEL_ACCESS_TOKEN=<您的LINE Token>

   # 可選環境變數
   PORT=8080
   ```

## 🚀 **部署流程**

### 步驟 1：程式碼部署

- [ ] 確認程式碼已推送到 GitHub
- [ ] 在 Zeabur 觸發重新部署

### 步驟 2：服務驗證

- [ ] 檢查 Web 服務狀態 (應顯示 "Running")
- [ ] 檢查 Scheduler 服務狀態 (應顯示 "Running")
- [ ] 檢查 MySQL 服務狀態 (應顯示 "Running")

### 步驟 3：功能測試

使用測試腳本驗證：

```bash
python test_health.py https://<your-project>.zeabur.app
```

預期結果：

```
🚀 開始測試 LINE 健康問卷系統
📍 目標網址: https://your-project.zeabur.app
⏰ 測試時間: 2024-...
--------------------------------------------------
🔍 測試健康檢查端點: https://your-project.zeabur.app/health
✅ 健康檢查通過
   狀態: healthy
   時間戳: 2024-...

🔍 測試問卷頁面: https://your-project.zeabur.app/survey
✅ 問卷頁面可正常存取

🔍 測試 API 端點...
✅ API 端點可用: /api/user/sync
✅ API 端點可用: /api/survey/submit
✅ API 端點測試完成

--------------------------------------------------
📊 測試結果: 3/3 通過
🎉 所有測試通過！系統運行正常
```

## 🔧 **LINE LIFF 設定**

### 設定步驟

1. [ ] 前往 [LINE Developers Console](https://developers.line.biz/)
2. [ ] 選擇您的 Channel
3. [ ] 進入 LIFF 設定頁面
4. [ ] 設定 Endpoint URL：
   ```
   https://<your-project>.zeabur.app/survey
   ```
5. [ ] 儲存設定並測試

## 🔍 **部署後檢查**

### 服務監控

- [ ] 檢查 Zeabur Dashboard 中的服務日誌
- [ ] 確認沒有錯誤訊息
- [ ] 監控服務資源使用情況

### 資料庫檢查

- [ ] 確認資料庫表結構正確建立
- [ ] 檢查 users 和 surveys 表是否存在
- [ ] 測試資料庫連線正常

### 功能驗證

- [ ] 透過 LINE 開啟 LIFF 頁面
- [ ] 測試使用者註冊流程
- [ ] 測試問卷填寫功能
- [ ] 檢查排程服務是否正常運行

## ⚠️ **常見問題處理**

### 1. 部署失敗

**檢查項目：**

- [ ] 環境變數是否完整設定
- [ ] MySQL 服務是否已啟動
- [ ] GitHub 程式碼是否最新

### 2. 資料庫連線失敗

**檢查項目：**

- [ ] MySQL 主機名是否正確
- [ ] 密碼是否設定正確
- [ ] 網路連線是否正常

### 3. LINE Bot 無法發送訊息

**檢查項目：**

- [ ] LINE_CHANNEL_ACCESS_TOKEN 是否正確
- [ ] Token 權限是否足夠
- [ ] LINE Developers Console 設定是否正確

### 4. 排程任務未執行

**檢查項目：**

- [ ] Scheduler 服務是否正常運行
- [ ] 時區設定是否正確 (Asia/Taipei)
- [ ] 資料庫中是否有活躍使用者

## 📞 **支援資源**

- [Zeabur 官方文件](https://zeabur.com/docs)
- [LINE Developers Console](https://developers.line.biz/)
- [專案 GitHub 儲存庫](https://github.com/your-username/your-repo)

## ✅ **部署完成確認**

部署成功的標誌：

- [ ] 所有服務狀態為 "Running"
- [ ] 健康檢查端點返回 200 狀態
- [ ] LINE LIFF 可以正常開啟問卷頁面
- [ ] 問卷提交功能正常
- [ ] 排程服務日誌正常

**🎉 恭喜！您的 LINE 健康問卷系統已成功部署到 Zeabur！**
