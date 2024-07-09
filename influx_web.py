from flask import Flask, render_template, request, redirect, url_for
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
from config import token_influx, url_influx
app = Flask(__name__)

# Конфігурація InfluxDB
token = token_influx
org = "Chornobyl"
bucket = "Graf"
client = InfluxDBClient(url=url_influx, token=token, org=org)
write_api = client.write_api(write_options=ASYNCHRONOUS)

# Функція для запису даних в InfluxDB
def zapis(name, value):
    data = f"test_6,host=host3 Self_fon_{name}={value}"
    write_api.write(bucket=bucket, org=org, record=data)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        value = request.form['value']
        zapis(name, value)
        return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.form
    for name, value, in data.items():
        zapis(name, value)
    return redirect(url_for('index'))


app.run(host='localhost', port=8000)