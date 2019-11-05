# -*- coding: utf-8 -*-
import pymysql
import numpy as np
import re
import csv

# Setup Mysql connection
mysql_con = pymysql.connect(host="rm-2zet5lw17as40fty28o.mysql.rds.aliyuncs.com",
                            user="snowball", password="MEDOsnow$%^&",
                            db="medo_master", charset='utf8')

# fail number
fail_num = 0
# pass number
pass_num = 0
file = open("EventID_in_mdm_detail_index.txt", "w")
#Scenario:
#Check if the event ID is both medmeeting_detail and medmeting_index
##########################################################################################
#Given:
#Open medmeeting_detail
# set cursor to execute sql
mysql_cursor_index = pymysql.cursors.Cursor(mysql_con)
mysql_cursor_detail = pymysql.cursors.Cursor(mysql_con)
mysql_cursor_detail.execute("select Event_ID from medmeeting_detail")
mysql_cursor_index.execute("select Event_ID from medmeeting_index")
############################################################################################
#When: EventID from medmeeting_index and medmeeting_detail
Event_ID_index = mysql_cursor_index.fetchall()
Event_ID_detail = mysql_cursor_detail.fetchall()
#Then: find the all EventID in medmeeting_detail but not in medmeeting_index
Event_ID_diff = np.setdiff1d(Event_ID_detail, Event_ID_index)
fail_num = len(Event_ID_diff)
pass_num = len(Event_ID_index) - fail_num
print("Fail:%s" % fail_num)
print("Pass:%s" % pass_num)
file.write("Fail:%s\n" % fail_num)
file.write("Pass:%s\n" % pass_num)
file.close()
#write list name to csv
with open('EventID_in_mdm_detail_index.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(Event_ID_diff)
mysql_cursor_index.close()
mysql_cursor_detail.close()
mysql_con.close()
####################################################################
