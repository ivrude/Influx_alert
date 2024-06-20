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
                current_amounts = last_record[:4]
                state_amounts = last_record[4:8]
                for i in range(1, 5):
                    current_amount = current_amounts[i-1]
                    state_amount = state_amounts[i-1]
                    if current_amount is not None and state_amount is not None:
                        if current_amount > 2 * state_amount and current_amount < 3 * state_amount:
                            triggers[f"trigger_{i}"] = 2
                        elif current_amount >= 3 * state_amount:
                            triggers[f"trigger_{i}"] = 3
                        else:
                            triggers[f"trigger_{i}"] = 1
                    else:
                        triggers[f"trigger_{i}"] = None
            else:
                triggers = {f"trigger_{i}": None for i in range(1, 5)}
    finally:
        conn.close()  # Ensure the connection is closed after use

    return render_template('alarm.html', triggers=triggers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
