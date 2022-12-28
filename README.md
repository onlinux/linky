# Monitor linky

<img  src="/Images/Peek 27-12-2022 21-34.gif" alt=" linky " />

# Installation libraries

`git clone https://github.com/onlinux/linky.git`

run:

`cd linky`

`$ sh setup.sh`

# Configuration

Modify config.ini

<pre>
[MQTT]
MQTT_USERNAME= xxxxx # Enter username if exists
MQTT_PASSWORD= xxxxx # Enter password to access mqtt broker
MQTT_IP=192.168.0.64
MQTT_PORT=1883

[DOMOTICZ]
# Domoticz index of linky P1_METER
LINKY_IDX = 466
# Domoticz index to be displayed within Marquee, here SONOFF POW
marqueeIdx = 27
</pre>

# Start Thermostat Domoticz

`source venv/bin/activate`

`python3 z2.py`
