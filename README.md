# LINE 健康問卷追蹤系統

這是一個透過 LINE LIFF 頁面，讓使用者定時回報每日健康狀況的問卷追蹤系統。系統會自動建立每日問卷、接收使用者提交的資料，並在指定時間自動發送提醒給尚未填寫的使用者。

本專案使用 Flask 作為後端框架，並設計為可輕鬆部署於 Zeabur 平台。

---

## 功能特色

- **每日三時段問卷**：使用者需於 10:00、13:00、17:00 透過 LIFF 頁面填寫健康問卷。
- **自動預建記錄**：每日 00:00，系統會為所有有效會員自動建立當日的三份空白問卷。
- **即時填寫更新**：使用者透過 LIFF 頁面提交問卷時，系統會即時更新對應的資料庫記錄。
- **自動漏填提醒**：每日 20:00，系統會檢查當日問卷是否有缺漏，並透過 LINE Bot 發送一對一提醒訊息。
- **健康檢查端點**：提供 `/health` 端點供 Zeabur 監控服務狀態。
- **多服務架構**：分離 Web 服務和排程服務，確保穩定性和可擴展性。

---

## 技術棧

- **後端**: Python 3.8+, Flask
- **資料庫**: MySQL 8.0+ (使用 `pymysql` 連接)
- **排程任務**: `apscheduler` (支援 Cron 格式)
- **部署伺服器**: `gunicorn` (WSGI 服務器)
- **部署平台**: Zeabur (支援多服務部署)
- **時區處理**: `zoneinfo` (Asia/Taipei)
- **LINE 整合**: LINE Messaging API, LIFF 2.0

---

## 資料庫設計

系統包含 `users` (使用者) 和 `surveys` (問卷記錄) 兩張資料表。

### `users` Table

儲存已註冊的使用者基本資料。

```sql
CREATE TABLE users (
  id          INT          PRIMARY KEY AUTO_INCREMENT,
  lineId      VARCHAR(255) UNIQUE NOT NULL,
  name        VARCHAR(255) NOT NULL,
  gender      ENUM('male','female','other') NULL,
  birthday    DATE         NULL,
  age         INT          NULL,
  is_active   BOOLEAN      DEFAULT TRUE,
  created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_lineId (lineId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### `surveys` Table

記錄每日各時段的問卷填寫狀況。

```sql
CREATE TABLE surveys (
  id           INT         PRIMARY KEY AUTO_INCREMENT,
  user_id      INT         NOT NULL,
  survey_date  DATE        NOT NULL,
  slot         ENUM('10:00','13:00','17:00') NOT NULL,
  q1           ENUM('V','X') NULL,
  q2           ENUM('V','X') NULL,
  q3           ENUM('V','X') NULL,
  q4           ENUM('V','X') NULL,
  remark       TEXT        NULL,
  submitted_at TIMESTAMP   NULL,
  created_at   TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP   DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY unique_survey (user_id, survey_date, slot),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

## 本地端設定與啟動

1.  **複製專案**

    ```bash
    git clone https://github.com/kuku_rar/Line-QA_Cursor.git
    cd Line-QA_Cursor/Line
    ```

2.  **建立虛擬環境並安裝依賴**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **設定資料庫**

    - 確保您有一個正在運行的 MySQL 伺服器。
    - 建立一個資料庫 (例如 `line_survey_db`)。
    - 建立一個使用者 (例如 `survey_user`) 並授予權限。
    - 系統會自動建立和更新資料表結構，無需手動建立。

4.  **設定環境變數**
    複製環境變數範例檔案並編輯：

    ```bash
    cp .env.example .env
    # 編輯 .env 檔案，填入您的資料庫連線資訊和 LINE Channel Access Token
    ```

5.  **啟動服務**

    - **啟動 Web 伺服器**:
      ```bash
      cd app
      python app.py
      ```
    - **啟動排程器** (開啟另一個終端機):
      ```bash
      cd scheduler
      python scheduler.py
      ```

6.  **驗證服務**
    - Web 服務健康檢查: `http://localhost:8080/health`
    - LIFF 頁面: `http://localhost:8080/survey`

---

## Zeabur 部署指南

### 快速部署

1.  **推送程式碼**:

    ```bash
    git add .
    git commit -m "準備部署到 Zeabur"
    git push origin main
    ```

2.  **在 Zeabur 建立專案**:

    - 登入 [Zeabur](https://zeabur.com)
    - 建立新專案並連結 GitHub 儲存庫
    - Zeabur 會自動偵測 `Procfile` 並建立 `web` 和 `worker` 服務

3.  **新增 MySQL 服務**:

    - 在專案中新增 MySQL 服務
    - 等待服務啟動完成

4.  **設定環境變數**:

    ```bash
    # 必要環境變數
    MYSQL_HOST=mysql.zeabur.internal
    MYSQL_USER=root
    MYSQL_PASSWORD=<您的資料庫密碼>
    MYSQL_DATABASE=zeabur
    LINE_CHANNEL_ACCESS_TOKEN=<您的 LINE Channel Access Token>
    ```

5.  **設定 LINE LIFF**:
    - LIFF URL: `https://<your-project>.zeabur.app/survey`
    - 健康檢查: `https://<your-project>.zeabur.app/health`

### 詳細部署指南

請參閱 [DEPLOYMENT.md](Line/DEPLOYMENT.md) 獲取完整的部署說明、故障排除和驗證方法。
