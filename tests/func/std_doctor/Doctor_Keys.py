import pymongo
import pandas as pd
import  jieba.analyse
import pandas as pd
import re

class Doctor_Info():
    @staticmethod
    def Get_Keys(Doctor_Name='李军'):
        # setup connection
        Mongo_client = pymongo.MongoClient(
            "mongodb://root:Mongodb789@dds-2ze92ad086cc41a4-pub.mongodb.rds.aliyuncs.com:3717/")
        # Access dbbase
        db_mongo = Mongo_client["medo_mango"]
        # Get table
        std_doctor = db_mongo['std_doctor']
        # set query object
        doc_name = Doctor_Name
        myquery = {"name": doc_name}
        List_doctor = std_doctor.find(myquery, {"DID": 1,
                                                "_id": 0,
                                                "affiliation": 1,
                                                "profession": 1,
                                                "expertise": 1,
                                                "description": 1,
                                                "faculty": 1,
                                                "physician_type": 1,
                                                "physician_scope": 1,
                                                "std_faculty": 1
                                                })
        Mongo_client.close()
        Dic_doctor = List_doctor
        Pd_doctor = pd.DataFrame(List_doctor)
        same_doctor = {}
        temp = {}
        discription = Pd_doctor["profession"] + Pd_doctor["expertise"] + \
                      Pd_doctor["description"] + Pd_doctor["faculty"] + Pd_doctor["physician_type"] + \
                      Pd_doctor["physician_scope"] + Pd_doctor["std_faculty"]
        for i in range(len(discription)):
            try:
                clean_words = re.sub(r'[^\w\s]', '', discription[i])
                clean_words = clean_words.replace(' ', '')
                temp[i] = list(jieba.cut(clean_words, cut_all=False))
            except:
                temp[i] = " "
                pass
        data = {'DID': Pd_doctor['DID'],
                'affiliation': Pd_doctor['affiliation'],
                'description': temp,
                }
        same_doctor = pd.DataFrame(data)
        return(same_doctor)

if __name__ == '__main__':
    list=Doctor_Info.Get_Keys()
    #print(list[DID])



