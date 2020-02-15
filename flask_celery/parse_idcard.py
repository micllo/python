# coding:UTF-8
import sys
sys.path.append('../')
from pymongo import MongoClient
import datetime
import re
import json

class AnalyzeIDCard:

    def __init__(self, id_card):
        self.id_card = id_card
        self.mongo = MongoClient("192.168.1.127", 27017)
        self.suvdata_db = self.mongo.suvdata               # 连接'suvdata'数据库
        self.province_zip = self.suvdata_db.province_zip   # 使用'province_zip'集合
        self.region_zip = self.suvdata_db.region_zip       # 使用'region_zip'集合
        self.result = {}

    def analyze_id_card(self):
        """
          [ 身份证解析 ]
          1.验证身份证
          （1）验证：身份证位数是否是18位或15位 （若为15位则转换成18位）
          （2）验证：第1~6位归属地代码是否合法（从mongo库中进行匹配）
          （3）验证：第7~14位出生年月是否合法
          （4）验证：第18位校验码是否合法
          2.解析身份证
          （1）省、市、县(从mongo中获取)
          （2）出生年月
          （3）性别
          （4）星座
        """
        if not self.check_size():return '身份证位数有误'
        if not self.check_region():return '归属地不合法'
        if not self.check_birthday():return '出生年月不合法'
        if not self.check_code():return '校验码不合法'
        self.analyze_region_code()
        self.analyze_birthday()
        self.analyze_sex()
        self.analyze_constellation()
        return json.dumps(self.result, encoding="UTF-8", ensure_ascii=False)

    def check_size(self):
        """
          [ 验证位数 ]
          1.15位身份证按19xx年考虑，先转为18位，校验位暂为‘M’，这样方便后面的判断和计算
          2.15位身份证要求全为数字，18位身份证前17位为数字，第18位为数字或字母“X”
        """
        if len(self.id_card) != 15 and len(self.id_card) != 18:
            return False

        if len(self.id_card) == 15:
            self.id_card = self.id_card[:6] + '19' + self.id_card[6:] + 'M'

        if not (self.id_card[:17].isdigit() and (self.id_card[-1].isdigit() or self.id_card[-1] == 'M' or self.id_card[-1].upper() == 'X')):
            return False

        return True

    def check_region(self):
        """
          [ 验证 归属地是否合法 ]
          1.验证：第3位必须是0，第4位不能是0
          2.验证：第5位和第6位不能同时为0
          3.验证：除"上海市、北京市、重庆市、天津市"以外，
                （1）第5，6位不能是01
                （2）第6位不能是0
          4.验证：该代码是否存在于'region_zip'表中
        """
        if self.id_card[:6][2] != "0" or self.id_card[:6][3] == "0":return False
        if self.id_card[:6][4] == "0" and self.id_card[:6][5] == "0":return False
        if self.id_card[:6][:3] not in ["310", "110", "500", "120"]:
            if self.id_card[:6][4:] == "01":return False
            if self.id_card[:6][5:] == "0":return False
        return any(self.id_card[:6] == i.get("region_code") for i in self.region_zip.find())

    def check_birthday(self):
        """
          [ 验证 出生日期的合法性 ]
          1.闰年出生日期的合法性正则表达式
          2.平年出生日期的合法性正则表达式
        """
        if (int(self.id_card[6:10]) % 4 == 0 or (int(self.id_card[6:10]) % 100 == 0 and int(self.id_card[6:10]) % 4 == 0)):
            ereg = re.compile('[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9XxM]$')
        else:
            ereg = re.compile('[1-9][0-9]{5}(19[0-9]{2}|20[0-9]{2})((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9XxM]$')
        return re.match(ereg, self.id_card)

    def check_code(self):
        """
          [ 验证 校验码 ]
          注：15位身份证不需要检查校验码
        """
        w = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        s = 0
        for i in range(17):
            s = s + int(self.id_card[i]) * w[i]
        last_code = (1 - s) % 11
        if last_code == 10: last_code = 'X'
        last_code = str(last_code)
        if self.id_card[-1] != last_code and self.id_card[-1] != 'M':
            return False
        else:
            return True

    def analyze_region_code(self):
        """
          [ 解析 归属地 ]
          1.省/市：根据前3位，在'province_zip'表中查询
          2.城市：根据前4位+00，在'region_zip'表中查询
          3.区/县：根据前6位，在'region_zip'表中查询
        """
        self.result["province"] = self.province_zip.find_one({"prov_code": self.id_card[:3]})["prov_name"]
        self.result["city"] = self.region_zip.find_one({"region_code": self.id_card[:4] + "00"})["region_name"]
        self.result["region"] = self.region_zip.find_one({"region_code": self.id_card[:6]})["region_name"]

    def analyze_birthday(self):
        """
          [ 解析 出生年月 ]
        """
        self.result["birthday"] = str(datetime.date(int(self.id_card[6:10]), int(self.id_card[10:12]), int(self.id_card[12:14])))

    def analyze_sex(self):
        """
          [ 解析 性别 ]
        """
        if int(self.id_card[-2]) % 2 == 0:
            self.result["sex"] = '女'
        else:
            self.result["sex"] = '男'

    def analyze_constellation(self):
        """
          [ 解析 星座 ]
        """
        month = int(self.id_card[10:12])
        day = int(self.id_card[12:14])
        if (month == 1 and day >= 20) or (month == 2 and day <= 18):
            self.result["constellation"] = '水瓶座'
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            self.result["constellation"] = '双鱼座'
        elif (month == 3 and day >= 20) or (month == 4 and day <= 19):
            self.result["constellation"] = '白羊座'
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            self.result["constellation"] = '金牛座'
        elif (month == 5 and day >= 21) or (month == 6 and day <= 21):
            self.result["constellation"] = '双子座'
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            self.result["constellation"] = '巨蟹座'
        elif (month == 7 and day >= 22) or (month == 8 and day <= 22):
            self.result["constellation"] = '狮子座'
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            self.result["constellation"] = '处女座'
        elif (month == 9 and day >= 23) or (month == 10 and day <= 23):
            self.result["constellation"] = '天秤座'
        elif (month == 10 and day >= 23) or (month == 11 and day <= 22):
            self.result["constellation"] = '天蝎座'
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            self.result["constellation"] = '射手座'
        elif (month == 12 and day >= 21) or (month == 1 and day <= 19):
            self.result["constellation"] = '摩羯座'

    def show_analyze_result(self):
        """
          [ 显示解析结果 ]
        """
        for key, value in self.result.items():
            print key, ':', value
