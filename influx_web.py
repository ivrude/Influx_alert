#app to send info to influx not from radiometr auto mut by hands
from flask import Flask, render_template, request, redirect, url_for
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS
from config import token_influx, url_influx

app = Flask(__name__)

# configuration InfluxDB
ORG = "Chornobyl"
BUCKET = "Graf"
TOKEN = token_influx
client = InfluxDBClient(url=url_influx, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=ASYNCHRONOUS)


# write to InfluxDB
def zapis(name, value):
    data = f"test_6,host=host3 Self_fon_{name}={value}"
    write_api.write(bucket=BUCKET, org=ORG, record=data)

# page whith table
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        value = request.form["value"]
        zapis(name, value)
        return redirect(url_for("index"))
    return render_template("index.html")

# sending info
@app.route("/send", methods=["POST"])
def send():
    data = request.form
    for (
        name,
        value,
    ) in data.items():
        zapis(name, value)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="localhost", port=5000)
