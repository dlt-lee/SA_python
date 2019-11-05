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
file = open("DID_Null_mdm_detail.txt", "w")
#Scenario:
#Check if the eachdoctors have their rwelated DID
##########################################################################################
#Given:
#Open medmeeting_detail
# set cursor to execute sql
mysql_cursor = pymysql.cursors.Cursor(mysql_con)
mysql_cursor.execute("select * from medmeeting_detail")
#get list name
list_name = mysql_cursor.description
temp = []
for i in range(len(list_name)):
        temp.append(list_name[i][0])
#write list name to csv
with open('DID_Null_mdm_detail.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(temp)
############################################################################################
while True:
    # When:
    # Get data form database
    row = mysql_cursor.fetchone()
    try:
        en_reg = re.compile(r'[A-Za-z]+')
        ch_reg = re.compile(u'[\u4e00-\u9fa5]+')
        contain_en = bool(re.search(en_reg, row[1]))
        contain_cn = bool(re.search(ch_reg, row[2]))
        if contain_en:
            pass
        elif contain_cn:
            if row[12] is "":
                # fail case if DID is NULL
                fail_num += 1
                with open('DID_Null_mdm_detail.csv', 'a+', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(row)
            else:
                pass_num += 1
    except Exception as e:
        print(e)
        #print(row)
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

