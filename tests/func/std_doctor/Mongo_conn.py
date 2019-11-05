import pymongo
import pandas as pd
import  jieba
import  numpy as np
import csv
#setup connection
Mongo_client = pymongo.MongoClient("mongodb://root:Mongodb789@dds-2ze92ad086cc41a4-pub.mongodb.rds.aliyuncs.com:3717/")
#Access dbbase
db_mongo = Mongo_client["medo_mango"]
#Get table
std_doctor = db_mongo['std_doctor']
#set query object
doc_name = "李军"
myquery = {"name": doc_name}
List_doctor = std_doctor.find(myquery, {"DID": 1,
                                        "_id": 0,
                                        "affiliation": 1,
                                        "profession": 1,
                                        "expertise": 1,
                                        "std faculty": 1,
                                        "description": 1,
                                        "faculty": 1,
                                        "physician_type": 1,
                                        "physician_scope": 1,
                                        "std_faculty": 1,
                                        "hospital": 1})
List_doctor = pd.DataFrame(List_doctor)
print(List_doctor)
Mongo_client.close()
