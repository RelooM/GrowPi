#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import Adafruit_DHT as dht
from datetime import datetime
from datetime import timedelta
import local


local = local.db()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


Air_pin = 4

class sensors():


	def read_air(self):
		
		#Auslesen der Temperatur und Logging in SQL
		
		Nachricht = "Gathering air temperature and humidity from sensor"
		print("\033[1;32;40m " + str(datetime.now())[:19] + " " + Nachricht)
		local.log("Info", "Sensor", Nachricht)
		
		humidity, temperature = dht.read_retry(dht.DHT22, int(Air_pin))
		

		
		local.write_air_data(humidity, temperature)
		
		return humidity, temperature

