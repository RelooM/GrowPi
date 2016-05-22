#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector as mysql
from datetime import datetime


DBHost = "localhost"
DBUser = "GrowPi"
DBPass = "Y@vs4|B%Asl051H"
DBName = "GrowPi"

database = mysql.connect(host=DBHost, user=DBUser, password=DBPass, database=DBName)
cur = database.cursor()

class db():
	# Writing Log Message
	def log(self, Level, Module, Message):

		Timestamp = str(datetime.now())[:19]
		try:

			sql = ("""INSERT INTO Log (Timestamp, Level, Module, Message) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")""" % (Timestamp, Level, Module, Message))
			cur.execute(sql)
			database.commit()

		except mysql.Error as error:

			print("Error: {}".format(error))
			
	#Read local config data
	def get_config(self, option, local_node_id):
		
		if option == "all":
		
			try:

				sql = ("""SELECT * FROM Node_config where Node_ID = 1 %s""" % (local_node_id))
				cur.execute(sql)
				row = cur.fetchone()
				while row is not None:
				
					local_node_id=row[0]
					localip=row[1]
					localnetmask=row[2]
					localsubnet=row[3]
					localgateway=row[4]
					localhostname=row[5]
					local_hu_min=row[6]
					local_hu_max=row[7]
					local_te_max=row[8]
					local_te_min=row[9]
					row = cur.fetchone()
					
				
				return localip, localnetmask, localsubnet, localgateway, localhostname, local_hu_min, local_hu_max, local_te_max, local_te_min

			except mysql.Error as error:

				print("Error: {}".format(error))
		
		if option == "environment":
		
			try:
				
				sql = ("""SELECT `Threshold_humidity_min`, `Threshold_humidity_max`, `Threshold_temperature_max`, `Threshold_temperature_min` FROM Node_config where Node_ID = %s""" % (local_node_id))
				cur.execute(sql)
				row = cur.fetchone()
				while row is not None:
					
					local_hu_min=row[0]
					local_hu_max=row[1]
					local_te_max=row[2]
					local_te_min=row[3]
					row = cur.fetchone()
					
				return local_hu_min, local_hu_max, local_te_max, local_te_min

			except mysql.Error as error:

				print("Error: {}".format(error))
				
	def write_config(self, localip, localnetmask, localsubnet, localgateway, localhostname):

		try:

			cur.execute("SELECT `IP-address`, `Netmask`, `Subnet`, `Gateway`, `Hostname`, `Threshold_humidity_min`, `Threshold_humidity_max`, `Threshold_temperature_max`, `Threshold_temperature_min` FROM Node_config where Node_ID = 1")
			row = cur.fetchone()
			while row is not None:
				localip=row[0]
				localnetmask=row[1]
				localsubnet=row[2]
				localgateway=row[3]
				localhostname=row[4]
				local_hu_min=row[5]
				local_hu_max=row[6]
				local_te_max=row[7]
				local_te_min=row[8]
				row = cur.fetchone()
				
			
			return localip, localnetmask, localsubnet, localgateway, localhostname, local_hu_min, local_hu_max, local_te_max, local_te_min

		except mysql.Error as error:

			print("Error: {}".format(error))
			
	def write_air_data(self, humidity, temperature):

		Timestamp = str(datetime.now())[:19]
		try:

			sql = ("""INSERT INTO Temperature (Temperature, Timestamp) VALUES (\"%s\",\"%s\")""" % (str(temperature)[:2], Timestamp))
			cur.execute(sql)
			database.commit()

		except mysql.Error as error:

			print("Error: {}".format(error))	
		
		try:

			sql = ("""INSERT INTO Humidity (Humidity, Timestamp) VALUES (\"%s\",\"%s\")""" % (str(humidity)[:2], Timestamp))
			cur.execute(sql)
			database.commit()

		except mysql.Error as error:

			print("Error: {}".format(error))
			
	def update_status(self, option, state, local_node_id):
	
		if option == "humidifier":
			try:
				sql = ("""UPDATE `Node_config` SET `Status_humidifier`='%s' WHERE (`Node_ID`='%s')""" % (state, local_node_id))
				cur.execute(sql)
				database.commit()
				
			except mysql.Error as error:
				print("Error: {}".format(error))
			
		if option == "pump":
		
			try:
				sql = ("""UPDATE `Node_config` SET `Status_pump`='%s' WHERE (`Node_ID`='%s')""" % (state, local_node_id))
				cur.execute(sql)
				database.commit()
				
			except mysql.Error as error:
				print("Error: {}".format(error))
		
		if option == "light":
		
			try:
				sql = ("""UPDATE `Node_config` SET `Status_light`='%s' WHERE (`Node_ID`='%s')""" % (state, local_node_id))
				cur.execute(sql)
				database.commit()
				
			except mysql.Error as error:
				print("Error: {}".format(error))
		
		if option == "exhaust":
		
			try:
				sql = ("""UPDATE `Node_config` SET `Status_exhaust`='%s' WHERE (`Node_ID`='%s')""" % (state, local_node_id))
				cur.execute(sql)
				database.commit()
				
			except mysql.Error as error:
				print("Error: {}".format(error))
		
		if option == "ventilation":
		
			try:
				sql = ("""UPDATE `Node_config` SET `Status_ventilation`='%s' WHERE (`Node_ID`='%s')""" % (state, local_node_id))
				cur.execute(sql)
				database.commit()
				
			except mysql.Error as error:
				print("Error: {}".format(error))
