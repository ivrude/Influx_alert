from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "Xwx1R1lV2_dcGr2AvCDHPoRvpq90n5hlCwutM2Zw3ZQXKzmURxj1q6Vs1BQx9fIiL499NRDpzyZwW0Gv8uGnBA=="
org = "Chornobyl"
bucket = "Graf"

# Ініціалізація клієнта InfluxDB
client = InfluxDBClient(url="http://192.168.0.52:8086", token=token, org=org)

# Використання write_api для запису даних в асинхронному режимі
write_api = client.write_api(write_options=SYNCHRONOUS)


# Запис кожного значення зі списку l у базу даних з кастомним timestamp
def zapis(name, value, timestamp=None):
    if timestamp is None:
        # If no custom timestamp is provided, use the current time in nanoseconds
        timestamp = int(datetime.utcnow().timestamp() * 1e9)
    else:
        # Convert the provided timestamp to nanoseconds if it is a datetime object
        if isinstance(timestamp, datetime):
            timestamp = int(timestamp.timestamp() * 1e9)

    # Create the line protocol string with the custom timestamp
    data = f"test_time,host=host1 {name}={value} {timestamp}"
    write_api.write(bucket=bucket, org=org, record=data)


# Example usage with custom timestamp
custom_timestamp = datetime(2024, 6, 19, 9, 16, 10, 113000)  # Custom datetime object
zapis("rad_status", 1, custom_timestamp)

# Example usage without custom timestamp (uses current time)


# Закриття з'єднання з InfluxDB
client.close()
