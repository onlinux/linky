# Monitorer sa consommation d'énergie 

Avec linky, liXee et Domoticz

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
MQTT_IP = <IP of mqtt broker>
MQTT_PORT = <mqtt broker PORT>

[DOMOTICZ]
DOMOTICZ_IP = <Domoticz server IP>
DOMOTICZ_PORT = <Domoticz server PORT>
LINKY_IDX = 466 # Domoticz index of linky P1_METER
marqueeIdx = 27 # Domoticz index to be displayed within Marquee, here SONOFF POW
</pre>

# Start linky.py

`source venv/bin/activate`

`python3 linky.py`
