# Monitorer sa consommation d'énergie avec linky, liXee et Domoticz

<img  src="/Images/Peek 27-12-2022 21-34.gif" alt=" linky " />

# Installation des bibliothèques

`git clone https://github.com/onlinux/linky.git`

run:

`cd linky`

`$ sh setup.sh`

# Configuration

Modifier config.ini

<pre>
[MQTT]
MQTT_USERNAME= xxxxx # Enter username if exists
MQTT_PASSWORD= xxxxx # Enter password to access mqtt broker
MQTT_IP=192.168.0.64
MQTT_PORT=1883

[DOMOTICZ]
LINKY_IDX = 466 # Domoticz index of linky P1_METER
marqueeIdx = 27 # Domoticz index to be displayed within Marquee, here SONOFF POW
</pre>

# Start Thermostat Domoticz

`source venv/bin/activate`

`python3 linky.py`
