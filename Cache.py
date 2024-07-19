import sqlite3
from time import sleep
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import datetime
from config import token_influx, url_influx

# Параметри підключення до InfluxDB
token = token_influx
org = "Chornobyl"
bucket = "Graf"
url = url_influx

# Ініціалізація клієнта InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Створення локальної бази даних SQLite для кешування
conn_cache = sqlite3.connect('local_cache.db')
c_cache = conn_cache.cursor()
c_cache.execute('''CREATE TABLE IF NOT EXISTS data_cache
                   (id INTEGER PRIMARY KEY, measurement TEXT, field TEXT, value REAL, host TEXT, timestamp DATETIME)''')
conn_cache.commit()

# Функція для отримання останнього запису з таблиці
def get_last_record(cursor, table_name):
    query = f"SELECT * FROM {table_name} ORDER BY rowid DESC LIMIT 1"
    cursor.execute(query)
    return cursor.fetchone()

# Функція для запису даних в InfluxDB або кешування в разі невдачі
def zapis(name, value, host, timestamp=None):
    if timestamp is None:
        timestamp = datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # Adjusting for UTC+3
    timestamp_ns = int(timestamp.timestamp() * 1e9)
    data = f"test_6,host={host} {name}={value} {timestamp_ns}"
    try:
        write_api.write(bucket=bucket, org=org, record=data)
        print(f"Datas written to InfluxDB: {name}={value} at {timestamp}")
    except Exception as e:
        print(f"Failed to write to InfluxDB, caching locally: {e}")
        c_cache.execute("INSERT INTO data_cache (measurement, field, value, host, timestamp) VALUES (?, ?, ?, ?, ?)", ("test_6", name, value, host, timestamp))
        conn_cache.commit()

# Функція для повторної відправки кешованих даних
def resend_cached_data():
    c_cache.execute("SELECT * FROM data_cache")
    rows = c_cache.fetchall()
    for row in rows:
        try:
            timestamp_ns = int(datetime.datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S.%f').timestamp() * 1e9)
            data = f"{row[1]},host={row[4]} {row[2]}={row[3]} {timestamp_ns}"
            write_api.write(bucket=bucket, org=org, record=data)
            c_cache.execute("DELETE FROM data_cache WHERE id=?", (row[0],))
            conn_cache.commit()
            print(f"Resent cached data to InfluxDB: {row[2]}={row[3]} at {row[5]}")
        except Exception as e:
            print(f"Failed to resend cached data: {e}")
            break

# Підключення до основної бази даних SQLite
conn = sqlite3.connect('Test_docker/Test.db')
cursor = conn.cursor()

# Список таблиць для обробки
tables = ['host3_e','host3']

# Запис останніх даних з кожної таблиці в InfluxDB

# Періодична перевірка та повторна відправка кешованих даних
while True:
    for table in tables:
        last_record = get_last_record(cursor, table)
        radio_state = last_record[12]
        if radio_state == 0:
            if last_record:
                current_amounts = last_record[:4]
                state_amounts = last_record[4:8]
                triger_state = last_record[8:12]
                sumar = last_record[8] + last_record[9] + last_record[10] + last_record[11]
                timestamp = datetime.datetime.utcnow() + datetime.timedelta(hours=3)  # Adjusting for UTC+3
                zapis("radio_state", radio_state, table, timestamp)
                for i, value in enumerate(current_amounts, start=1):
                    zapis(f"current_amount_{i}", value, table, timestamp)
                for i, value in enumerate(state_amounts, start=1):
                    zapis(f"state_amount_{i}", value, table, timestamp)
                if sumar > 1:
                    for i, value in enumerate(triger_state, start=1):
                        if triger_state[i-1] == 0:
                            zapis(f"triger_state_{i}", value, table, timestamp)
                        else:
                            zapis(f"triger_state_{i}", 2, table, timestamp)
                else:
                    for i, value in enumerate(triger_state, start=1):
                        zapis(f"triger_state_{i}", value, table, timestamp)
        else:
            zapis("radio_state", radio_state, table, timestamp)
    resend_cached_data()
    sleep(60)  # Перевіряємо кожну хвилину

# Закриття з'єднання з InfluxDB та SQLite
client.close()
conn_cache.close()
conn.close()
