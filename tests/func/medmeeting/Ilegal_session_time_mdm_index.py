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
file = open("Ilegal_session_time_mdm_detail.txt", "w")
#Scenario:
#Check if the speaker have report name
##########################################################################################
#Given:
#Open medmeeting_detail
# set cursor to execute sql
mysql_cursor = pymysql.cursors.Cursor(mysql_con)
# check medmeeting_detail
mysql_cursor.execute("select * from medmeeting_detail")
#get list name
list_name=mysql_cursor.description
temp=[]
for i in range(len(list_name)):
        temp.append(list_name[i][0])
#write list name to csv
with open('Ilegal_session_time_mdm_detail.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(temp)
############################################################################################
while True:
    # When:
    # Get data form database
    row = mysql_cursor.fetchone()
    contain_time = True

    try:
        en_reg = re.compile(r'[A-Za-z]+')
        cn_reg = re.compile(u"[\u4e00-\u9fa5]+")
        if bool(re.search(en_reg, row[9])):
            contain_time = False
        elif bool(re.search(cn_reg, row[9])):
            contain_time = False
        if contain_time:
            pass_num += 1
        else:
            fail_num += 1
            with open('Ilegal_session_time_mdm_detail.csv', 'a+', newline='') as csv_file:
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