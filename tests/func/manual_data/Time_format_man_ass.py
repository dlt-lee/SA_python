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
# log preparation
file = open("Time_format_man_ass.txt", "w")
#Scenario:
#Check whether ttime and time format in manual_association
##########################################################################################
#Given:
#Open manual_association
# set cursor to execute sql
mysql_cursor = pymysql.cursors.Cursor(mysql_con)
# check medmeeting_index
mysql_cursor.execute("select * from manual_association")
#get list name
list_name = mysql_cursor.description
des_name = []
for i in range(len(list_name)):
        des_name.append(list_name[i][0])
#write list name to csv
with open('Time_format_man_ass.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(des_name)
############################################################################################
while True:
    #When:
    #Get data form database
    row = mysql_cursor.fetchone()
    try:
        Fm_year = False
        Fm_month = False
        Fm_day = False
        if len(row[12]) == 4:
            Fm_year = True
            Fm_month = True
            Fm_day = True
            if row[12] == "0000":
                Fm_year = False
        else:
            str_time = row[12].split("-")
            if len(str_time) == 2:
                Fm_day = True
                if bool(re.match(r"(\d{4})", str_time[0])):
                    Fm_year = True
                    if str_time[0] == "0000":
                        Fm_year = False
                if bool(re.match(r"(\d{2})", str_time[1])):
                    Fm_month = True
                    if str_time[1] == "00":
                        Fm_month = False
            elif len(str_time) == 3:
                if bool(re.match(r"(\d{4})", str_time[0])):
                    Fm_year = True
                    if str_time[0] == "0000":
                        Fm_year = False
                if bool(re.match(r"(\d{2})", str_time[1])):
                    Fm_month = True
                    if str_time[1] == "00":
                        Fm_month = False
                if bool(re.match(r"(\d{2})", str_time[2])):
                    Fm_day = True
                    if str_time[2] == "00":
                        Fm_day = False

        if Fm_year and Fm_month and Fm_day:
            pass_num += 1
        else:
            fail_num += 1
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
