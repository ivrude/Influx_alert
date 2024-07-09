Cache.py - to send information from local db to influx
influx_web.py - feature to send information from "Dozimetrist" to influx in Grafana
main.py - start webhooks
start_doc.py - feature still working on it, u need to change container id on your own
stream video.py - capture frames from rtsp stream and send them on ip to capture then them again using grafana(still working on it).



config.py - add your own configs
structure:
token_influx = "your token"
url_influx = "influx ip:port"
rtsp_camrera = 'rtsp://user:password@ip:port'

to start grafana:

docker pull irudenkokiev/grafa:latest
admin | p@ssw0rd - to login

to start influx:

docker pull irudenkokiev/influx:latest
credentials to register for properly working scrypts
Ogranisation = "Chornobyl" | bucket = "Graf"

Make your own token whith all permisions and add it to:
Grafana -> datasources -> influxdb -> token reset -> save and test
config.py
