import time
import re

class tools():

    @staticmethod
    def time_check(time):
        Fm_year = False
        Fm_month = False
        Fm_day = False
        if len(time) == 4:
            Fm_year = True
            Fm_month = True
            Fm_day = True
            if time == "0000":
                Fm_year = False
        else:
            str_time = time.split("-")
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
        return Fm_year, Fm_month, Fm_day

    @staticmethod
    def en_cn_check(self , row):
        contain_name = False
        en_reg = re.compile(r'[A-Za-z]+')
        cn_reg = re.compile(u"[\u4e00-\u9fa5]+")
        if bool(re.search(en_reg, row)):
            contain_name = True
        elif bool(re.search(cn_reg, row)):
            contain_name = True
        return contain_name

    @staticmethod
    def en_cn_length_check(self , row , length):
        en_reg = re.compile(r'[A-Za-z]+')
        cn_reg = re.compile(u"[\u4e00-\u9fa5]+")
        if bool(re.search(en_reg, row)):
            contain = True
        elif bool(re.search(cn_reg, row)):
            contain = True
            if len(row) < length:
                contain = False
        return contain

    @staticmethod
    def en_cn_length_check(self , row , length1,length2):
        en_reg = re.compile(r'[A-Za-z]+')
        cn_reg = re.compile(u"[\u4e00-\u9fa5]+")
        if bool(re.search(en_reg, row)):
            contain = True
        elif bool(re.search(cn_reg, row)):
            contain = True
            if (len(row) < length1) or (len(row) > length2):
                contain = False
        return contain