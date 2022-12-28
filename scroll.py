#!/usr/bin/python
# -*- coding: utf-8 -*-
from inspect import Traceback
import pygame
import sys
import time
import threading
import os
import socket
import signal
import paho.mqtt.client as mqtt  # type: ignore
import json
import logging
import logging.config
import random
from Marquee import *
import configparser

TOPIC = [('domoticz/out', 0), ('domoticz/in', 0)]
# set up the colors
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREY = (211, 211, 211)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
MYGREEN = (0, 96, 65)
DARKORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
DARKGREEN = (0, 100, 0)
NAVY = (16, 22, 137)
LIGHTBLUE = (0, 113, 188)

path = os.path.dirname(os.path.realpath(sys.argv[0]))
logfile = path + '/scroll.log'

path = script_dir = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
configuration_file = script_dir + '/config.ini'
hostname = os.uname().nodename

logging.config.fileConfig(configuration_file, defaults={
                          'logfilename': logfile}, disable_existing_loggers=False)


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
            global index
            logging.debug("Get variable MQTT")
            mqttUserName = config.get('MQTT', 'MQTT_USERNAME')
            mqttPassword = config.get('MQTT', 'MQTT_PASSWORD')
            mqttIp = config.get('MQTT', 'MQTT_IP')
            mqttPort = config.get('MQTT', 'MQTT_PORT')
            id = config.get('DOMOTICZ', 'LINKY_IDX')
            if id:
                idx = id
                logging.debug("IDX is %s", idx)

        except configparser.Error as err:
            logging.error("ConfigParser: %s", err)

    else:
        logging.critical("get_config %s is not accessible", file)
        sys.exit(1)


def handler(signum=None, frame=None):
    global client
    logging.debug(' Signal handler called with signal ' + str(signum))
    time.sleep(0.5)  # here check if process is done
    logging.debug(' Wait done')
    pygame.display.quit()
    client.disconnect()  # disconnect
    client.loop_stop()  # type: ignore # stop loop
    sys.exit(0)


def beep():
    global beeps
    pygame.mixer.Sound.play(beeps)


for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
    logging.debug(' Registering handler for signal %s' % (sig))
    signal.signal(sig, handler)


def on_connect(client, userdata, flag, rc):
    global hostname
    global mqttIp
    logging.debug(
        "{} connected with result code {} ".format(hostname, str(rc)))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    if rc == 0:
        logging.info("{} connected to broker @ {} rc {}".format(
            hostname, mqttIp, rc))
        client.subscribe(TOPIC)
        logging.debug(str(TOPIC).strip('[]'))
    else:
        logging.error("{} connection error  to broker @ {} rc {}".format(
            hostname, mqttIp, rc))


def on_message(client, userdata, msg):
    global marquee1, marquee2, marquee3
    try:
        d = json.loads(msg.payload)
        # print(d)
        if 'CODE' in d and 'COTE' in d:
            stock[d['CODE']] = d

            for code in stock:
                print(code)
                d = stock[code]
                text = "{name:>6.6s} {v:>3.2f}E {variation:<6.6s}".format(
                    name=d['CODE'], v=float(d['COTE']), variation=d['VARIATION'])

                if 'VARIATION' in d and '%' in d['VARIATION'] and float(d['VARIATION'].strip('%')) > 0:
                    color = GREEN
                else:
                    color = RED

                marquee3.addMsg(text, color, name=d['CODE'])

        elif 'dtype' in d and 'Temp' in d['dtype']:
            if 'svalue1' in d:
                # print(">>>>>>>>>>>>>>>>>>>>>>>>> " + d['name'])
                text = d['name'] + " {v:>.1f}".format(v=float(d['svalue1']))
                text = text + u'\N{DEGREE SIGN}' + 'C'
                if float(d['svalue1']) > 26.0:
                    color = DARKORANGE
                elif float(d['svalue1']) > 15:
                    color = GREEN
                else:
                    color = LIGHTBLUE

                marquee1.addMsg(text, color, name=d['idx'])
                marquee1.speed = random.randint(2, 5)

        elif 'dtype' in d and d['dtype'] == 'Usage':
            beep()
            text = "Energie " + "{v:4.0f}W".format(v=float(d['svalue1']))
            # print("--------------------------- " +text)
            marquee2.addMsg(text, GREY, name=d['idx'])

        elif d['idx'] == 27:
            text = "SI " + \
                "{v:4.0f}W".format(v=float(d['svalue'].split(';')[0]))
            marquee2.addMsg(text, GREY, name=d['idx'])

    except ValueError:
        logging.warning(' %s MQTT ERROR ' % (threading.current_thread()))


def start_window():
    global running, marquee1, marquee2, marquee3
    global stock
    global beeps
    get_config(configuration_file)
    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
    beeps = pygame.mixer.Sound(path + "/sounds/TickerPoints.wav")

    # Text
    zfontpath = path + '/fonts/HandelGotD.ttf'
    fontTitle = pygame.font.Font(zfontpath, 24)
    font = pygame.font.SysFont("Arial", 64)

    info = pygame.display.Info()  # width and height
    w, h = info.current_w, info.current_h

    width = 1024
    height = 120
    screen = pygame.display.set_mode((width, height))
    screen.set_colorkey(BLACK)
    clock = pygame.time.Clock()

    try:
        # Setup MQTT connection and start loop
        client = mqtt.Client("SCROLL {}".format(hostname))
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
        Traceback.print_exc()
        sys.exit(1)

    marquee1 = Marquee(fontTitle, GREEN, speed=2, ry=10)
    marquee2 = Marquee(font, ry=50, color=GREY, speed=1)
    marquee3 = Marquee(fontTitle, ry=32,
                       color=GREY, speed=1, direction=1)

    while running:
        screen.fill(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and
                    event.key == pygame.K_ESCAPE):

                pygame.quit()
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                marquee1.reset()
                marquee3.reset()

        marquee1.update()
        marquee2.update()
        marquee3.update()

        clock.tick(60)
        pygame.display.update()
    return screen


running = True
marquee1 = None
marquee2 = None
marquee3 = None
stock = dict()
start_window()
