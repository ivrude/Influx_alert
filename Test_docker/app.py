import sqlite3

import requests
from flask import Flask, render_template

app = Flask(__name__)

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('Test.db')
    conn.row_factory = sqlite3.Row  # This allows you to access columns by name
    return conn

# Function to get the last record from a table
def get_last_record(conn, table_name):
    cursor = conn.cursor()
    query = f'SELECT * FROM "{table_name}" ORDER BY rowid DESC LIMIT 1'
    cursor.execute(query)
    record = cursor.fetchone()
    return record

# Process a table and update triggers dictionary
def process_table(triggers, conn, table_name, prefix):
    last_record = get_last_record(conn, table_name)
    if last_record:
        # Assuming the columns have indices for current_amounts and state_amounts
        triger_state = last_record[8:12]
        sumar = sum(triger_state)
        for i in range(1, 5):
            if sumar > 1:
                if triger_state[i-1] == 0:
                    triggers[f"{prefix}{i}"] = triger_state[i-1]
                else:
                    triggers[f"{prefix}{i}"] = 2
            else:
                triggers[f"{prefix}{i}"] = triger_state[i-1]
        for i in range (1, 5):
            if triger_state[i-1] == 1:

                responce = requests.post("http://192.168.0.151:5001/webhook2")

@app.route('/')
def index():
    triggers = {}
    conn = get_db_connection()
    try:
        for table in ['host3']:
            process_table(triggers, conn, table, "trigger_")
        for table in ['host3_e']:
            process_table(triggers, conn, table, "trigger_e")
    finally:
        conn.close()  # Ensure the connection is closed after use

    return render_template('alarm.html', triggers=triggers)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=False)
