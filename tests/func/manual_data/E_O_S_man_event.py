# -*- coding: utf-8 -*-
import re
import pymysql
import csv
import  numpy as np
import pandas as pd

# Setup Mysql connection
mysql_con = pymysql.connect(host="rm-2zet5lw17as40fty28o.mysql.rds.aliyuncs.com",
                            user="snowball", password="MEDOsnow$%^&",
                            db="medo_master", charset='utf8')

mysql_cursor = mysql_con.cursor()
mysql_cursor.execute("select Event_Name as Event,Event_Sponsor as Sponsor from manual_event   group by Event_Sponsor")

event_sponsor = pd.DataFrame(mysql_cursor.fetchall())
print(event_sponsor[0].value_counts())


