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



Pump_pin = 14
Light_pin = 15
Exhaust_pin = 18
Ventilation_pin = 23
Humidifier_pin = 24

GPIO.setup(int(Pump_pin), GPIO.OUT)
GPIO.setup(int(Light_pin), GPIO.OUT)
GPIO.setup(int(Exhaust_pin), GPIO.OUT)
GPIO.setup(int(Ventilation_pin), GPIO.OUT)
GPIO.setup(int(Humidifier_pin), GPIO.OUT)

class relay():


	def check(self, humidity, temperature, local_node_id):
	
		local_hu_min, local_hu_max, local_te_max, local_te_min = local.get_config("environment", local_node_id)

		if humidity < local_hu_min:
		
			GPIO.output(int(Humidifier_pin), GPIO.LOW)
			local.update_status("humidifier", "true", local_node_id)
			
			Nachricht = "Humidity is too low. Turning Humidifier on"
			print("\033[1;33;40m " + str(datetime.now())[:19] + " " + Nachricht)
			local.log("Minor", "Relay", Nachricht)
			 
		else:
			GPIO.output(int(Humidifier_pin), GPIO.HIGH)
			local.update_status("humidifier", "false", local_node_id)
		
		bool_prepath = "false"
			
		if temperature > local_te_max:
			if humidity > local_hu_max:
				GPIO.output(int(Exhaust_pin), GPIO.LOW)
				local.update_status("exhaust", "true", local_node_id)
			
				Nachricht = "Temperature and Humidity too high. Turning Exhaust on"
				print("\033[1;33;40m " + str(datetime.now())[:19] + " " + Nachricht)
				local.log("Minor", "Relay", Nachricht)
				
				bool_prepath = "true"
				
			else:
			
				GPIO.output(int(Exhaust_pin), GPIO.LOW)
				local.update_status("exhaust", "true", local_node_id)
				
				Nachricht = "Temperature is too high. Turning Exhaust on"
				print("\033[1;33;40m " + str(datetime.now())[:19] + " " + Nachricht)
				local.log("Minor", "Relay", Nachricht)
			
		if humidity > local_hu_max and bool_prepath == "false":
			GPIO.output(int(Exhaust_pin), GPIO.LOW)
			local.update_status("exhaust", "true", local_node_id)
			
			Nachricht = "Humidity is too high. Turning Exhaust on"
			print("\033[1;33;40m " + str(datetime.now())[:19] + " " + Nachricht)
			local.log("Minor", "Relay", Nachricht)
			
		else:
			GPIO.output(int(Exhaust_pin), GPIO.HIGH)
			local.update_status("exhaust", "false", local_node_id)