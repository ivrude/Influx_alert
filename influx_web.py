#app to send info to influx not from radiometr auto but by hands

from flask import Flask, render_template, request, redirect, url_for
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS
from config import token_influx, url_influx

app = Flask(__name__)

# Configuration InfluxDB
ORG = "Chornobyl"
BUCKET = "Graf"
TOKEN = token_influx
client = InfluxDBClient(url=url_influx, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=ASYNCHRONOUS)

# Write to InfluxDB
def zapis(name, value):
    data = f"test_6,host=host3 {name}={value}"
    write_api.write(bucket=BUCKET, org=ORG, record=data)

# Main page with table
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get data from the form
        kuzov = request.form.get("body")
        kolesa = request.form.get("wheels")
        dno_mashini = request.form.get("bottom")

        # Send each field to InfluxDB
        zapis("Кузов", kuzov)
        zapis("Колеса", kolesa)
        zapis("Дно_машини", dno_mashini)

        return redirect(url_for("index"))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
