#-*- coding: UTF-8 -*-
import os
import time
import datetime
from pymongo import MongoClient
import re

def run_case(path):
    if os.path.isdir(path):
        for name in os.listdir(path):
            abs_path = os.path.join(path,name)
            print(abs_path)
            if abs_path.endswith('.py'):
                os.system('python %s' % abs_path)

def write_mongo(path):
    # connect to mongodb
    client = MongoClient("mongodb://root:Mongodb789@dds-2ze92ad086cc41a4-pub.mongodb.rds.aliyuncs.com:3717/")
    mydb = client['medo_mango']
    mycol = mydb["checklist"]
    # add time tag
    ticks = time.mktime(datetime.datetime.now().timetuple())
    #print("*************Reaing and Writing all the results to mongodb*****************")
    result = []
    if os.path.isdir(path):#if it is a path
        for name in os.listdir(path):#遍历所有Name
            abs_path = os.path.join(path, name)
            if abs_path.endswith('.txt'):
                result.clear()
                with open(abs_path, 'r') as file_to_read:#open each txt and read
                    while True:
                        lines = file_to_read.readline()  # 整行读取数据
                        result.append(lines)
                        if not lines:
                            break
                            pass
                # split the case name from txt
                casename=abs_path.split('.txt')
                casename=casename[0].split('./')
                # split the number of fail and pass from txt
                try:
                    failnum = result[0].split(':')
                    failnum=re.sub('[\n]', '', failnum[1])
                    #print(failnum)
                    passnum = result[1].split(':')
                    passnum = re.sub('[\n]', '', passnum[1])

                except:
                    passnum = 'null'
                    failnum='null'
                # write json data
                jsontext = {'case_name': casename[1],
                'result': {'fail': failnum ,'pass':passnum},
                'check_time': int(ticks)}

                try:
                    mycol.insert_one(jsontext)
                    print("add check results successfully")
                except Exception as e:
                    print("add fail")

run_case(r'.\func\manual_data')
run_case(r'.\func\medmeeting')
write_mongo(r'./')