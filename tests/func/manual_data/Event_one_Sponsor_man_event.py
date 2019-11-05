# -*- coding: utf-8 -*-
import re
import pymysql
import csv
import  numpy as np

# Setup Mysql connection
mysql_con = pymysql.connect(host="rm-2zet5lw17as40fty28o.mysql.rds.aliyuncs.com",
                            user="snowball", password="MEDOsnow$%^&",
                            db="medo_master", charset='utf8')

# fail number
fail_num = 0
# pass number
pass_num = 0
n = 1
# Case rsult storage
file = open("Event_one_Sponsor_man_event.txt", "w")
####################################################################
#Scenario:
#check whether Asso_Name has English or Chinese
####################################################################
#Given:
#Open manual_association
# set cursor to execute sql
#mysql_cursor = pymysql.cursors.Cursor(mysql_con)
mysql_cursor_event = mysql_con.cursor()
mysql_cursor_sponsor = mysql_con.cursor()
# check manual_association
#mysql_cursor.execute("select * from manual_event")
mysql_cursor_event.execute("select Event_Name,Event_Sponsor,count(*) as counts from manual_event group by Event_Name")
#####################################################################
#Get Event_Name
list_event = mysql_cursor_event.fetchall()
for event in list_event:
    sql = "select Event_Sponsor,count(*) as counts from manual_event  where Event_Name = '{0}' group by Event_Sponsor".format(event[0])
    mysql_cursor_sponsor.execute(sql)
    if len(mysql_cursor_sponsor.fetchall()) > 1:
        fail_num += 1
        print(event)
