import re
from pyparsing import *
import pandas as pd
import sys
sys.path.append(r'../std_doctor/')
from Doctor_Keys import Doctor_Info
List_keys = ["缺血", "血小板"]
in_string = '不同类型缺血性卒中患者的抗血小板治疗'
print(re.search("缺血", '不同类型缺血性卒中患者的抗血小板治疗'))
List_match = any(key in in_string for key in List_keys)
print(re.search( "血小板", in_string))
List_doctor_infor = Doctor_Info.Get_Keys()
List_doctor_infor.to_excel("List_doctor_infor.xlsx")
#for index, row in List_doctor_infor.iterrows():

