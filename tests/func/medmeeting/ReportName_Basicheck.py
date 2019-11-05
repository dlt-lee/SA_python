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
file = open("ReportName_Basicheck.txt", "w")
#Scenario:
#Check if the speaker have report name
##########################################################################################
#Given:
#Open medmeeting_index
# set cursor to execute sql
mysql_cursor = pymysql.cursors.Cursor(mysql_con)
# check medmeeting_detail
mysql_cursor.execute("select * from medmeeting_detail")
#get list name
list_name=mysql_cursor.description
temp=[]
for i in range(len(list_name[0])):
        temp.append(list_name[i][0])
#write list name to csv
with open('ReportName_Basicheck.csv', 'w',newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(temp)
############################################################################################
while True:
    # When:
    # Get data form database
    row = mysql_cursor.fetchone()
    try:
        if bool(re.match("讲者", row[4])):
            if row[5] is "":
                fail_num += 1
                with open('ReportName_Basicheck.csv', 'a+', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(row)
            else:
                pass_num += 1
    except:
        pass
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

