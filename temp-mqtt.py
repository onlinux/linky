#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Author: Eric Vandecasteele (c)2022
# http://blog.onlinux.fr
#
#
# Import required Python libraries
#
#
import traceback
import os
import time
import logging
import logging.config
import signal
import sys
import getopt
import threading
import pygame
import colors
from PiTft import PiTft
import pprint
import paho.mqtt.client as mqtt  # type: ignore
import json
import fnmatch
import configparser
from icon import Icon

hostname = os.uname().nodename
pp = pprint.PrettyPrinter(indent=4)

# Constants
SABLIER_XPOS = 390
SABLIER_YOFFSET = 10
# os.path.realpath returns the canonical path of the specified filename,
# eliminating any symbolic links encountered in the path.

path = script_dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
configuration_file = script_dir + "/configtemp.ini"

logging.config.fileConfig(
    configuration_file,
    defaults={"logfilename": script_dir + "/temp.log"},
    disable_existing_loggers=False,
)

# Global variables
mqttUserName = ""
mqttPassword = ""
mqttIp = ""
mqttPort = ""
topics = ""
outdoorTemp = 0
indoorTemp = "0"
rssi = 0
idx = 466  # default idx LINKY P1_M
tidx = 27  # default idx which will be displayed in marquee. Here SONOFF POW idx
title = "indoorTemp"  # default caption
displayClock = True
noFrame = False
lastUpdateTime = ""
animation = False
angle = 0


def parseArg():
    global idx, title, displayClock, noFrame

    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "fhni:t:", ["noframe", "help", "noclock", "idx=", "title="]
        )
        logging.debug(str(opts))
        logging.debug(str(args))
    except getopt.error as err:
        # output error, and return with an error code
        logging.error(str(err))
        logging.error(
            "ERROR parsing argv  {} [--noframe] [--noclock] [--help] -i <idx> -t <title>".format(
                sys.argv[0]
            )
        )
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(
                "{} [--noframe] [--noclock] [--help] -i <idx> -t <title>".format(
                    sys.argv[0]
                )
            )
            logging.debug(
                "{} [--noframe] [--noclock] [--help] -i <idx> -t <title>".format(
                    sys.argv[0]
                )
            )
            sys.exit()
        elif opt in ("-i", "--idx"):
            idx = int(arg)
            logging.debug("idx is " + arg)
        elif opt in ("-t", "--title"):
            title = arg
            logging.debug("title is ' + title")
        elif opt in ("-n", "--noclock"):
            displayClock = False
            logging.debug("clock is " + str(displayClock))
        elif opt in ("-f", "--noframe"):
            noFrame = True
            logging.debug("noFrame is " + str(noFrame))
        else:
            return


def get_config(file):
    logging.debug("Get configuration from %s", file)

    if os.path.isfile(file):
        try:
            config = configparser.ConfigParser()
            config.read(file)
            global mqttUserName
            global mqttPassword
            global mqttIp
            global mqttPort
            global topics

            global index
            logging.debug("Get variable MQTT")
            mqttUserName = config.get("MQTT", "MQTT_USERNAME")
            mqttPassword = config.get("MQTT", "MQTT_PASSWORD")
            mqttIp = config.get("MQTT", "MQTT_IP")
            mqttPort = config.get("MQTT", "MQTT_PORT")
            topics = [config.get("Topics", topic) for topic in config.options("Topics")]

        except configparser.Error as err:
            logging.error("ConfigParser: %s", err)

    else:
        logging.critical("get_config %s is not accessible", file)
        sys.exit(1)


def blitRotate(image, pos, originPos, angle):
    # offset from pivot to center
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # rotated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # rotated image center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # Return the rotated image and shifted rect.
    return rotated_image, rotated_image_rect


def triggerAnimation():
    global angle, animation
    animation = True
    angle = 0


def on_connect(client, userdata, flag, rc):
    global hostname
    global mqttIp
    global topics
    logging.debug("{} connecting with result code {} ".format(hostname, str(rc)))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    if rc == 0:
        logging.info("{} connected to broker @ {} rc {}".format(hostname, mqttIp, rc))
        for topic in topics:
            client.subscribe(topic, 1)
        # client.subscribe(TOPIC)
    else:
        logging.error(
            "{} connection error  to broker @ {} rc {}".format(hostname, mqttIp, rc)
        )


def on_message(client, userdata, msg):
    RenderThreadMqtt(msg, "TEMPERATURE").start()


# Create an instance of the PiTft class
scope = PiTft(title=title, no_frame=noFrame, display_clock=displayClock)
scope.clear()
lcd = scope.screen


