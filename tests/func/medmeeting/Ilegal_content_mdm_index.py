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
file = open("Ilegal_content_mdm_index.txt", "w")
#Scenario:
#Check if the speaker have report name
##########################################################################################
#Given:
#Open medmeeting_detail
# set cursor to execute sql
mysql_cursor = pymysql.cursors.Cursor(mysql_con)
# check medmeeting_detail
mysql_cursor.execute("select * from medmeeting_index")
#get list name
list_name=mysql_cursor.description
temp=[]
for i in range(len(list_name)):
        temp.append(list_name[i][0])
#write list name to csv
with open('Ilegal_content_mdm_index.csv', 'w',newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(temp)
############################################################################################
while True:
    # When:
    # Get data form database
    row = mysql_cursor.fetchone()
    contain_context = False

    try:
        if bool(re.search("会议简介", row[3])) or row[5] is "":
            contain_context = True

        if contain_context:
            pass_num += 1
        else:
            fail_num += 1
            with open('Ilegal_content_mdm_index.csv', 'a+', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(row)
    except Exception as e:
        print(e)
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

