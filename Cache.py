import sqlite3
from datetime import datetime
from time import sleep
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Параметри підключення до InfluxDB
token = "Xwx1R1lV2_dcGr2AvCDHPoRvpq90n5hlCwutM2Zw3ZQXKzmURxj1q6Vs1BQx9fIiL499NRDpzyZwW0Gv8uGnBA=="
org = "Chornobyl"
bucket = "Graf"
url = "http://192.168.0.95:8086"

# Ініціалізація клієнта InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Створення локальної бази даних SQLite
conn = sqlite3.connect('local_cache.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS data_cache
             (id INTEGER PRIMARY KEY, measurement TEXT, field TEXT, value REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

def zapis(name, value):
    data = f"test_4,host=host3 amount_{name}={value}"
    try:
        write_api.write(bucket=bucket, org=org, record=data)
        print(f"Data written to InfluxDB: {name}={value}")
    except Exception as e:
        print(f"Failed to write to InfluxDB, caching locally: {e}")
        c.execute("INSERT INTO data_cache (measurement, field, value) VALUES (?, ?, ?)", ("test_4", f"amount_{name}", value))
        conn.commit()

def resend_cached_data():
    c.execute("SELECT * FROM data_cache")
    rows = c.fetchall()
    for row in rows:
        try:
            data = f"{row[1]},host=host3 {row[2]}={row[3]}"
            write_api.write(bucket=bucket, org=org, record=data)
            c.execute("DELETE FROM data_cache WHERE id=?", (row[0],))
            conn.commit()
            print(f"Resent cached data to InfluxDB: {row[2]}={row[3]}")
        except Exception as e:
            print(f"Failed to resend cached data: {e}")
            break

# Приклад запису даних
zapis("high_radiation", 23)
zapis("high_electr", 35)
zapis("low_radiation", 12)
zapis("low_electr", 32)

zapis("high_radiation", 27)
zapis("high_electr", 8)
zapis("low_radiation", 12)
zapis("low_electr", 32)

# Періодична перевірка та повторна відправка даних
while True:
    resend_cached_data()
    sleep(60)  # Перевіряємо кожну хвилину

# Закриття з'єднання з InfluxDB та SQLite
client.close()
conn.close()