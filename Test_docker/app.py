import sqlite3
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

# List of tables to process
tables = ['host3']

@app.route('/')
def index():
    triggers = {}
    conn = get_db_connection()
    try:
        for table in tables:
            last_record = get_last_record(conn, table)
            if last_record:
                # Assuming the columns have indices for current_amounts and state_amounts
                triger_state = last_record[8:12]
                for i in range(1, 5):
                    triggers[f"trigger_{i}"] = triger_state[i-1]
                    print(triggers)
    finally:
        conn.close()  # Ensure the connection is closed after use

    return render_template('alarm.html', triggers=triggers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
