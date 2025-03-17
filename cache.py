# app to send info to influx from local db
import datetime
import sqlite3
from time import sleep
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from config import token_influx, url_influx

# Параметри підключення до InfluxDB
TOKEN = token_influx
ORG = "Chornobyl"
BUCKET = "Graf"
URL = url_influx

# Ініціалізація клієнта InfluxDB
client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Створення локальної бази даних SQLite для кешування
conn_cache = sqlite3.connect("local_cache.db")
c_cache = conn_cache.cursor()
c_cache.execute(
    """CREATE TABLE IF NOT EXISTS data_cache
                   (id INTEGER PRIMARY KEY, 
                   measurement TEXT, 
                   field TEXT, 
                   value REAL, 
                   host TEXT, 
                   timestamp DATETIME)"""
)
conn_cache.commit()


# Get last record from db
def get_last_record(cursor, table_name):
    query = f"SELECT * FROM {table_name} ORDER BY rowid DESC LIMIT 1"
    cursor.execute(query)
    return cursor.fetchone()


# send data to influx or cache
def zapis(name, value, host, timestamp=None):
    if timestamp is None:
        timestamp = datetime.datetime.utcnow() + datetime.timedelta(
            hours=2
        )  # Adjusting for UTC+3
    timestamp_ns = int(timestamp.timestamp() * 1e9)
    data = f"test_6,host={host} {name}={value} {timestamp_ns}"
    try:
        write_api.write(bucket=BUCKET, org=ORG, record=data)
        print(f"Datas written to InfluxDB: {name}={value} at {timestamp}")
    except Exception as e:
        print(f"Failed to write to InfluxDB, caching locally: {e}")
        c_cache.execute(
            "INSERT INTO data_cache (measurement, field, value,"
            " host, timestamp) VALUES (?, ?, ?, ?, ?)",
            ("test_6", name, value, host, timestamp),
        )
        conn_cache.commit()


# resend data fron cache
def resend_cached_data():
    c_cache.execute("SELECT * FROM data_cache")
    rows = c_cache.fetchall()
    for row in rows:
        try:
            timestamp_ns = int(
                datetime.datetime.strptime(
                    row[5], "%Y-%m-%d %H:%M:%S.%f"
                ).timestamp()
                * 1e9
            )
            data = f"{row[1]},host={row[4]} {row[2]}={row[3]} {timestamp_ns}"
            write_api.write(bucket=BUCKET, org=ORG, record=data)
            c_cache.execute("DELETE FROM data_cache WHERE id=?", (
                row[0],
            ))
            conn_cache.commit()
            print(
                f"Resent cached data to Influx: {row[2]}={row[3]} at {row[5]}"
            )
        except Exception as e:
            print(f"Failed to resend cached data: {e}")
            break


# connect to local db
conn = sqlite3.connect("./Test.db")
cursor = conn.cursor()

# Список таблиць для обробки
tables = ["host3"]

# Запис останніх даних з кожної таблиці в InfluxDB

# Cycle loking into local db and sending data
while True:
    for table in tables:
        last_record = get_last_record(cursor, table)
        radio_state = last_record[13]
        if radio_state == 0:
            if last_record:
                current_amounts = last_record[1:5]
                state_amounts = last_record[5:9]
                triger_state = last_record[9:13]
                #lamda = last_record[14]
                timestamp = datetime.datetime.utcnow() + datetime.timedelta(
                    hours=2
                )  # Adjusting for UTC+3
                zapis("radio_state", radio_state, table, timestamp)
                #zapis("lamda", lamda, table, timestamp)
                for i, value in enumerate(current_amounts, start=1):
                    zapis(f"current_amount_{i}", float(value), table, timestamp)
                for i, value in enumerate(state_amounts, start=1):
                    zapis(f"state_amount_{i}", value, table, timestamp)
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
