#!/usr/bin/env python
# -*- coding: utf-8 -*-


import mysql.connector as mysql
from datetime import datetime


DBHost = "159.122.221.242"
DBUser = "Node"
DBPass = "n3[#|*8 <'3\?Ov"
DBName = "GrowPi"

database = mysql.connect(host=DBHost, user=DBUser, password=DBPass, database=DBName)
cur = database.cursor()

class db():

	#Read cloud config data
	def config(self, local_node_id):

		try:

			sql = ("""INSERT INTO Log (Timestamp, Level, Module, Message) VALUES (\"%s\",\"%s\",\"%s\",\"%s\")""" % (Zeit, Level, Modul, Nachricht))

			cursor.execute(sql)
			
			cur.execute("""SELECT `IP-address`, `Netmask`, `Subnet`, `Gateway`, `Hostname`, `Threshold_humidity_min`, `Threshold_humidity_max`, `Threshold_temperature_max`, `Threshold_temperature_min` FROM Node_config where Node_ID = %s""" % (local_node_id))
			row = cur.fetchone()
			while row is not None:
				cloudip=row[0]
				cloudnetmask=row[1]
				cloudsubnet=row[2]
				cloudgateway=row[3]
				cloudhostname=row[4]
				cloud_hu_min=row[5]
				cloud_hu_max=row[6]
				cloud_te_max=row[7]
				cloud_te_min=row[8]
				row = cur.fetchone()
				
			
			return cloudip, cloudnetmask, cloudsubnet, cloudgateway, cloudhostname, cloud_hu_min, cloud_hu_max, cloud_te_max, cloud_te_min

		except mysql.Error as error:

			print("Error: {}".format(error))
			
		

