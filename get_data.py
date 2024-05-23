from influxdb_client import InfluxDBClient
from influxdb_client.client.query_api import QueryApi

# Задайте ваші параметри підключення
from influxdb_client.client.write_api import SYNCHRONOUS

token = "Xwx1R1lV2_dcGr2AvCDHPoRvpq90n5hlCwutM2Zw3ZQXKzmURxj1q6Vs1BQx9fIiL499NRDpzyZwW0Gv8uGnBA=="
org = "Chornobyl"
bucket = "Graf"
url = "http://192.168.0.95:8086"

# Ініціалізація клієнта InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()
write_api = client.write_api(write_options=SYNCHRONOUS)

# Функція для отримання останнього значення для вказаного поля
def fetch_last_value(field_name):
    query = f'from(bucket: "{bucket}") |> range(start: -6h) |> filter(fn: (r) => r["_measurement"] == "test_4" and r["_field"] == "{field_name}") |> last()'
    tables = query_api.query(org=org, query=query)
    for table in tables:
        for record in table.records:
            return record.get_value()
    return None
def zapis(name,value):
    data = f"test_4,host=host3 {name}={value}"
    write_api.write(bucket=bucket, org=org, record=data)
# Отримання останніх значень для "high_radiation" і "high_electr"
def triger(number):
    Current = fetch_last_value(f"Current_{number}")
    State = fetch_last_value(f"State_{number}")
    print(Current)
    print(State)
    if Current > 2 * State and Current< 3 * State:
        zapis(f"triger_{number}",2)
    elif Current > 3 * State:
        zapis(f"triger_{number}",3)
    else :
        zapis(f"triger_{number}",1)

triger(1)
triger(2)
triger(3)
triger(4)

# Закриття з'єднання з InfluxDB
client.close()