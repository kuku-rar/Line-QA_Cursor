from flask import Flask, request, jsonify, send_from_directory
import pymysql
from datetime import datetime
import os

app = Flask(__name__)

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'mysql.zeabur.internal'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', 'JdTHR3vX816u2kU4WmtVZCi90p5rqY7a'),
    'database': os.environ.get('DB_DATABASE', 'zeabur'),
    'charset': 'utf8mb4'
}

def init_database():
    """初始化資料庫和表結構"""
    try:
        # 先連接到 MySQL 伺服器（不指定資料庫）
        conn = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            charset=DB_CONFIG['charset']
        )
        
        with conn.cursor() as cursor:
            # 建立資料庫（如果不存在）
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            cursor.execute(f"USE {DB_CONFIG['database']}")
            
            # 建立 users 表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    lineId VARCHAR(50) UNIQUE NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    gender ENUM('male', 'female', 'other') NOT NULL,
                    age INT NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
            # 建立 surveys 表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS surveys (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    slot ENUM('10:00', '13:00', '17:00') NOT NULL,
                    lineId VARCHAR(50) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    gender ENUM('male', 'female', 'other') NOT NULL,
                    age INT NOT NULL,
                    q1 ENUM('V', 'X') NULL,
                    q2 ENUM('V', 'X') NULL,
                    q3 ENUM('V', 'X') NULL,
                    q4 ENUM('V', 'X') NULL,
                    remark TEXT NULL,
                    submittedAt TIMESTAMP NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    UNIQUE KEY unique_survey (date, slot, lineId),
                    INDEX idx_lineId (lineId),
                    INDEX idx_date_slot (date, slot)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            
        conn.commit()
        print("✅ 資料庫初始化完成")
        
    except Exception as e:
        print(f"❌ 資料庫初始化失敗: {e}")
        raise e
    finally:
        if 'conn' in locals():
            conn.close()

# 在應用程式啟動時初始化資料庫
init_database()

@app.route('/survey')
def survey_page():
    return send_from_directory('.', 'survey.html')

@app.route('/api/survey/submit', methods=['POST'])
def submit_survey():
    data = request.get_json()
    required_fields = ['lineId', 'slot']
    for field in required_fields:
        if field not in data:
            return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400

    lineId = data['lineId']
    slot = data['slot']
    q1 = data.get('q1')
    q2 = data.get('q2')
    q3 = data.get('q3')
    q4 = data.get('q4')
    remark = data.get('remark', None)

    if slot not in ['10:00', '13:00', '17:00']:
        return jsonify({'success': False, 'error': 'Invalid slot'}), 400

    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            sql_select = """
                SELECT id FROM surveys
                WHERE lineId=%s AND date=CURDATE() AND slot=%s
            """
            cursor.execute(sql_select, (lineId, slot))
            result = cursor.fetchone()
            if not result:
                return jsonify({'success': False, 'error': 'No survey record found'}), 404

            survey_id = result[0]
            sql_update = """
                UPDATE surveys
                SET q1=%s, q2=%s, q3=%s, q4=%s, remark=%s, submittedAt=%s
                WHERE id=%s
            """
            cursor.execute(sql_update, (
                q1, q2, q3, q4, remark, datetime.now(), survey_id
            ))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

@app.route('/api/user/sync', methods=['POST'])
def user_sync():
    data = request.get_json()
    lineId = data.get('lineId')
    name = data.get('name')
    if not lineId or not name:
        return jsonify({'success': False, 'error': '缺少 lineId 或 name'}), 400
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            cursor.execute("SELECT lineId, name, gender, birthday, age FROM users WHERE lineId=%s", (lineId,))
            user = cursor.fetchone()
            if not user:
                # 新用戶，僅存 lineId, name, is_active=1
                cursor.execute("INSERT INTO users (lineId, name, is_active, created_at, updated_at) VALUES (%s, %s, 1, NOW(), NOW())", (lineId, name))
                conn.commit()
                return jsonify({'success': True, 'status': 'new'})
            else:
                # 已存在，若 name 有變則自動更新
                if user[1] != name:
                    cursor.execute("UPDATE users SET name=%s, updated_at=NOW() WHERE lineId=%s", (name, lineId))
                    conn.commit()
                # 回傳完整資料
                user_dict = {
                    'lineId': user[0],
                    'name': user[1],
                    'gender': user[2],
                    'birthday': user[3],
                    'age': user[4]
                }
                return jsonify({'success': True, 'status': 'exist', 'user': user_dict})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    app.run(debug=True) 