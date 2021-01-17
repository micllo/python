# -*- coding:utf-8 -*-
import re, xlrd, openpyxl


class MobeleData:

    def __init__(self, basicFile, analysisFile):
        """
        :param basicFile:     原始数据 Excel
        :param analysisFile:  报表分析 Excel

        """
        self.basicFile = basicFile
        self.analysisFile = analysisFile
        self.basic_dict = {}  # "原始数据"字典 ->  { 字段名 : [2019,2018,2017,2016,2015,2014] }
        self.field_dict = {}  # "新旧字段"字段 -> { "老字段名"："新字段名" }

    def show(self):
        for field, data_list in self.basic_dict.items(): print(field + " : " + str(data_list) + "\n")
        # for field in self.field_list: print(field)

    def run(self):
        """
            [ 运 行 ]
            1.获取"原始数据Excel"到字典中： basic_dict ->  { 字段名 : [2019,2018,2017,2016,2015,2014] }
            2.将"原始数据字典"中的字段整理成"报表分析"中需要的字段
             （1）数据填补完整（填补0.0）
             （2）字段名称处理
             （3）删除不需要的字段
        :return:
        """
        self.get_basic_dict()
        self.data_process()

    def get_basic_dict(self):
        """
            获取"原始数据Excel"到字典中： basic_dict ->  { 字段名 : [2019,2018,2017,2016,2015,2014] }
        """
        bbhz_sheet = xlrd.open_workbook(self.basicFile).sheet_by_index(0)
        for row_num in range(bbhz_sheet.nrows):
            field = bbhz_sheet.row_values(row_num)[0].strip()
            data_2019 = bbhz_sheet.row_values(row_num)[1]
            data_2018 = bbhz_sheet.row_values(row_num)[2]
            data_2017 = bbhz_sheet.row_values(row_num)[3]
            data_2016 = bbhz_sheet.row_values(row_num)[4]
            data_2015 = bbhz_sheet.row_values(row_num)[5]
            data_2014 = bbhz_sheet.row_values(row_num)[6]
            self.basic_dict[field] = [data_2019, data_2018, data_2017, data_2016, data_2015, data_2014]

    def data_process(self):
        """
           将"原始数据字典"中的字段整理成"报表分析"中需要的字段
           1.删除不需要的字段
           2.填补金额数据（将 "" 或 "--" 转换成 0.0）
           3.字段名处理

            < 字段名处理规则 >
            1.去掉 "：" 及之前的内容
            （1）通过"："分割成列表
            （2）通过分割列表判断不同的处理情况
                  若len=1，直接使用原有内容  （说明没有需要删除的内容）
                  若len>1，获取第二个元素内容（第一个元素是不需要的内容）
            2.仅去掉 "、" 及之前包含"一，二，三，四，五，六，七"的内容
            （1）通过"、"分割成列表
            （2）通过分割列表判断不同的处理情况
                  若len=1，直接使用原有内容  （说明没有需要删除的内容）
                  若len>1 并且 第一个元素不含"一，二，三，四，五，六"中的内容，直接使用原有内容  （说明没有需要删除的内容）
                  若len>1 并且 第一个元素包含"一，二，三，四，五，六"中的内容，获取第二个元素内容（第一个元素是不需要的内容）
            3.去掉尾部的 "(元)"
        """

        # 1.删除不需要的字段
        del self.basic_dict["科目\时间"]
        del self.basic_dict[""]

        for field, data_list in self.basic_dict.items():
            # 2.填补金额数据（将 "" 或 "--" 转换成 0.0）
            for i, amount in enumerate(data_list):
                if isinstance(amount, str):
                    self.basic_dict[field][i] = 0.0
            # 3.字段名处理
            field_new = len(field.split("：")) > 1 and field.split("：")[1] or field
            field_new = len(field_new.split("、")) > 1 and field_new.split("、")[0] in ["一", "二", "三", "四", "五", "六"] \
                         and field_new.split("、")[1] or field_new
            field_new = re.sub(r'(\(元\))', "", field_new)
            self.field_dict[field] = field_new

        # 将"原始数据"字典中的"字段名"替换成"处理后的字段名"
        for field_old, field_new in self.field_dict.items():
            self.basic_dict[field_new] = self.basic_dict.pop(field_old)


if __name__ == '__main__':
    """
        【 年 报 数 据 整 理 步 骤 】
        1.将"原始数据"中的字段整理成"报表分析"中需要的字段
    """

    pathDir = "/Users/micllo/Downloads/年报数据抓取/"
    basicFile = pathDir + "原始数据.xlsx"
    analysisFile = pathDir + "报表分析.xlsx"
    md = MobeleData(basicFile=basicFile, analysisFile=analysisFile)
    md.run()
    md.show()

