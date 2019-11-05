# -*- coding: utf-8 -*-
import pymysql
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
file = open("EventID_Index.txt", "w")
#Scenario:
#medmeeting_index & medmeeting_detail relationship
#The event_id of medmeeting_detail should be in medmeeting_index too
##########################################################################################
#Given:
#Open medmeeting_index
# set cursor to execute sql
mysql_cursor = pymysql.cursors.Cursor(mysql_con)
# check medmeeting_index
mysql_cursor.execute("select * from wf_data_article")
#get list name
list_name = mysql_cursor.description
print()
temp = []
for i in range(len(list_name)):
        temp.append(list_name[i][0])
#write list name to csv
with open('EventID_Index.csv', 'w',newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(temp)
############################################################################################
while True:
    # When:
    # Get data form database
    row = mysql_cursor.fetchone()
    try:
        str_reg = re.compile(r'[<em>]+')
        unclear_string = bool(re.search(str_reg, row[1]))
        if unclear_string:
            fail_num += 1
        else:
            with open('EventID_Index.csv', 'a+',newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(row)
            pass_num += 1
    except:
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
####################################################################

