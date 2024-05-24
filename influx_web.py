from flask import Flask, render_template, request, redirect, url_for
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS

app = Flask(__name__)

# Конфігурація InfluxDB
token = "Xwx1R1lV2_dcGr2AvCDHPoRvpq90n5hlCwutM2Zw3ZQXKzmURxj1q6Vs1BQx9fIiL499NRDpzyZwW0Gv8uGnBA=="
org = "Chornobyl"
bucket = "Graf"
client = InfluxDBClient(url="http://192.168.0.95:8086", token=token, org=org)
write_api = client.write_api(write_options=ASYNCHRONOUS)

# Функція для запису даних в InfluxDB
def zapis(name, value, host):
    data = f"test_4,host={host} State_{name}={value}"
    write_api.write(bucket=bucket, org=org, record=data)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        value = request.form['value']
        host = request.form['host']
        zapis(name, value, host)
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.form
    for name, value, host in data.items():
        zapis(name, value, host)
    return redirect(url_for('index'))


app.run(host='192.168.0.15', port=8000)