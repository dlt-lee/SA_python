# -*- coding: utf-8 -*-
import re
import pymysql
import xlsxwriter
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
workbook = xlsxwriter.Workbook('Time_basicheck_guide.xlsx')
worksheet = workbook.add_worksheet()
n = 1
file = open("Name_check_guide.txt", "w")
#Scenario:
#Check whether ttime and time format in manual_association
##########################################################################################
#Given:
#Open manual_association
# set cursor to execute sql
mysql_cursor = pymysql.cursors.Cursor(mysql_con)
# check medmeeting_index
mysql_cursor.execute("select * from manual_guide")
############################################################################################
while True:
    #When:
    #Get data form database
    row = mysql_cursor.fetchone()
    try:
        Fm_year = False
        Fm_month = False
        Fm_day = False
        if len(row[7]) == 4:
            Fm_year = True
            Fm_month = True
            Fm_day = True
            if row[7] == "0000":
                Fm_year = False
        else:
            str_time = row[7].split("-")
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
    except:
        fail_num += 1
        try:
            worksheet.write(n, 0, row[0])
            worksheet.write(n, 1, row[1])
            worksheet.write(n, 2, row[12])
            n += 1
        except:
            pass
#Then: Pass_number +1 if all of the check points are TRue
    if Fm_year and Fm_month and Fm_day:
        pass_num += 1
    else:
        fail_num += 1
        try:
            worksheet.write(n, 0, row[0])
            worksheet.write(n, 1, row[1])
            worksheet.write(n, 2, row[12])
            n += 1
        except:
            print(row)



    if not row:
            break

print("Fail:%s" % fail_num)
print("Pass:%s" % pass_num)
file.write("Fail:%s\n" % fail_num)
file.write("Pass:%s\n" % pass_num)
file.close()
workbook.close()
mysql_cursor.close()
mysql_con.close()
