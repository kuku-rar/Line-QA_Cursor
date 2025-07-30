# LINE 健康問卷追蹤系統

這是一個透過 LINE LIFF 頁面，讓使用者定時回報每日健康狀況的問卷追蹤系統。系統會自動建立每日問卷、接收使用者提交的資料，並在指定時間自動發送提醒給尚未填寫的使用者。

本專案使用 Flask 作為後端框架，並設計為可輕鬆部署於 Zeabur 平台。

---

## 功能特色

- **每日三時段問卷**：使用者需於 10:00、13:00、17:00 透過 LIFF 頁面填寫健康問卷。
- **自動預建記錄**：每日 00:00，系統會為所有有效會員自動建立當日的三份空白問卷。
- **即時填寫更新**：使用者透過 LIFF 頁面提交問卷時，系統會即時更新對應的資料庫記錄。
- **自動漏填提醒**：每日 20:00，系統會檢查當日問卷是否有缺漏，並透過 LINE Bot 發送一對一提醒訊息。

---

## 技術棧

- **後端**: Python, Flask
- **資料庫**: MySQL (使用 `pymysql` 連接)
- **排程任務**: `apscheduler`
- **部署伺服器**: `gunicorn`
- **部署平台**: Zeabur

---

## 資料庫設計

系統包含 `users` (使用者) 和 `surveys` (問卷記錄) 兩張資料表。

### `users` Table
儲存已註冊的使用者基本資料。
```sql
CREATE TABLE users (
  lineId      VARCHAR(50) PRIMARY KEY,
  name        VARCHAR(100) NOT NULL,
  gender      ENUM('男','女') NOT NULL,
  age         INT          NOT NULL,
  is_active   TINYINT(1)   DEFAULT 1,
  created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP
);
```

### `surveys` Table
記錄每日各時段的問卷填寫狀況。
```sql
CREATE TABLE surveys (
  id          BIGINT      PRIMARY KEY AUTO_INCREMENT,
  date        DATE        NOT NULL,
  slot        ENUM('10:00','13:00','17:00') NOT NULL,
  lineId      VARCHAR(50) NOT NULL,
  name        VARCHAR(20) NOT NULL,
  gender      ENUM('男','女') NOT NULL,
  age         INT         NOT NULL,
  q1          CHAR(1),    -- 'V'/'X' or NULL
  q2          CHAR(1),
  q3          CHAR(1),
  q4          CHAR(1),
  remark      VARCHAR(20),
  submittedAt DATETIME    DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uk_survey (date, slot, lineId),
  FOREIGN KEY (lineId) REFERENCES users(lineId)
);
```

---

## 本地端設定與啟動

1.  **複製專案**
    ```bash
    git clone https://github.com/FelixLin02/Line-QA_Cursor.git
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
    - 根據上述 `資料庫設計` 建立 `users` 和 `surveys` 資料表。

4.  **設定環境變數**
    為了讓程式能連接到資料庫，您需要在本地設定環境變數，或直接修改 `app.py` 和 `scheduler.py` 中的 `DB_CONFIG`。

5.  **啟動服務**
    - **啟動 Web 伺服器**:
      ```bash
      python app.py
      ```
    - **啟動排程器** (開啟另一個終端機):
      ```bash
      python scheduler.py
      ```

---

## Zeabur 部署指南

1.  **推送至 GitHub**:
    確保所有程式碼 (包含 `Procfile`) 都已推送到您的 GitHub 儲存庫。

2.  **在 Zeabur 建立專案**:
    - 登入 Zeabur，建立新專案並連結到您的 GitHub 儲存庫。
    - Zeabur 會自動偵測 `Procfile` 並建立 `web` 和 `worker` 兩個服務。

3.  **設定環境變數**:
    在 Zeabur 專案的 "Variables" 頁面，新增以下環境變數：
    - `DB_HOST`: 您的資料庫主機位址
    - `DB_USER`: 資料庫使用者名稱
    - `DB_PASSWORD`: 資料庫密碼
    - `DB_DATABASE`: 資料庫名稱
    - `LINE_CHANNEL_ACCESS_TOKEN`: 您的 LINE Channel Access Token

4.  **取得 LIFF 連結**:
    - 部署完成後，Zeabur 會為您的 `web` 服務提供一個公開網址 (例如: `https://your-project.zeabur.app`)。
    - 您的 LIFF URL 為: **`https://<您的 Zeabur 網址>/survey`**

5.  **設定 LINE LIFF**:
    前往 LINE Developers Console，將上述 URL 填入 LIFF App 的 "Endpoint URL" 欄位。
