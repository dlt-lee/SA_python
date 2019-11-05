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
workbook = xlsxwriter.Workbook('Char_basicheck_event.xlsx')
worksheet = workbook.add_worksheet()
n = 1
# Case rsult storage
file = open("Char_basicheck_event.txt", "w")
#Scenario:
#Check whether the Name/Origin_Title/Event_Name/Event_Tier/Origin_Title of manual_association are null/english/chinese
##########################################################################################
#Given:
#Open manual_event
# set cursor to execute sql
mysql_cursor = pymysql.cursors.Cursor(mysql_con)
# check manual_event
mysql_cursor.execute("select * from manual_event")
#get list name
list_name = mysql_cursor.description
list_tri = ["地市级", "国际级", "国家级", "省市级"]
############################################################################################
while True:
    #When:
    #Get data form database
    row = mysql_cursor.fetchone()
    contain_Origin_Title = False
    contain_name = False
    length_name = False
    contain_Event_Name = False
    contain_Event_Tier = False
    contain_Event_Sponsor = False
    try:
        en_reg = re.compile(r'[A-Za-z]+')
        cn_reg = re.compile(u"[\u4e00-\u9fa5]+")
        # check Origin_Title
        if bool(re.search(en_reg, row[4])):
            contain_Origin_Title = True
        elif bool(re.search(cn_reg, row[4])):
            contain_Origin_Title = True
        # check Name
        if bool(re.search(en_reg, row[5])):
            contain_name = True
            length_name = True
        elif bool(re.search(cn_reg, row[5])):
            contain_name = True
            if bool(len(row[5]) > 1) and bool(len(row[5]) < 4):
                length_name = True
        # check Event_Name
        if bool(re.search(en_reg, row[7])):
            contain_Event_Name = True
        elif bool(re.search(cn_reg, row[7])):
            contain_Event_Name = True
        #check Event_Tier
        if row[8] in list_tri:
            contain_Event_Tier = True
        # check Event_Sponsor
        if bool(re.search(en_reg, row[10])):
            contain_Event_Sponsor = True
        elif bool(re.search(cn_reg, row[10])):
            contain_Event_Sponsor = True

    except:
        print(row)


    #Thne: Number of pass +1 if all check points are True

    if contain_Origin_Title and contain_name and length_name and contain_Event_Name and contain_Event_Sponsor:
        pass_num += 1
    else:
        fail_num += 1
        #Add fail case related information into log file
        try:
            worksheet.write(n, 0, row[4])
            worksheet.write(n, 1, contain_Origin_Title)
            worksheet.write(n, 2, row[5])
            worksheet.write(n, 3, contain_name)
            worksheet.write(n, 4, length_name)
            worksheet.write(n, 5, row[7])
            worksheet.write(n, 6, contain_Event_Name)
            worksheet.write(n, 7, row[8])
            worksheet.write(n, 8, contain_Event_Tier)
            worksheet.write(n, 9, row[10])
            worksheet.write(n, 10, contain_Event_Sponsor)
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