def renderTemp():
    logging.debug(" Render Temperature display ")
    global lcd
    width, _ = lcd.get_size()
    textAnchorX = 0
    textAnchorY = 0

    # Render outdoorTemp
    outdoorTempStr = "{:.1f}".format(round(float(outdoorTemp), 1)) + "°C "
    # color = colors.RED if float(outdoorTemp) > 27.0 else colors.DARKORANGE
    # color = colors.GREEN if float(outdoorTemp) < 23.0 else color
    color = colors.outdoor_temp_to_rgb(float(outdoorTemp))
    logging.debug("outdoor ")
    logging.debug( color)
    text = fontTemp.render(outdoorTempStr, True, color)
    size = fontTemp.size(outdoorTempStr)
    textrect = text.get_rect()
    textrect.topleft = (5, textAnchorY)

    # clear left side
    rect = [(textAnchorX, textAnchorY), (width, size[0] / 2)]
    lcd.fill(colors.BLACK, rect)
    # render outdoorTemp string
    lcd.blit(text, textrect)
    # Render Last update
    timeStr = lastUpdateTime
    text = fontTemp.render(timeStr, True, colors.WHITE)
    textrect.topleft = (230, textAnchorY)
    lcd.blit(text, textrect)
    # Display Alarm Icon
    lcd.blit(iconAlarmClockBitmap, (SABLIER_XPOS, textAnchorY + SABLIER_YOFFSET))
    # Render RSSI
    index = int(rssi) // 2 - 1  # get the right icon index
    lcd.blit(iconSignal[index].bitmap, (430, textAnchorY + 3))
    # Render indoorTemp
    textAnchorY = +size[1] + 15
    size = fontTempHuge.size(indoorTemp)
    rect = [(textAnchorX, textAnchorY), (width, size[1])]


    color = colors.indoor_temp_to_rgb(float(indoorTemp))
    logging.debug("INDOOR")
    logging.info(color)
    textBlack = fontTempHuge.render(indoorTemp + "°C", True, colors.BLACK)
    text = fontTempHuge.render(indoorTemp + "°C", True, color)
    textrect = text.get_rect()
    textrect.center = (width // 2, textAnchorY + size[1] // 2 - 6)

    # Création effet mise à jour pendant 0,5 seconde
    # lcd.fill(colors.WHITE, rect)
    # lcd.blit(textBlack, textrect)

    #pygame.display.update()

    # time.sleep(0.5)
    # # Affiche text
    lcd.fill(colors.BLACK, rect)
    lcd.blit(text, textrect)

    #pygame.display.update()

    triggerAnimation()


def handler(signum=None, frame=None):
    logging.debug(" Signal handler called with signal " + str(signum))
    time.sleep(1)  # here check if process is done
    logging.debug(" Wait done")
    pygame.display.quit()
    pygame.quit()
    client.disconnect()  # disconnect
    client.loop_stop()  # stop loop
    sys.exit(0)


for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
    logging.debug(" Registering handler for signal %s" % (sig))
    signal.signal(sig, handler)


class RenderTimeThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        width, height = lcd.get_size()
        margin = 0
        textAnchorX = 0
        textAnchorY = 0
        text = fontTime.render(time.strftime("%H:%M:%S"), True, colors.GREY)
        # Get height of the screen
        textHeight = text.get_height()
        textAnchorY = height - textHeight - margin
        rect = [(textAnchorX, textAnchorY), (width, textAnchorY)]
        # Display time on bottom line of screen
        textrect = text.get_rect()
        textrect.center = (lcd.get_width() // 2, textAnchorY + textHeight // 2)
        lcd.fill(colors.BLACK, rect)
        lcd.blit(text, textrect)


class RenderThreadMqtt(threading.Thread):
    def __init__(self, msg, what):
        threading.Thread.__init__(self)
        self.msg = msg
        self.what = what

    def run(self):
        global outdoorTemp
        global rssi
        global indoorTemp
        global lastUpdateTime
        global marquee
        try:
            topic = self.msg.topic
            payload = json.loads(self.msg.payload)
            logging.debug(topic, payload)
            if topic == "zigbee2mqtt/salle-a-manger_probe":
                lastUpdateTime = time.strftime("%H:%M")
                rssi = str(int(payload["linkquality"] / 35))
                indoorTemp = str(payload["temperature"])
            elif topic == "rtl_433/events/133":
                outdoorTemp = str(payload["temperature_C"])

            renderTemp()            
            
        except ValueError:
            logging.warning(" %s MQTT ERROR " % (threading.current_thread()))


parseArg()
get_config(configuration_file)

icons = []  # This list gets populated at startup
iconPath = path + "/icons"  # Sub-directory containing UI bitmaps (PNG format)
iconSignal = []
iconSignal.append(Icon(path, "/icons/S1-46"))
iconSignal.append(Icon(path, "/icons/S2-46"))
iconSignal.append(Icon(path, "/icons/S3-46"))
iconSignal.append(Icon(path, "/icons/S4-46"))
iconSignal.append(Icon(path, "/icons/S5-46"))

iconAlarmClockBitmap = Icon(path, "/icons/antenna-5-32").bitmap
w, h = iconAlarmClockBitmap.get_size()
pygame.display.set_icon(Icon(path, "/icons/flash").bitmap)

# Load all icons at startup.
for file in os.listdir(iconPath):
    if fnmatch.fnmatch(file, "*.png"):
        icons.append(Icon(iconPath, file.split(".")[0]))
# Assign Icons to Buttons, now that they're loaded

# set up the fonts
fontpath = pygame.font.match_font("dejavusansmono")
zfontpath = path + "/fonts/HandelGotD.ttf"
logging.debug(" zfontpath %s" % (zfontpath))
logging.debug(" fontpath %s" % (fontpath))
# set up 2 sizes
font = pygame.font.Font(fontpath, 28)
fontMono36 = pygame.font.Font(fontpath, 36)
fontTemperature = pygame.font.Font(fontpath, 40)
fontTime = pygame.font.Font(fontpath, 100)
fontTitle = pygame.font.Font(zfontpath, 48)
fontTempHuge = pygame.font.Font(zfontpath, 150)
fontTemp = pygame.font.Font(zfontpath, 50)

updateRate = 60 * 5  # kWh update interval in seconds
running = True  # define a variable to control the main loop
# marquee = Marquee(fontTitle, colors.DARKSLATEGREY, speed=2, ry=135 * 1.5)
# marquee.addMsg("En attente de message...", colors.DARKSLATEGREY, name="indoorTemp")

# Create time event for updating kWh
# updatekWh_event = pygame.USEREVENT + 1
# pygame.time.set_timer(updatekWh_event, 60 * 1000 * 5)

if displayClock:  # Create a timer for updating the clock
    clock_event = pygame.USEREVENT + 2
    pygame.time.set_timer(clock_event, 1000)

# threading.Thread(target=getStatus, args=(idx,)).start()

clock = pygame.time.Clock()

try:
    # Setup MQTT connection and start loop
    client = mqtt.Client("TEMPERATURE {}".format(hostname))
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username=mqttUserName, password=mqttPassword)
    client.connect(mqttIp, port=int(mqttPort), keepalive=60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_start()
except:
    logging.critical("Something get wrong when connecting to Mqtt broker")
    traceback.print_exc()
    sys.exit(1)

try:
    while running:
        # pygame.draw.rect(lcd, 0, marquee.getRect())
        # marquee.update()
        # event = pygame.event.wait()
        if animation:
            # print ('Angle', angle)

            if angle == 0:
                rotated_image, rect = blitRotate(
                    iconAlarmClockBitmap,
                    (SABLIER_XPOS + w / 2, h / 2 + SABLIER_YOFFSET),
                    (w / 2, h / 2),
                    angle,
                )

            if angle >= 360:
                animation = False
                angle = 0
                # Display original image
                lcd.fill(colors.BLACK, rect)
                lcd.blit(iconAlarmClockBitmap, (SABLIER_XPOS, SABLIER_YOFFSET))

            lcd.fill(colors.BLACK, rect)
            rotated_image, rect = blitRotate(
                iconAlarmClockBitmap,
                (SABLIER_XPOS + w / 2, h / 2 + SABLIER_YOFFSET),
                (w / 2, h / 2),
                angle,
            )
            lcd.blit(rotated_image, rect)
            angle += 10

        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            elif displayClock and event.type == clock_event:
                RenderTimeThread().start()
                pygame.display.set_caption(
                    "{} FPS: {:.1f}".format(title, clock.get_fps())
                )

            pressed_keys = pygame.key.get_pressed()

            if pressed_keys[pygame.K_ESCAPE]:
                print("K_ESCAPE")
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("screen pressed")  # for debugging purposes
                pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                print(pos)  # for checking

        pygame.display.update()
        clock.tick(5)

finally:
    logging.info("{} Quit".format(hostname))
    pygame.quit()
