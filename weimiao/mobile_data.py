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
            3.将"原始数据字典"导入"报表分析Excel"
        :return:
        """
        self.get_basic_dict()
        self.data_process()
        self.import_analysisFile()

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

    def import_analysisFile(self):
        """
            [ 将"原始数据字典"导入"报表分析Excel" ]
            1.导入'8个关键指标'工作表
            2.导入'18步分析指标'工作表
            3.导入'财务造假分析'工作表
            4.导入'其他分析指标'工作表
        """
        self.import_8_key_index()
        self.import_18_analysis_index()
        self.import_financial_fraud_analysis()
        self.import_other_analysis_index()

    def save_sheet(self, sheet_name, import_field_dict):
        """
            导入工作表（公共模块）
            :param sheet_name:  工作表名称
            :param import_field_dict: 需要导入的字段字典
            :return:
        """
        # 从"原始数据"字典中找到相应的数据，根据对应的行数，依次填入相应的列中
        wb = openpyxl.load_workbook(self.analysisFile)
        sheet = wb.get_sheet_by_name(sheet_name)
        # 遍历需要的字段和行数
        for field, row_num in import_field_dict.items():
            # 判断"报表分析"中需要填入的字段名，是否存在于"原始数据"中
            if field in list(self.basic_dict.keys()):
                # 找到对应的数据列表 依次填入相应的列中
                for col_i, col_value in enumerate(self.basic_dict[field]):
                    sheet.cell(row=row_num, column=col_i + 3, value=col_value)  # 修改单元格数据
        wb.save(self.analysisFile)  # 将修改完的数据保存入Excel

    def import_8_key_index(self):
        """ 导入'8个关键指标'工作表 """

        # 需要导入的字段 {字段名:行数}
        field_dict = {"归属于母公司所有者的净利润": 7, "归属于母公司所有者权益合计": 8, "经营活动产生的现金流量净额": 15,
                      "净利润": 16, "负债合计": 23, "资产合计": 24, "营业收入": 31, "营业成本": 32, "营业利润": 41,
                      "固定资产": 56, "在建工程": 57, "工程物资": 58}
        self.save_sheet(sheet_name='8个关键指标', import_field_dict=field_dict)

    def import_18_analysis_index(self):
        """ 导入'18步分析指标'工作表 """

        # 需要导入的字段 {字段名:行数}
        field_dict = {"资产合计": 6, "负债合计": 13, "货币资金": 21, "交易性金融资产": 22, "短期借款": 26, "长期借款": 27,
                      "一年内到期的非流动负债": 28, "应付债券": 29, "长期应付款": 30, "应付票据": 38, "应付账款": 39, "预收款项": 40,
                      "合同负债": 41, "应收票据": 43, "应收款项融资": 44, "应收账款": 45, "合同资产": 46, "预付账款": 47,
                      "固定资产": 64, "在建工程": 65, "工程物资": 66, "以公允价值计量且其变动计入当期损益的金融资产": 75,
                      "可供出售金融资产": 76, "其他非流动金融资产": 77, "其他权益工具投资": 78, "其他债权投资": 79, "债权投资": 80,
                      "持有至到期投资": 81, "长期股权投资": 82, "投资性房地产": 83, "商誉": 92, "存货": 100, "营业收入": 109,
                      "营业成本": 117, "销售费用": 126, "管理费用": 127, "研发费用": 128, "财务费用": 129, "营业税金及附加": 150,
                      "营业利润": 151, "经营活动产生的现金流量净额": 160, "净利润": 161, "归属于母公司所有者的净利润": 168,
                      "归属于母公司所有者权益合计": 176, "购建固定资产、无形资产和其他长期资产支付的现金": 183,
                      "分配股利、利润或偿付利息支付的现金": 191}
        self.save_sheet(sheet_name='18步分析指标', import_field_dict=field_dict)

    def import_financial_fraud_analysis(self):
        """ 导入'财务造假分析'工作表 """

        # 需要导入的字段 {字段名:行数}
        field_dict = {"货币资金": 5, "净利润": 9, "应收账款": 16, "资产合计": 17, "预付款项": 23, "其他应收款": 24, "在建工程": 32}
        self.save_sheet(sheet_name='财务造假分析', import_field_dict=field_dict)


    def import_other_analysis_index(self):
        """ 导入'其他分析指标'工作表 """

        # 需要导入的字段 {字段名:行数}
        field_dict = {"货币资金": 5, "交易性金融资产": 6, "应收票据": 9, "应收账款": 10, "应收款项融资": 11, "预付款项": 12,
                      "存货": 13, "合同资产": 14, "长期应收款": 15, "固定资产": 16, "在建工程": 17, "使用权资产": 18,
                      "无形资产": 19, "开发支出": 20, "长期待摊费用": 21, "递延所得税资产": 22, "资产合计": 25,
                      "营业外收入": 51, "营业外支出": 52, "利润总额": 54, "销售商品、提供劳务收到的现金": 63, "营业收入": 64,
                      "经营活动产生的现金流量净额": 71, "投资活动产生的现金流量净额": 79, "筹资活动产生的现金流量净额": 80,
                      "现金及现金等价物净增加额": 86, "期末现金及现金等价物余额": 93}
        self.save_sheet(sheet_name='其他分析指标', import_field_dict=field_dict)


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

