# 🚀 簡化部署指南

## ✨ **配置優化**

我們已經簡化了 Zeabur 部署配置，移除了重複的配置文件：

### ❌ **已移除的重複文件**

- `env.json` - 功能與 Procfile 重複
- `zeabur.json` - 功能與 Procfile 重複

### ✅ **保留的核心文件**

- `Procfile` - 標準且通用的進程定義
- `requirements.txt` - Python 依賴定義
- `.env.example` - 環境變數範例

## 📋 **極簡部署步驟**

### 1. 推送程式碼

```bash
git add .
git commit -m "簡化 Zeabur 配置"
git push origin main
```

### 2. Zeabur 自動檢測

Zeabur 會自動：

- 檢測 Python 專案（通過 `requirements.txt`）
- 讀取 `Procfile` 定義的服務
- 建立 `web` 和 `worker` 服務

### 3. 設定環境變數

在 Zeabur Variables 頁面設定：

```bash
MYSQL_HOST=mysql.zeabur.internal
MYSQL_USER=root
MYSQL_PASSWORD=<你的密碼>
MYSQL_DATABASE=zeabur
LINE_CHANNEL_ACCESS_TOKEN=<你的Token>
```

### 4. 新增 MySQL 服務

- 在 Zeabur 專案中點擊 "Add Service"
- 選擇 "MySQL"
- 等待啟動完成

## 🎯 **優化效果**

### 簡化前 (3 個配置文件)

```
📁 配置文件
├── Procfile      ✅ 定義服務
├── env.json      ❌ 重複定義服務
└── zeabur.json   ❌ 重複定義服務
```

### 簡化後 (1 個配置文件)

```
📁 配置文件
└── Procfile      ✅ 唯一服務定義
```

## 📊 **優勢**

1. **更簡潔** - 只需維護一個配置文件
2. **更標準** - 使用業界標準 Procfile 格式
3. **更通用** - 兼容 Heroku、Zeabur、AWS 等平台
4. **更清晰** - 避免配置衝突和混淆
5. **更易維護** - 單一配置源，降低維護成本

## ⚠️ **注意事項**

- 原有的 `env.json` 和 `zeabur.json` 已備份到 `config_backup/` 目錄
- 如需復原，可以從備份目錄恢復文件
- 新配置已在多個文檔平台測試驗證

## 🧪 **測試部署**

使用測試腳本驗證：

```bash
python test_health.py https://your-project.zeabur.app
```

預期看到：

```
🎉 所有測試通過！系統運行正常
```

---

**🎊 恭喜！現在你的 LINE 健康問卷系統使用了最佳實踐的極簡配置！**
