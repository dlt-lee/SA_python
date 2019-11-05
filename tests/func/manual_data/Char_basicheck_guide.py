# -*- coding: utf-8 -*-
import re
import pymysql
import xlsxwriter

# Setup Mysql connection
mysql_con = pymysql.connect(host="rm-2zet5lw17as40fty28o.mysql.rds.aliyuncs.com",
                            user="snowball", password="MEDOsnow$%^&",
                            db="medo_master", charset='utf8')

# fail number
fail_num = 0
# pass number
pass_num = 0
# log preparation
workbook = xlsxwriter.Workbook('Char_basicheck_guide.xlsx')
worksheet = workbook.add_worksheet()
n = 1
# case result storage
file = open("Char_basicheck_guide.txt", "w")
#Scenario:
#Check whether the Name/Origin_Title/Guide_Type of manual_guide are null/english/chinese
##########################################################################################
#Given:
#Open manual_event
# set cursor to execute sql
mysql_cursor = pymysql.cursors.Cursor(mysql_con)
# check medmeeting_index
mysql_cursor.execute("select * from manual_guide")
#get list name
list_name = mysql_cursor.description
#get uide_Type list
list_type = ["共识","指南"]
############################################################################################
while True:
    #When:
    #Get data form database
    row = mysql_cursor.fetchone()
    contain_name = False
    length_name = False
    contain_Origin_Title = False
    contain_Guide_Type = False
    contain_Guide_Name = False
    try:
        en_reg = re.compile(r'[A-Za-z]+')
        cn_reg = re.compile(u"[\u4e00-\u9fa5]+")
        # check Name
        if bool(re.search(en_reg, row[1])):
            contain_name = True
            length_name = True
        elif bool(re.search(cn_reg, row[1])):
            contain_name = True
            if bool(len(row[1]) > 1) and bool(len(row[1]) <= 4):
                length_name = True
        # check Origin_Title
        if bool(re.search(en_reg, row[4])):
            contain_Origin_Title = True
        elif bool(re.search(cn_reg, row[4])):
            contain_Origin_Title = True
        #check Guide_Type
        if row[5] in list_type:
            contain_Guide_Type = True
        # check Guide_Name
        if bool(re.search(en_reg, row[6])):
            contain_Guide_Name = True
        elif bool(re.search(cn_reg, row[6])):
            contain_Guide_Name = True

    except:
        print(row)


    #Thne: Number of pass +1 if all check points are True

    if contain_Origin_Title and contain_name and length_name and contain_Guide_Name and contain_Guide_Type:
        pass_num += 1
    else:
        fail_num += 1
        #Add fail case related information into log file
        try:
            worksheet.write(n, 0, row[4])
            worksheet.write(n, 1, contain_Origin_Title)
            worksheet.write(n, 2, row[1])
            worksheet.write(n, 3, contain_name)
            worksheet.write(n, 4, length_name)
            worksheet.write(n, 5, row[5])
            worksheet.write(n, 6, contain_Guide_Type)
            worksheet.write(n, 7, row[6])
            worksheet.write(n, 8, contain_Guide_Name)
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
