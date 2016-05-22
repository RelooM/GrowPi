#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import mysql.connector as mysql
import local
from datetime import datetime



local = local.db()


CloudDBHost = "159.122.221.242"
CloudDBUser = "Node"
CloudDBPass = "n3[#|*8 <'3\?Ov"
CloudDBName = "GrowPi"

cloud_db = mysql.connect(host=CloudDBHost, user=CloudDBUser, password=CloudDBPass, database=CloudDBName)
cloud_cur = cloud_db.cursor()

LocalDBHost = "localhost"
LocalDBUser = "GrowPi"
LocalDBPass = "Y@vs4|B%Asl051H"
LocalDBName = "GrowPi"

local_db = mysql.connect(host=LocalDBHost, user=LocalDBUser, password=LocalDBPass, database=LocalDBName)
local_cur = local_db.cursor()

class sync():
	
	
	def start(self, local_node_id):

		try:
	
			sql = ("""SELECT `IP-address`, `Netmask`, `Gateway`, `Hostname`, `Threshold_humidity_min`, `Threshold_humidity_max`, `Threshold_temperature_max`, `Threshold_temperature_min` FROM Node_config where Node_ID = %s""" % (local_node_id))
			local_cur.execute(sql)
			row = local_cur.fetchone()
			while row is not None:
				localip=row[0]
				localnetmask=row[1]
				localgateway=row[2]
				localhostname=row[3]
				local_hu_min=row[4]
				local_hu_max=row[5]
				local_te_max=row[6]
				local_te_min=row[7]
				row = local_cur.fetchone()

		except mysql.Error as error:

			print("Error: {}".format(error))
		
		try:

			Timestamp = str(datetime.now())[:19]
			sql = ("""SELECT `IP-address`, `Netmask`, `Gateway`, `Hostname`, `Threshold_humidity_min`, `Threshold_humidity_max`, `Threshold_temperature_max`, `Threshold_temperature_min` FROM Node_config where Node_ID = %s""" % (local_node_id))
			cloud_cur.execute(sql)
			
			row = cloud_cur.fetchone()
			while row is not None:
				cloudip=row[0]
				cloudnetmask=row[1]
				cloudgateway=row[2]
				cloudhostname=row[3]
				cloud_hu_min=row[4]
				cloud_hu_max=row[5]
				cloud_te_max=row[6]
				cloud_te_min=row[7]
				row = cloud_cur.fetchone()
				
		except mysql.Error as error:

				print("Error: {}".format(error))

		
		if (localip != cloudip or localnetmask != cloudnetmask or localgateway != cloudgateway or localhostname != cloudhostname):

			Nachricht = "Network settings differ from cloud. Changing system settings"
			print("\033[1;33;40m " + str(datetime.now())[:19] + " " + Nachricht)
			local.log("Minor", "Sync", Nachricht)
			
			localip=cloudip
			localnetmask=cloudnetmask
			localgateway=cloudgateway
			localhostname=cloudhostname
			
			ipchange = ("""sudo ifconfig enxb827ebccdd05 %s netmask %s""" % (localip, localnetmask))
			hostnamechange = ("""sudo hostname %s""" % (localhostname))
			gwchange = ("""sudo route add default gw %s enxb827ebccdd05""" % (localgateway))
			os.system('sudo ifconfig enxb827ebccdd05 down')
			os.system(hostnamechange)
			os.system(ipchange)
			os.system(gwchange)
			os.system('sudo ifconfig enxb827ebccdd05 up')
			
			try:

				Timestamp = str(datetime.now())[:19]
				sql = ("""UPDATE `Node_config` SET `IP-address`='%s', `Netmask`='%s', `Gateway`='%s', `Hostname`='%s' WHERE (`Node_ID`='%s')""" % (localip, localnetmask, localgateway, localhostname, local_node_id))
				local_cur.execute(sql)
				local_db.commit()				
				
				
				try:

					Timestamp = str(datetime.now())[:19]
					sql = ("""UPDATE `Node_config` SET `Last_update`='%s' WHERE (`Node_ID`='%s')""" % (Timestamp, local_node_id))
					cloud_cur.execute(sql)
					
				except mysql.Error as error:

					print("Error: {}".format(error))
				
			except mysql.Error as error:

				print("Error: {}".format(error))
			
		if (local_hu_min != cloud_hu_min or local_hu_max != cloud_hu_max or local_te_max != cloud_te_max or local_te_min != cloud_te_min):
			
			Nachricht = "Environment settings differ from cloud. Adjusting settings"
			print("\033[1;33;40m " + str(datetime.now())[:19] + " " + Nachricht)
			local.log("Minor", "Sync", Nachricht)
			
			local_hu_min=cloud_hu_min
			local_hu_max=cloud_hu_max
			local_te_max=cloud_te_max
			local_te_min=cloud_te_min
			try:

				Timestamp = str(datetime.now())[:19]
				sql = ("""UPDATE `Node_config` SET `Threshold_humidity_min`='%s', `Threshold_humidity_max`='%s', `Threshold_temperature_max`='%s', `Threshold_temperature_min`='%s' WHERE (`Node_ID`='%s')""" % (local_hu_min, local_hu_max, local_te_max, local_te_min, local_node_id))
				local_cur.execute(sql)
				local_db.commit()
				
				try:

					Timestamp = str(datetime.now())[:19]
					sql = ("""UPDATE `Node_config` SET `Last_update`='%s' WHERE (`Node_ID`='%s')""" % (Timestamp, local_node_id))
					cloud_cur.execute(sql)
					cloud_db.commit()
					
				except mysql.Error as error:

					print("Error: {}".format(error))
				
			except mysql.Error as error:

				print("Error: {}".format(error))
