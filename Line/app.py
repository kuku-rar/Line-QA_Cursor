from flask import Flask, request, jsonify, send_from_directory
import pymysql
from datetime import datetime
import os

app = Flask(__name__)

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'survey_user'),
    'password': os.environ.get('DB_PASSWORD', 'P@ssw0rd'),
    'database': os.environ.get('DB_DATABASE', 'line_survey_db'),
    'charset': 'utf8mb4'
}

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

if __name__ == "__main__":
    app.run(debug=True) 