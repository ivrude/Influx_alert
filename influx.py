from datetime import datetime
from time import sleep

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS


token = "Xwx1R1lV2_dcGr2AvCDHPoRvpq90n5hlCwutM2Zw3ZQXKzmURxj1q6Vs1BQx9fIiL499NRDpzyZwW0Gv8uGnBA=="
org = "Chornobyl"
bucket = "Graf"


# Ініціалізація клієнта InfluxDB
client = InfluxDBClient(url="http://192.168.0.95:8086", token=token, org=org)

# Використання write_api для запису даних в асинхронному режимі
write_api = client.write_api(write_options=SYNCHRONOUS)

# Запис кожного значення зі списку l у базу даних
def zapis(name,value):
    data = f"test_3,host=host4 amount_radiation_{name}={value}"
    write_api.write(bucket=bucket, org=org, record=data)
zapis("AM",0)
zapis("BA",0)
zapis("CS",0)
zapis("CO",0)
zapis("TH",0)
zapis("CF",0)
zapis("PU",0)

# Закриття з'єднання з InfluxDB
client.close()