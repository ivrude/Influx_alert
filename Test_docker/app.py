import sqlite3
from flask import Flask, render_template, jsonify

app = Flask(__name__)

connection = sqlite3.connect("/home/admin-user/Influx_alert/Test_docker/Test.db")
cursor = connection.cursor()

# Створюємо таблицу host3_e
cursor.execute('''
               CREATE TABLE IF NOT EXISTS host3_e
               (
                   id
                       INTEGER
                       PRIMARY
                           KEY,
                   vymir_1
                       REAL,
                   vymir_2
                       REAL,
                   vymir_3
                       REAL,
                   vymir_4
                       REAL,
                   fon_1
                       REAL,
                   fon_2
                       REAL,
                   fon_3
                       REAL,
                   fon_4
                       REAL,
                   triger_1
                       INTEGER,
                   triger_2
                       INTEGER,
                   triger_3
                       INTEGER,
                   triger_4
                       INTEGER,
                   triger_0
                       INTEGER,
                    radiometr_state
                        INTEGER
               )
               ''')
conn = sqlite3.connect("/home/admin-user/Influx_alert/Test_docker/Test.db")
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('alarm.html')

@app.route('/latest_data')
def latest_data():
    conn = sqlite3.connect("/home/admin-user/Influx_alert/Test_docker/Test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM host3_e ORDER BY rowid DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        keys = ["curent_amount_1", "curent_amount_2", "curent_amount_3", "curent_amount_4",
                "state_amount_1", "state_amount_2", "state_amount_3", "state_amount_4",
                "triger_1", "triger_2", "triger_3", "triger_4", "radiometr_state","id", "triger_0"]
        return jsonify(dict(zip(keys, row)))
    return jsonify({})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
