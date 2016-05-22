#!/usr/bin/env python
# -*- coding: utf-8 -*-

print("--------------------------------")
print("-----------GrowPi 0.1-----------")
print("---Written by Baese Alexander---")
print("Power to all planters out there!")
print("----github.com/RelooM/GrowPi----")
print("--------------------------------")

local_node_id = 1

import RPi.GPIO as GPIO
import Adafruit_DHT as dht
from datetime import datetime
from datetime import timedelta
import local, cloud, sensors, relay, sync
#cloud = cloud.sync()
local = local.db()
cloud = cloud.db()
sync=sync.sync()
sensors = sensors.sensors()
relay = relay.relay()

#GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Nachricht = "Syncing configuration with cloud"
print("\033[1;32;40m " + str(datetime.now())[:19] + " " + Nachricht)
local.log("Info", "Configuration", Nachricht)

sync.start(local_node_id);
humidity, temperature = sensors.read_air();
#sensors.read_moisture
relay.check(humidity, temperature, local_node_id);
print("\033[1;37;40m ")

