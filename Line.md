# LINE 健康問卷追蹤系統整合設計

---

## 一、系統目標
1. **每日三時段問卷**：使用者需於 10:00、13:00、17:00 填寫健康問卷。  
2. **自動預建記錄**：每天 00:00 為所有LINE有效會員新增三筆空問卷記錄（早/中/晚）。  
3. **即時填寫更新**：使用者點擊 LIFF 填寫時，更新既有記錄，題目未填欄位存為 `null`。  
4. **漏填提醒**：每天 20:00 統計當日問卷 `q1~q4` 是否有 `null`，並透過 LINE 官方帳號個別提醒。

---

## 二、資料庫設計

```sql
-- 使用者主表
CREATE TABLE users (
  lineId      VARCHAR(50) PRIMARY KEY,
  name        VARCHAR(100) NOT NULL,
  gender      ENUM('男','女') NOT NULL,
  age         INT          NOT NULL,
  is_active   TINYINT(1)   DEFAULT 1,
  created_at  DATETIME     DEFAULT CURRENT_TIMESTAMP
);

-- 問卷記錄表
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

 資料表格參考:(1. ~ 4. 問題為必填，選項只有V 或 X) 
| 日期 | 時間 | LINE_ID | 姓名 | 性別 | 年紀 | 1. 喝水500cc | 2. 吃藥 | 3. 拉筋 | 4. 超慢跑 | 備註(限20字) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025/7/27 | 10:00 | DANNYLIU | 丹尼 | 男 | 56 | V | V | V | V |  |
| 2025/7/27 | 13:00 | DANNYLIU | 丹尼 | 男 | 56 | V | V | V | V |  |
| 2025/7/27 | 17:00 | DANNYLIU | 丹尼 | 男 | 56 | V | V | V | V |  |
| 2025/7/27 | 10:00 | WANG | 王小姐 | 女 | 65 | V | X | V | V | 肚子會痛 |
| 2025/7/27 | 13:00 | WANG | 王小姐 | 女 | 65 | V |  | V | V |  |
| 2025/7/27 | 17:00 | WANG | 王小姐 | 女 | 65 | V | V | V | V |  |
| 2025/7/27 | 10:00 | SAM113 | 山姆 | 男 | 57 | X | V | V | V |  |
| 2025/7/27 | 13:00 | SAM113 | 山姆 | 男 | 57 | X | V | V | V |  |
| 2025/7/27 | 17:00 | SAM113 | 山姆 | 男 | 57 | X | V | V | V |  |

---
## 三、自動預建問卷記錄（00:00 排程）

---
INSERT IGNORE INTO surveys (date, slot, lineId, name, gender, age)
SELECT
  CURDATE(),
  slot_list.slot,
  u.lineId,
  u.name,
  u.gender,
  u.age
FROM users u
CROSS JOIN (
  SELECT '10:00' AS slot UNION ALL
  SELECT '13:00'      UNION ALL
  SELECT '17:00'
) AS slot_list
WHERE u.is_active = 1;


