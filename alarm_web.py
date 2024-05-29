from flask import Flask, render_template
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

app = Flask(__name__)

# Задайте ваші параметри підключення
token = "Xwx1R1lV2_dcGr2AvCDHPoRvpq90n5hlCwutM2Zw3ZQXKzmURxj1q6Vs1BQx9fIiL499NRDpzyZwW0Gv8uGnBA=="
org = "Chornobyl"
bucket = "Graf"
url = "http://192.168.0.218:8086"

# Ініціалізація клієнта InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

# Функція для отримання останнього значення для вказаного поля
def fetch_last_value(field_name, host):
    query = f'''
    from(bucket: "{bucket}")
      |> range(start: -24h)
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

@app.route('/')
def index():
    host = 'host1'  # Ви можете змінити це значення або зробити його динамічним
    triggers = {}
    for i in range(1, 5):
        trigger_value = fetch_last_value(f"triger_{i}", host)
        if trigger_value is not None:
            triggers[f"trigger_{i}"] = trigger_value
        else:
            triggers[f"trigger_{i}"] = 0  # Встановіть значення за замовчуванням, якщо дані не знайдено

    return render_template('alarm.html', triggers=triggers)


app.run(debug=True)
