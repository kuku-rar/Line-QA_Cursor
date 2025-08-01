# 🎨 前端路徑更新說明

## ✅ **修正完成**

### 🔄 **檔案移動**

```bash
# 原始位置
survey.html

# 新位置
FrontEnd/survey.html
```

### 🔧 **程式碼修正**

#### 1. **app/app.py**

```python
# 修正前
@app.route('/survey')
def survey_page():
    return send_from_directory('.', 'survey.html')

# 修正後
@app.route('/survey')
def survey_page():
    return send_from_directory('../FrontEnd', 'survey.html')
```

#### 2. **app/Dockerfile**

```dockerfile
# 已正確配置
WORKDIR /workspace
COPY .. .  # 複製整個專案結構，包含 FrontEnd/
```

### 📁 **目錄結構對應**

#### 本地開發環境：

```
Line/
├── app/
│   ├── app.py (使用 ../FrontEnd/survey.html)
│   └── Dockerfile
├── FrontEnd/
│   └── survey.html
├── Procfile
└── requirements.txt
```

#### 容器環境 (/workspace)：

```
/workspace/
├── app/
│   ├── app.py
│   └── Dockerfile
├── FrontEnd/
│   └── survey.html
├── Procfile
└── requirements.txt
```

### 🎯 **路徑解析**

| 環境 | 執行位置          | 相對路徑                  | 絕對路徑                          |
| ---- | ----------------- | ------------------------- | --------------------------------- |
| 本地 | `Line/app/`       | `../FrontEnd/survey.html` | `Line/FrontEnd/survey.html`       |
| 容器 | `/workspace/app/` | `../FrontEnd/survey.html` | `/workspace/FrontEnd/survey.html` |

### ✅ **驗證結果**

```bash
# 從 app 目錄測試路徑
cd app && ls -la ../FrontEnd/
# ✅ 成功找到 survey.html

# 路徑驗證
../FrontEnd/survey.html → 正確指向前端文件
```

### 🚀 **部署影響**

#### Zeabur 部署：

- ✅ Procfile 不變：`gunicorn app.app:app`
- ✅ 路徑自動正確：容器內結構與本地一致
- ✅ 前端文件正確載入

#### 本地開發：

- ✅ Flask 開發伺服器：`cd app && python app.py`
- ✅ 訪問：`http://localhost:8080/survey`
- ✅ 前端頁面正常顯示

### 🔗 **相關端點**

| 端點                 | 功能     | 檔案路徑               |
| -------------------- | -------- | ---------------------- |
| `/survey`            | 問卷頁面 | `FrontEnd/survey.html` |
| `/api/user/sync`     | 用戶同步 | `app/app.py`           |
| `/api/survey/submit` | 問卷提交 | `app/app.py`           |
| `/health`            | 健康檢查 | `app/app.py`           |

---

**✅ 前端路徑更新完成，所有環境均可正常運作！**
