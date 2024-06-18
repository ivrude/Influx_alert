import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

#app when no connection
# Функція для отримання останнього запису з таблиці
# docker run -p 5000:5000 -v "$(pwd)/Test.db:/app/Test.db" flask_app
def get_last_record(table_name):
    conn = sqlite3.connect('Test.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM {table_name}  ORDERBY rowid DESC LIMIT 1"
    cursor.execute(query)
    record = cursor.fetchone()
    conn.close()
    return record

# Список таблиць для обробки
tables = ['host3']

@app.route('/')
def index():
    triggers = {}
    for table in tables:
        last_record = get_last_record(table)
        if last_record:
            # Припустимо, що стовпці мають індекси для current_amounts і state_amounts
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

    return render_template('alarm.html', triggers=triggers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
