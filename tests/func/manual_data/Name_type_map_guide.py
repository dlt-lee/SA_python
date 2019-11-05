# -*- coding: utf-8 -*-
import re
import pymysql
import csv
import datetime

# Setup Mysql connection
mysql_con = pymysql.connect(host="rm-2zet5lw17as40fty28o.mysql.rds.aliyuncs.com",
                            user="snowball", password="MEDOsnow$%^&",
                            db="medo_master", charset='utf8')

# fail number
fail_num = 0
# pass number
pass_num = 0
file = open("Name_type_map_guide.txt", "w")
#Scenario:
#Check whether ttime and time format in manual_association
##########################################################################################
#Given:
#Open manual_association
# set cursor to execute sql
mysql_cursor = pymysql.cursors.Cursor(mysql_con)
# check medmeeting_index
mysql_cursor.execute("select * from manual_guide")
#get list name
list_name = mysql_cursor.description
des_name = []
for i in range(len(list_name)):
        des_name.append(list_name[i][0])
#write list name to csv
with open('Name_type_map_guide.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(des_name)
############################################################################################
while True:
    # When:
    # Get data form database
    row = mysql_cursor.fetchone()
    # Assert no mapping
    map = False
    try:
        if bool(re.search(row[5], row[6])):
            map = True
            pass_num += 1
# Assert the rest file should be "共识"
        elif bool(re.match(u"共识", row[5])):
            map = True
        if not map:
            fail_num += 1
            # Then fail no mapping case and tore related iinormation for investigation
            with open('Name_type_map_guide.csv', 'a+', newline='') as csv_file:
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
