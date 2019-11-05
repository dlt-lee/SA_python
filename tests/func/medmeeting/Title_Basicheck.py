# -*- coding: utf-8 -*-
import sys
import re
import pymysql
import csv

# Setup Mysql connection
mysql_con = pymysql.connect(host="rm-2zet5lw17as40fty28o.mysql.rds.aliyuncs.com",
                            user="snowball", password="MEDOsnow$%^&",
                            db="medo_master", charset='utf8')
# fail number
fail_num = 0
# pass number
pass_num = 0
file = open("Title_Basicheck.txt", "w")
#Scenario:
#Check if the title is English case or Chinese case
##########################################################################################
#Given:
#Open medmeeting_index
# set cursor to execute sql
mysql_cursor = pymysql.cursors.Cursor(mysql_con)
# check medmeeting_index
mysql_cursor.execute("select * from medmeeting_index")
#get list name
list_name=mysql_cursor.description
temp=[]
for i in range(len(list_name[0])):
        temp.append(list_name[i][0])
#write list name to csv
with open('Title_Basicheck.csv', 'w',newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(temp)
############################################################################################
while True:
    # When:
    # Get data form database
    row = mysql_cursor.fetchone()
    try:
        en_reg = re.compile(r'[A-Za-z]+')
        contain_en = bool(re.search(en_reg, row[1]))
    except TypeError:
        print()
    try:
        ch_reg = re.compile(u'[\u4e00-\u9fa5]+')
        contain_ch = bool(re.search(ch_reg, row[1]))
    except TypeError:
        print()
    if contain_en:
        pass_num += 1
    elif contain_ch:
        pass_num += 1
    else:
        fail_num += 1
        print(row)
        with open('Title_Basicheck.csv', 'a+',newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(row)
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

