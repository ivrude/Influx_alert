import sqlite3
from time import sleep
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Параметри підключення до InfluxDB
token = "Xwx1R1lV2_dcGr2AvCDHPoRvpq90n5hlCwutM2Zw3ZQXKzmURxj1q6Vs1BQx9fIiL499NRDpzyZwW0Gv8uGnBA=="
org = "Chornobyl"
bucket = "Graf"
url = "http://192.168.0.218:8086"

# Ініціалізація клієнта InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Створення локальної бази даних SQLite для кешування
conn_cache = sqlite3.connect('local_cache.db')
c_cache = conn_cache.cursor()
c_cache.execute('''CREATE TABLE IF NOT EXISTS data_cache
                   (id INTEGER PRIMARY KEY, measurement TEXT, field TEXT, value REAL, host TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
conn_cache.commit()

# Функція для отримання останнього запису з таблиці
def get_last_record(cursor, table_name):
    query = f"SELECT * FROM {table_name} ORDER BY rowid DESC LIMIT 1"
    cursor.execute(query)
    return cursor.fetchone()

# Функція для запису даних в InfluxDB або кешування в разі невдачі
def zapis(name, value, host):
    data = f"test_4,host={host} {name}={value}"
    try:
        write_api.write(bucket=bucket, org=org, record=data)
        print(f"Data written to InfluxDB: {name}={value}")
    except Exception as e:
        print(f"Failed to write to InfluxDB, caching locally: {e}")
        c_cache.execute("INSERT INTO data_cache (measurement, field, value, host) VALUES (?, ?, ?, ?)", ("test_4", f"amount_{name}", value, host))
        conn_cache.commit()

# Функція для повторної відправки кешованих даних
def resend_cached_data():
    c_cache.execute("SELECT * FROM data_cache")
    rows = c_cache.fetchall()
    for row in rows:
        try:
            data = f"{row[1]},host={row[4]} {row[2]}={row[3]}"
            write_api.write(bucket=bucket, org=org, record=data)
            c_cache.execute("DELETE FROM data_cache WHERE id=?", (row[0],))
            conn_cache.commit()
            print(f"Resent cached data to InfluxDB: {row[2]}={row[3]}")
        except Exception as e:
            print(f"Failed to resend cached data: {e}")
            break

# Підключення до основної бази даних SQLite
conn = sqlite3.connect('Test.db')
cursor = conn.cursor()

# Список таблиць для обробки
tables = ['host1', 'host2', 'host3', 'host4']

# Запис останніх даних з кожної таблиці в InfluxDB
for table in tables:
    last_record = get_last_record(cursor, table)
    if last_record:
        current_amounts = last_record[:4]
        state_amounts = last_record[5:]
        for i, value in enumerate(current_amounts, start=1):
            zapis(f"current_amount_{i}", value, table)
        for i, value in enumerate(state_amounts, start=1):
            zapis(f"state_amount_{i}", value, table)

# Періодична перевірка та повторна відправка кешованих даних
while True:
    resend_cached_data()
    sleep(60)  # Перевіряємо кожну хвилину

# Закриття з'єднання з InfluxDB та SQLite
client.close()
conn_cache.close()
conn.close()