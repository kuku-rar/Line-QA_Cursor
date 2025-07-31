from flask import Flask, request, jsonify, send_from_directory
import pymysql
from datetime import date, datetime
import os

app = Flask(__name__)

# --- 資料庫設定 ---
DB_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'mysql.zeabur.internal'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'database': os.environ.get('MYSQL_DATABASE', 'zeabur'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    """建立並回傳資料庫連線"""
    return pymysql.connect(**DB_CONFIG)

def init_database():
    """初始化資料庫和表結構，並安全地新增欄位"""
    conn = None
    try:
        db_name = DB_CONFIG['database']
        # 先連線到 MySQL，不指定特定資料庫
        temp_config = DB_CONFIG.copy()
        temp_config.pop('database')
        temp_config.pop('cursorclass')
        conn = pymysql.connect(**temp_config)

        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.execute(f"USE `{db_name}`")

            # 建立 users 表 (如果不存在)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    lineId VARCHAR(255) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    gender ENUM('male', 'female', 'other') NULL,
                    age INT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_lineId (lineId)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)

            # **【關鍵修正】** 檢查並安全地新增 birthday 欄位
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' AND COLUMN_NAME = 'birthday'
            """, (db_name,))
            if cursor.fetchone()['count'] == 0:
                print("⚠️ 'users' 表中缺少 'birthday' 欄位，正在新增...")
                cursor.execute("ALTER TABLE users ADD COLUMN birthday DATE NULL AFTER gender;")
                print("✅ 'birthday' 欄位新增完成")

            # 建立 surveys 表 (如果不存在)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS surveys (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    survey_date DATE NOT NULL,
                    slot ENUM('10:00', '13:00', '17:00') NOT NULL,
                    q1 ENUM('V', 'X') NULL,
                    q2 ENUM('V', 'X') NULL,
                    q3 ENUM('V', 'X') NULL,
                    q4 ENUM('V', 'X') NULL,
                    remark TEXT NULL,
                    submitted_at TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_survey (user_id, survey_date, slot),
                    INDEX idx_date_slot (survey_date, slot),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)
        conn.commit()
        print("✅ 資料庫結構初始化/驗證完成")
    except Exception as e:
        print(f"❌ 資料庫初始化失敗: {e}")
        raise e
    finally:
        if conn and conn.open:
            conn.close()

# 在應用程式啟動時執行資料庫初始化
init_database()

@app.route('/survey')
def survey_page():
    return send_from_directory('.', 'survey.html')

@app.route('/api/user/sync', methods=['POST'])
def sync_user():
    data = request.get_json()
    if not data or 'lineId' not in data or 'name' not in data:
        return jsonify({'success': False, 'error': 'Missing lineId or name'}), 400

    lineId = data['lineId']
    name = data['name']
    today = date.today()
    slots = ['10:00', '13:00', '17:00']

    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE lineId = %s", (lineId,))
            user = cursor.fetchone()

            if user:
                user_id = user['id']
                cursor.execute("UPDATE users SET name = %s WHERE id = %s", (name, user_id))
            else:
                cursor.execute("INSERT INTO users (lineId, name) VALUES (%s, %s)", (lineId, name))
                user_id = cursor.lastrowid

            for slot in slots:
                cursor.execute("INSERT IGNORE INTO surveys (user_id, survey_date, slot) VALUES (%s, %s, %s)", (user_id, today, slot))
            
            conn.commit()

            # **【關鍵修正】** SELECT 查詢中也加入 birthday
            cursor.execute("SELECT lineId, name, gender, birthday, age FROM users WHERE id = %s", (user_id,))
            user_profile = cursor.fetchone()

            return jsonify({'success': True, 'userProfile': user_profile})

    except pymysql.MySQLError as e:
        print(f"資料庫錯誤: {e}")
        return jsonify({'success': False, 'error': f'Database error: {e}'}), 500
    except Exception as e:
        print(f"伺服器錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/survey/submit', methods=['POST'])
def submit_survey():
    data = request.get_json()
    required_fields_survey = ['lineId', 'slot', 'q1', 'q2', 'q3', 'q4']
    if not all(field in data for field in required_fields_survey):
        return jsonify({'success': False, 'error': 'Missing required survey fields'}), 400

    lineId = data['lineId']
    slot = data['slot']

    conn = None
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM users WHERE lineId = %s", (lineId,))
            user = cursor.fetchone()
            if not user:
                return jsonify({'success': False, 'error': 'User not found. Please sync first.'}), 404
            user_id = user['id']

            # **【關鍵修正】** 如果是註冊流程，則更新使用者基本資料
            if 'gender' in data and 'age' in data and 'birthday' in data:
                cursor.execute("""
                    UPDATE users SET
                        gender = COALESCE(gender, %s),
                        age = COALESCE(age, %s),
                        birthday = COALESCE(birthday, %s)
                    WHERE id = %s
                """, (data.get('gender'), data.get('age'), data.get('birthday'), user_id))

            # 更新問卷答案
            sql_update = """
                UPDATE surveys
                SET q1=%s, q2=%s, q3=%s, q4=%s, remark=%s, submitted_at=%s
                WHERE user_id=%s AND survey_date=CURDATE() AND slot=%s
            """
            affected_rows = cursor.execute(sql_update, (
                data.get('q1'), data.get('q2'), data.get('q3'), data.get('q4'), 
                data.get('remark'), datetime.now(), user_id, slot
            ))

            if affected_rows == 0:
                 return jsonify({'success': False, 'error': 'No survey record found to update for today and this slot.'}), 404

            conn.commit()
            return jsonify({'success': True, 'message': 'Survey submitted successfully.'})
            
    except pymysql.MySQLError as e:
        print(f"資料庫錯誤: {e}")
        return jsonify({'success': False, 'error': f'Database error: {e}'}), 500
    except Exception as e:
        print(f"伺服器錯誤: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))