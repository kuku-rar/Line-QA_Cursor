import os
import pymysql
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from zoneinfo import ZoneInfo
from datetime import datetime

# --- 設定 ---
# 從環境變數讀取資料庫設定，與 app.py 相同
DB_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'mysql.zeabur.internal'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'database': os.environ.get('MYSQL_DATABASE', 'zeabur'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}
# 從環境變數讀取你的 Channel Access Token (需要從 LINE Developers 後台取得)
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', 'HVmEY/uPF+fahkzZYmPxA3c82yhwHy9SchF748yA2XWfO7Hj82Qq6qWj0kQSNziJCDDwVgVG5pnSZsnAwYIh0MFBvQ3oU2LktL0djXH51k0e+bud9uEUZyhdQ/w8uCDbDEay9DbIDeKpLGIznhGqBQdB04t89/1O/w1cDnyilFU=')
LINE_API_URL = 'https://api.line.me/v2/bot/message/push'

def send_reminder_message(user_id, user_name):
    """使用 LINE Messaging API 發送推播提醒訊息"""
    if not LINE_CHANNEL_ACCESS_TOKEN:
        print("❌ 未設定 LINE_CHANNEL_ACCESS_TOKEN 環境變數，無法發送提醒。")
        return

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
    }
    
    # 你可以自訂提醒的文字內容
    message_body = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": f"你好 {user_name}！溫馨提醒，您今天還有健康問卷尚未完成填寫喔，請記得完成！"
            }
        ]
    }
    
    try:
        response = requests.post(LINE_API_URL, headers=headers, json=message_body)
        response.raise_for_status() # 如果請求失敗 (e.g., 4xx or 5xx), 會拋出例外
        print(f"✅ 已成功發送提醒給 {user_name} ({user_id})")
    except requests.exceptions.RequestException as e:
        print(f"❌ 發送提醒給 {user_name} ({user_id}) 失敗: {e}")
        # 印出 LINE API 回傳的錯誤訊息，方便除錯
        if e.response is not None:
            print(f"   - 回應內容: {e.response.text}")

def remind_users():
    """找出所有未完成當日問卷的使用者，並呼叫發送函式"""
    print(f"⏰ {datetime.now(ZoneInfo('Asia/Taipei'))} - 開始執行每日提醒任務...")
    conn = None
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            # 使用新的資料庫結構來查詢
            # 找出今天有至少一筆問卷的 submitted_at 是 NULL 的使用者
            sql = """
                SELECT u.lineId, u.name
                FROM users u
                JOIN surveys s ON u.id = s.user_id
                WHERE s.survey_date = CURDATE() AND s.submitted_at IS NULL
                GROUP BY u.id, u.lineId, u.name
                HAVING COUNT(*) > 0;
            """
            cursor.execute(sql)
            users_to_remind = cursor.fetchall()

            if not users_to_remind:
                print("👍 所有使用者的今日問卷都已完成，無需提醒。")
                return

            print(f"🔍 發現 {len(users_to_remind)} 位使用者需要提醒。")
            for user in users_to_remind:
                send_reminder_message(user['lineId'], user['name'])

    except pymysql.MySQLError as e:
        print(f"❌ 執行提醒任務時發生資料庫錯誤: {e}")
    except Exception as e:
        print(f"❌ 執行提醒任務時發生未預期錯誤: {e}")
    finally:
        if conn:
            conn.close()
        print("✅ 每日提醒任務執行完畢。")

if __name__ == "__main__":
    # 設定排程器，並明確指定時區為台北
    scheduler = BlockingScheduler(timezone=ZoneInfo("Asia/Taipei"))

    # 新增任務：設定在每天晚上 9 點 (21:00) 執行 remind_users 函式
    scheduler.add_job(
        remind_users,
        trigger=CronTrigger(hour=22, minute=00),
        id='daily_reminder_job',
        name='Daily survey reminder',
        replace_existing=True
    )

    print("🚀 排程提醒服務已啟動，等待觸發時間 (每日 21:00)...")
    
    # 如果您想在服務一啟動時就立刻測試一次，可以取消下面這行的註解
    # remind_users() 

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("🛑 排程提醒服務已停止。")