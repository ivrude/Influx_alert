import sqlite3
from time import sleep

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

#app for sending status of trigers to influx
# Задайте ваші параметри підключення
token = "Xwx1R1lV2_dcGr2AvCDHPoRvpq90n5hlCwutM2Zw3ZQXKzmURxj1q6Vs1BQx9fIiL499NRDpzyZwW0Gv8uGnBA=="
org = "Chornobyl"
bucket = "Graf"
url = "http://192.168.0.52:8086"

# Ініціалізація клієнта InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()
write_api = client.write_api(write_options=SYNCHRONOUS)


conn = sqlite3.connect('Test_docker/Test.db')
cursor = conn.cursor()
# Список таблиць для обробки
tables = ['host1', 'host2', 'host3', 'host4']


# Функція для отримання останнього значення для вказаного поля
def fetch_last_value(field_name, host):
    query = f'''
    from(bucket: "{bucket}")
      |> range(start: -6h)
      |> filter(fn: (r) => r["_measurement"] == "test_5")
      |> filter(fn: (r) => r["_field"] == "{field_name}")
      |> filter(fn: (r) => r["host"] == "{host}")
      |> last()
    '''
    tables = query_api.query(org=org, query=query)
    for table in tables:
        for record in table.records:
            return record.get_value()
    return None

def zapis(name, value, host):
    data = f"test_5,host={host} {name}={value}"
    write_api.write(bucket=bucket, org=org, record=data)

# Отримання останніх значень для "high_radiation" і "high_electr"
def triger(number, host):
    Current = fetch_last_value(f"current_amount_{number}", host)
    State = fetch_last_value(f"state_amount_{number}", host)
    print(f"current_amount_{number}: {Current}")
    print(f"state_amount_{number}: {State}")
    if Current is not None and State is not None:
        if Current > 2 * State and Current < 3 * State:
            zapis(f"triger_{number}", 2, host)
        elif Current >= 3 * State:
            zapis(f"triger_{number}", 3, host)
        else:
            zapis(f"triger_{number}", 1, host)
    else:
        print(f"Failed to fetch data for Current_{number} or State_{number}")
while True:
    hosts = ['host1', 'host2', 'host3', 'host4']
    for host in hosts:
        for i in range(1, 5):
            triger(i, host)

    sleep(60)

# Закриття з'єднання з InfluxDB
client.close()
