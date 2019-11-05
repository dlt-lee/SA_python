# -*- coding: utf-8 -*-
import sys
import re
import pymysql
import csv
sys.path.append(r'../../')
from Tools import tools

# Setup Mysql connection
mysql_con = pymysql.connect(host="rm-2zet5lw17as40fty28o.mysql.rds.aliyuncs.com",
                            user="snowball", password="MEDOsnow$%^&",
                            db="medo_master", charset='utf8')

# fail number
fail_num = 0
# pass number
pass_num = 0
# log preparation
file = open("End_Time_format_man_event.txt", "w")
#Scenario:
#Check whether ttime and time format in manual_association
##########################################################################################
#Given:
#Open manual_association
# set cursor to execute sql
mysql_cursor = pymysql.cursors.Cursor(mysql_con)
# check medmeeting_index
mysql_cursor.execute("select * from manual_event")
#get list name
list_name = mysql_cursor.description
des_name = []
for i in range(len(list_name)):
        des_name.append(list_name[i][0])
#write list name to csv
with open('End_Time_format_man_event.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(des_name)
############################################################################################
while True:
    #When:
    #Get data form database
    row = mysql_cursor.fetchone()
    try:
        Fm_year,Fm_month,Fm_day = tools.time_check(row[12])
        if Fm_year and Fm_month and Fm_day:
            pass_num += 1
        else:
            fail_num += 1
            with open('End_Time_format_man_event.csv', 'a+', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(row)
    except Exception as e:
        print(e)
        print(row)
    if not row:
            break

print("Fail:%s" % fail_num)
print("Pass:%s" % pass_num)
file.write("Fail:%s\n" % fail_num)
file.write("Pass:%s\n" % pass_num)
file.close()
mysql_cursor.close()
mysql_con.close()
