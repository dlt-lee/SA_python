import re
import pymysql
import pymongo
import xlsxwriter
import sys
import sys
sys.path.append(r'../std_doctor/')
from Doctor_Keys import Doctor_Info

#Setup Mysql connection
mysql_con = pymysql.connect(host="rm-2zet5lw17as40fty28o.mysql.rds.aliyuncs.com",
                            user="snowball", password="MEDOsnow$%^&",
                            db="medo_master", charset='utf8')
# log preparation
workbook = xlsxwriter.Workbook('map_doctor_detail.xlsx')
worksheet = workbook.add_worksheet()
n =0
# set cursor to execute sql
mysql_cursor = mysql_con.cursor()
# check manual_event
mysql_cursor.execute("select * from medmeeting_detail where name = '李军'")
# Get doctor keys
Doctor_keys = Doctor_Info.Get_Keys("李军")
while True:
    # Get data form database
    row_mdm = mysql_cursor.fetchone()
    cn_reg = re.compile(u"[\u4e00-\u9fa5]+")
    try:
        # Set integral
        Doctor_integral = -1
        for index, row_doctor in Doctor_keys.iterrows():

            count = 0
            if bool(re.search(cn_reg, row_mdm[3])) and bool(re.search(str(row_doctor["affiliation"]), row_mdm[3])):
                # Set integral
                Doctor_integral = -1
                Doctor_ID = []
                Doctor_add = []
                Doctor_add.append(row_doctor["affiliation"])
                Doctor_ID.append(row_doctor["DID"])
                break

            else:
                if bool(re.search(cn_reg, row_mdm[1])):
                    for key in row_doctor["description"]:
                        if bool(re.search(key, row_mdm[1])):
                            count += 1
                if bool(re.search(cn_reg, row_mdm[5])):
                    for key in row_doctor["description"]:
                        if bool(re.search(key, row_mdm[5])):
                            count += 1
                if bool(re.search(cn_reg, row_mdm[10])):
                    for key in row_doctor["description"]:
                        if bool(re.search(key, row_mdm[10])):
                            count += 1

            if count > Doctor_integral:
                Doctor_ID = []
                Doctor_add = []
                Doctor_integral = count
                Doctor_add.append(row_doctor["affiliation"])
                Doctor_ID.append(row_doctor["DID"])
            elif count == Doctor_integral:
                Doctor_add.append(row_doctor["affiliation"])
                Doctor_ID.append(row_doctor["DID"])

        worksheet.write(n, 0, row_mdm[1])
        worksheet.write(n, 1, row_mdm[2])
        worksheet.write(n, 2, row_mdm[3])
        worksheet.write(n, 3, str(Doctor_add))
        worksheet.write(n, 4, row_mdm[5])
        worksheet.write(n, 5, row_mdm[10])
        worksheet.write(n, 6, Doctor_integral)
        worksheet.write(n, 7, str(Doctor_ID))
        n += 1


    except Exception as e:
        print(e)
        print(row_mdm)
    if not row_mdm:
        break

workbook.close()
mysql_cursor.close()
mysql_con.close()