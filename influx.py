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
    data = f"test_4,host=host3 {name}={value}"
    write_api.write(bucket=bucket, org=org, record=data)
zapis("State_1",2.15)
zapis("Current_1",4)
zapis("State_2",2.35)
zapis("Current_2",6)
zapis("State_3",2.1)
zapis("Current_3",2.30)
zapis("State_4",2.2)
zapis("Current_4",4.5)


# Закриття з'єднання з InfluxDB
client.close()