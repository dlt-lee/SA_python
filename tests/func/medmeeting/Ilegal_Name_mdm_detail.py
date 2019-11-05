# -*- coding: utf-8 -*-
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
n = 1
# Case rsult storage
file = open("Ilegal_Name_mdm_detail.txt", "w")
####################################################################
#Scenario:
#check whether Asso_Name has English or Chinese
####################################################################
#Given:
#Open manual_association
# set cursor to execute sql
mysql_cursor = pymysql.cursors.Cursor(mysql_con)
# check manual_association
mysql_cursor.execute("select * from medmeeting_detail")
#get list name
list_name = mysql_cursor.description
des_name = []
for i in range(len(list_name)):
        des_name.append(list_name[i][0])
#write list name to csv
with open('Ilegal_Name_mdm_detail.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(des_name)
#####################################################################
# When:
# Get data form database
while True:
    #set curser for reading
    row = mysql_cursor.fetchone()
    # set contain_name as False
    contain_name = False
    try:
        en_reg = re.compile(r'[A-Za-z]+')
        cn_reg = re.compile(u"[\u4e00-\u9fa5]+")
        if bool(re.search(en_reg, row[2])):
            contain_name = True
        elif bool(re.search(cn_reg, row[2])):
            contain_name = True
            if (len(row[2]) < 2) or len(row[2] > 4):
                contain_name = False
        if contain_name:
            pass_num += 1
        else:
            fail_num += 1
            with open('Ilegal_Name_mdm_detail.csv', 'a+', newline='') as csv_file:
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
