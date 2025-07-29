import pymysql
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

DB_CONFIG = {
    'host': 'localhost',
    'user': 'survey_user',
    'password': 'P@ssw0rd',
    'database': 'line_survey_db',
    'charset': 'utf8mb4'
}

LINE_CHANNEL_ACCESS_TOKEN = 'HVmEY/uPF+fahkzZYmPxA3c82yhwHy9SchF748yA2XWfO7Hj82Qq6qWj0kQSNziJCDDwVgVG5pnSZsnAwYIh0MFBvQ3oU2LktL0djXH51k0e+bud9uEUZyhdQ/w8uCDbDEay9DbIDeKpLGIznhGqBQdB04t89/1O/w1cDnyilFU='
LINE_API_URL = 'https://api.line.me/v2/bot/message/push'

# 預建問卷
def create_daily_surveys():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            sql = """
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
              SELECT '13:00' UNION ALL
              SELECT '17:00'
            ) AS slot_list
            WHERE u.is_active = 1;
            """
            cursor.execute(sql)
        conn.commit()
        print(f"[{datetime.now()}] 問卷預建完成")
    except Exception as e:
        print(f"[{datetime.now()}] 預建問卷失敗: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

# 查詢需提醒用戶
def get_users_need_reminder():
    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT DISTINCT lineId
                FROM surveys
                WHERE date = CURDATE()
                  AND (q1 IS NULL OR q2 IS NULL OR q3 IS NULL OR q4 IS NULL)
            """
            cursor.execute(sql)
            results = cursor.fetchall()
            return [row[0] for row in results]
    finally:
        conn.close()

# 發送 LINE 提醒
def send_line_reminder(line_id):
    headers = {
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": line_id,
        "messages": [{
            "type": "text",
            "text": "您今日有健康問卷尚未完成，請於今晚前補填，謝謝！"
        }]
    }
    response = requests.post(LINE_API_URL, headers=headers, json=data)
    return response.status_code == 200

# 20:00 提醒
def remind_users():
    users = get_users_need_reminder()
    print(f"[{datetime.now()}] 需提醒人數: {len(users)}")
    for line_id in users:
        success = send_line_reminder(line_id)
        print(f"提醒 {line_id} {'成功' if success else '失敗'}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    # 每天 00:00 預建問卷
    scheduler.add_job(create_daily_surveys, 'cron', hour=0, minute=0)
    # 每天 20:00 提醒
    scheduler.add_job(remind_users, 'cron', hour=20, minute=0)
    print("排程啟動，等待每日 00:00/20:00 執行...")
    scheduler.start() 