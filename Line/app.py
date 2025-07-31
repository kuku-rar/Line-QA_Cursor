from flask import Flask, request, jsonify, send_from_directory
import pymysql
from datetime import date, datetime
import os
import time # 引入 time 模組用於等待

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
    """初始化資料庫和表結構，並加入重試機制與自動結構修正"""
    max_retries = 5
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        conn = None
        try:
            print(f"🚀 [嘗試 {attempt + 1}/{max_retries}] 連線到資料庫...")
            
            db_name = DB_CONFIG['database']
            temp_config = DB_CONFIG.copy()
            temp_config.pop('database')
            temp_config.pop('cursorclass', None)
            conn = pymysql.connect(**temp_config)

            with conn.cursor() as cursor:
                print("✅ 資料庫連線成功，開始檢查/更新結構...")
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                cursor.execute(f"USE `{db_name}`")

                # 建立 users 表
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

                with conn.cursor(pymysql.cursors.DictCursor) as dict_cursor:
                    # **【關鍵修正】** 檢查並修正 gender 欄位為允許 NULL
                    dict_cursor.execute("SELECT IS_NULLABLE FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' AND COLUMN_NAME = 'gender'", (db_name,))
                    result = dict_cursor.fetchone()
                    if result and result['IS_NULLABLE'] == 'NO':
                        print("⚠️ 'users.gender' 是 NOT NULL, 正在修正為允許 NULL...")
                        cursor.execute("ALTER TABLE users MODIFY COLUMN gender ENUM('male', 'female', 'other') NULL;")
                        print("✅ 'users.gender' 欄位修正完成。")

                    # **【關鍵修正】** 檢查並修正 age 欄位為允許 NULL
                    dict_cursor.execute("SELECT IS_NULLABLE FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' AND COLUMN_NAME = 'age'", (db_name,))
                    result = dict_cursor.fetchone()
                    if result and result['IS_NULLABLE'] == 'NO':
                        print("⚠️ 'users.age' 是 NOT NULL, 正在修正為允許 NULL...")
                        cursor.execute("ALTER TABLE users MODIFY COLUMN age INT NULL;")
                        print("✅ 'users.age' 欄位修正完成。")
                    
                    # 檢查並安全地新增 birthday 欄位
                    dict_cursor.execute("SELECT COUNT(*) as count FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' AND COLUMN_NAME = 'birthday'", (db_name,))
                    if dict_cursor.fetchone()['count'] == 0:
                        print("⚠️ 'users' 表中缺少 'birthday' 欄位，正在新增...")
                        cursor.execute("ALTER TABLE users ADD COLUMN birthday DATE NULL AFTER gender;")
                        print("✅ 'birthday' 欄位新增完成")

                # 建立 surveys 表
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
            print("✅ 資料庫結構初始化/驗證完成。")
            return

        except pymysql.err.OperationalError as e:
            print(f"⚠️ 資料庫連線操作失敗: {e}")
            if attempt + 1 == max_retries:
                print("❌ 已達最大重試次數，放棄初始化。")
                raise e
            print(f"   將在 {retry_delay} 秒後重試...")
            time.sleep(retry_delay)
        
        except Exception as e:
            print(f"❌ 資料庫初始化時發生未預期的錯誤: {e}")
            raise e
        
        finally:
            if conn and conn.open:
                conn.close()

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

            if 'gender' in data and 'age' in data and 'birthday' in data:
                cursor.execute("""
                    UPDATE users SET
                        gender = COALESCE(gender, %s),
                        age = COALESCE(age, %s),
                        birthday = COALESCE(birthday, %s)
                    WHERE id = %s
                """, (data.get('gender'), data.get('age'), data.get('birthday'), user_id))

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