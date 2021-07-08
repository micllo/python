# -*- coding:utf-8 -*-
import re, xlrd, xlwt, openpyxl


class MobeleData:

    def __init__(self, basicFile, analysisFile):
        """
        :param basicFile:     原始数据 Excel
        :param analysisFile:  报表分析 Excel

        """
        self.basicFile = basicFile
        self.analysisFile = analysisFile
        self.basic_dict = {}          # "原始数据"字典 ->  { 字段名 : [2019,2018,2017,2016,2015,2014] }
        self.field_dict = {}          # "新旧字段"字段 -> { "老字段名"："新字段名" }
        self.target_info_dict = {}    # "指标信息"字典 -> { 工作表名 : { 指标名 : 行号 } }
        self.target_data_dict = {}    # "指标数据"字典 -> { 工作表名 : { 指标名 : [2020,2019,2018,2017,2016,2015] } }
        self.target_result_dict = {}  # "指标结果"字典 -> { 工作表名 : { 指标名 : [2020,2019,2018,2017,2016,2015] } }

    def show(self):
        for field, data_list in self.basic_dict.items(): print(field + " : " + str(data_list) + "\n")
        # for field, data_list in self.basic_dict.items(): print(field + "\n")

        print("\n\n")  # 显示"指标数据"字典
        for sheet_name, target_info in self.target_data_dict.items():
            print(sheet_name + "\n")
            for target_name, target_data in target_info.items():
                print(target_name + " : " + str(target_data) + "\n")

        print("\n\n")  # 显示"指标结果"字典
        for sheet_name, target_info in self.target_result_dict.items():
            print(sheet_name + "\n")
            for target_name, target_result in target_info.items():
                print(target_name + " : " + str(target_result) + "\n")

    def run_import(self):
        """
        [ 导 入 数 据 ]
        1.获取"原始数据Excel"到字典中： basic_dict ->  { 字段名 : [2020,2019,2018,2017,2016,2015] }
        2.将"原始数据字典"中的字段整理成"报表分析"中需要的字段
        3.将"原始数据字典"导入"报表分析Excel"
        """
        self.get_basic_dict()
        self.data_process()
        self.import_analysisFile()

    def run_analysis_result(self):
        """
        [ 导 入 分 析 结 果 ]
        1.提供'指标信息字典': target_info_dict
            { 工作表名 : { 指标名 : 行号 } } -> { 8个关键指标 : { 净资产收益率 : 9 } }
        2.获取"报表分析Excel"中的'指标数据字典'：target_data_dict
            { 工作表名 : { 指标名 : [2020_data,2019_data,2018_data,2017_data,2016_data,2015_data] } }
        3.验证并得到'指标结果字典'：target_result_dict
            { 工作表名 : { 指标名 : [2020_result,2019_result,2018_result,2017_result,2016_result,2015_result] } }
        4.将指标结果保存入"报表分析Excel"
        """
        self.get_target_info_dict()
        self.get_target_data_dict()
        self.get_target_result_dict()
        self.import_result()

    def get_basic_dict(self):
        """
            获取"原始数据Excel"到字典中： basic_dict ->  { 字段名 : [2019,2018,2017,2016,2015,2014] }
            备注：将 '补充资料：(元)' 及之后的内容删除掉
        """
        # bbhz_sheet = xlrd.open_workbook(self.basicFile).sheet_by_index(0)
        with xlrd.open_workbook(self.basicFile) as excel:
            bbhz_sheet = excel.sheet_by_index(0)
            for row_num in range(bbhz_sheet.nrows):
                field = bbhz_sheet.row_values(row_num)[0].strip()
                if "补充资料" in field:
                    break
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
            将"原始数据字典"导入"报表分析Excel"
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
                      "固定资产合计": 56, "在建工程合计": 57, "工程物资": 58}
        self.save_sheet(sheet_name='8个关键指标', import_field_dict=field_dict)

    def import_18_analysis_index(self):
        """ 导入'18步分析指标'工作表 """

        # 需要导入的字段 {字段名:行数}
        field_dict = {"资产合计": 6, "负债合计": 13, "货币资金": 21, "交易性金融资产": 22, "短期借款": 26, "长期借款": 27,
                      "一年内到期的非流动负债": 28, "应付债券": 29, "长期应付款合计": 30, "应付票据": 38, "应付账款": 39, "预收款项": 40,
                      "合同负债": 41, "应收票据": 43, "应收款项融资": 44, "应收账款": 45, "合同资产": 46, "预付款项": 47,
                      "固定资产合计": 64, "在建工程合计": 65, "工程物资": 66, "以公允价值计量且其变动计入当期损益的金融资产": 75,
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
        field_dict = {"货币资金": 5, "净利润": 9, "应收账款": 16, "资产合计": 17, "预付款项": 23, "其他应收款合计": 24, "在建工程合计": 32}
        self.save_sheet(sheet_name='财务造假分析', import_field_dict=field_dict)

    def import_other_analysis_index(self):
        """ 导入'其他分析指标'工作表 """

        # 需要导入的字段 {字段名:行数}
        field_dict = {"货币资金": 5, "交易性金融资产": 6, "应收票据": 9, "应收账款": 10, "应收款项融资": 11, "预付款项": 12,
                      "存货": 13, "合同资产": 14, "长期应收款": 15, "固定资产合计": 16, "在建工程合计": 17, "使用权资产": 18,
                      "无形资产": 19, "开发支出": 20, "长期待摊费用": 21, "递延所得税资产": 22, "资产合计": 25,
                      "营业外收入": 51, "营业外支出": 52, "利润总额": 54, "销售商品、提供劳务收到的现金": 63, "营业收入": 64,
                      "经营活动产生的现金流量净额": 71, "投资活动产生的现金流量净额": 79, "筹资活动产生的现金流量净额": 80,
                      "现金及现金等价物净增加额": 86, "期末现金及现金等价物余额": 93}
        self.save_sheet(sheet_name='其他分析指标', import_field_dict=field_dict)

    def get_target_info_dict(self):
        """
            提供'指标信息字典': target_info_dict
                { 工作表名 : { 指标名 : 行号 } } -> { 8个关键指标 : { 净资产收益率 : 9 } }
            :return:
        """
        sheet_1 = {}
        sheet_1["净资产收益率"] = 9
        sheet_1["净利润现金比率"] = 17
        sheet_1["资产负债率"] = 25
        sheet_1["毛利率"] = 33
        sheet_1["营业利润率"] = 42
        sheet_1["营业收入增长率"] = 50
        sheet_1["固定资产合计占总资产的比率"] = 61
        sheet_1["分红率"] = 69   # 暂不处理
        self.target_info_dict["8个关键指标"] = sheet_1

        sheet_2 = {}
        sheet_2["总资产增长率"] = 7
        sheet_2["资产负债率"] = 15
        sheet_2["准货币资金-有息负债"] = 32
        sheet_2["应付预收-应收预付差额"] = 49
        sheet_2["（应收账款+合同资产）占资产总计的比率"] = 58
        sheet_2["固定资产合计占总资产的比率"] = 69
        sheet_2["投资类资产占资产总计的比率"] = 86
        sheet_2["商誉占资产总计的比率"] = 94
        sheet_2["存货占资产总计的比率"] = 102
        sheet_2["营业收入增长率"] = 110
        sheet_2["毛利率波动幅度"] = 119   # 暂不处理
        sheet_2["期间费用率/毛利率"] = 133
        sheet_2["销售费用率"] = 141
        sheet_2["主营利润/营业利润"] = 154   # 暂不处理
        sheet_2["净利润现金比率"] = 162
        sheet_2["归母净利润增长率"] = 169
        sheet_2["净资产收益率"] = 177
        sheet_2["购建资产/经营现金流"] = 185
        sheet_2["分配股利/经营现金流"] = 193
        self.target_info_dict["18步分析指标"] = sheet_2

        sheet_3 = {}
        sheet_3["利息支出/净利润"] = 11  # 暂不处理
        sheet_3["应收账款/资产总计"] = 18
        sheet_3["（预付款项+其他应收款）/总资产"] = 27
        sheet_3["在建工程/总资产"] = 34   # 暂不处理
        self.target_info_dict["财务造假分析"] = sheet_3

        sheet_4 = {}
        sheet_4["与企业经营无关的资产/总资产"] = 27
        sheet_4["准货币资金/资产总计"] = 38
        sheet_4["预付款项/资产总计"] = 45
        sheet_4["营业外收入净额/利润总额"] = 55
        sheet_4["销售商品/营业收入"] = 65
        sheet_4["经营现金流增长率"] = 72
        # sheet_4["公司类型"] = 81  # 暂不处理
        sheet_4["现金+分红"] = 88
        sheet_4["期末现金及现金等价物余额"] = 93
        self.target_info_dict["其他分析指标"] = sheet_4

    def get_target_data_dict(self):
        """
            获取"报表分析Excel"中的'指标数据字典'：target_data_dict
                { 工作表名 : { 指标名 : [2020_data,2019_data,2018_data,2017_data,2016_data,2015_data] } }
            :return:
        """
        for sheet_name, target_info in self.target_info_dict.items():
            with xlrd.open_workbook(self.analysisFile) as excel:
                sheet = excel.sheet_by_name(sheet_name)
                data_dict = {}
                for target_name, target_row in target_info.items():
                    # 将str数据转成float,并保留4位小数
                    data_2020 = round(float(sheet.row_values(target_row - 1)[2]), 4)
                    data_2019 = round(float(sheet.row_values(target_row - 1)[3]), 4)
                    data_2018 = round(float(sheet.row_values(target_row - 1)[4]), 4)
                    data_2017 = round(float(sheet.row_values(target_row - 1)[5]), 4)
                    data_2016 = round(float(sheet.row_values(target_row - 1)[6]), 4)
                    data_dict[target_name] = [data_2020, data_2019, data_2018, data_2017, data_2016]
                self.target_data_dict[sheet_name] = data_dict

    def get_target_result_dict(self):
        """
            验证并得到'指标结果字典'：target_result_dict
             { 工作表名 : { 指标名 : [2020_result,2019_result,2018_result,2017_result,2016_result,2015_result] } }
        """
        for sheet_name, sheet_target_data in self.target_data_dict.items():
            self.target_result_dict[sheet_name] = self.get_target_result(sheet_target_data)

    def get_target_result(self, sheet_target_data):
        """
            参数：sheet_target_data   -> { 指标名 : [2020_data,2019_data,2018_data,2017_data,2016_data,2015_data] }
            返回：sheet_target_result -> { 指标名 : [2020_result,2019_result,2018_result,2017_result,2016_result,2015_result] }
        """
        sheet_target_result = {}
        for target_name, data_list in sheet_target_data.items():
            result_list = []
            for index, data in enumerate(data_list):
                # < 8个关键指标 >
                if target_name == "净资产收益率":
                    result_list.append(data >= 0.2 and "非常优秀" or (data >= 0.15 and "优秀" or (data >= 0.05 and "一般" or "质量较差")))
                if target_name == "净利润现金比率":  # < 需要手动判断 平均值 >
                    result_list.append(data >= 1 and "优秀" or (data >= 0.8 and "一般" or "质量较差"))
                if target_name == "资产负债率":
                    result_list.append(data < 0.4 and "无风险" or (data < 0.6 and "风险小" or "风险大"))
                if target_name == "毛利率":
                    result_list.append(data >= 0.6 and "非常优秀" or (data >= 0.4 and "优秀" or (data >= 0.15 and "一般" or "质量较差")))
                if target_name == "营业利润率":
                    result_list.append(data >= 0.2 and "优秀" or (data >= 0.12 and "一般" or "质量较差"))
                if target_name == "营业收入增长率":
                    result_list.append(data >= 0.1 and "优秀" or (data > 0 and "一般" or "质量较差"))
                if target_name == "固定资产合计占总资产的比率":
                    result_list.append(data < 0.4 and "风险小" or (data < 0.5 and "一般" or "风险大"))

                # < 18步分析指标 >（上述已有的判断，则不要重复添加）
                if target_name == "总资产增长率":
                    result_list.append(data > 0.1 and "优秀" or (data > 0 and "一般" or "质量较差"))
                if target_name in ["准货币资金-有息负债", "应付预收-应收预付差额"]:
                    result_list.append(data > 0 and "质量较好" or "质量较差")
                if target_name == "（应收账款+合同资产）占资产总计的比率":
                    result_list.append(data <= 0.01 and "非常优秀" or (data <= 0.03 and "优秀" or (data <= 0.2 and "一般" or "风险大")))
                if target_name == "投资类资产占资产总计的比率":
                    result_list.append(data <= 0.1 and "优秀" or (data < 0.2 and "一般" or "质量较差"))
                if target_name == "商誉占资产总计的比率":
                    result_list.append(data <= 0.1 and "无风险" or "风险大")
                if target_name == "存货占资产总计的比率":
                    if sheet_target_data["应付预收-应收预付差额"][index] > 0 and sheet_target_data["（应收账款+合同资产）占资产总计的比率"][index] < 0.01:
                        result_list.append("无风险")
                    elif sheet_target_data["（应收账款+合同资产）占资产总计的比率"][index] > 0.05 and data > 0.15:
                        result_list.append("风险大")
                    else:
                        result_list.append("一般")
                if target_name == "毛利率波动幅度":  # < 需要手动判断 >
                    result_list.append(abs(data) < 0.1 and "风险小" or (abs(data) < 0.2 and "一般" or "风险大"))
                if target_name == "期间费用率/毛利率":
                    result_list.append(data < 0.4 and "优秀" or (data < 0.5 and "一般" or "质量较差"))
                if target_name == "销售费用率":
                    result_list.append(data <= 0.15 and "风险小" or (data <= 0.3 and "一般" or "质量较差"))
                if target_name == "主营利润/营业利润":  # < 需要手动判断 >
                    result_list.append(data >= 0.8 and "质量较好" or (data >= 0.7 and "一般" or "质量较差"))
                if target_name == "归母净利润增长率":
                    result_list.append(data >= 0.1 and "优秀" or (data > 0 and "一般" or "质量较差"))
                if target_name == "购建资产/经营现金流":
                    result_list.append(data > 0.6 and "风险大" or (data > 0.03 and "风险小" or "一般"))
                if target_name == "分配股利/经营现金流":
                    result_list.append(data >= 0.2 and "优秀" or "一般")

                # < 财务造假分析 >
                if target_name == "应收账款/资产总计":
                    result_list.append(data < 0.15 and "风险小" or "风险大")
                if target_name == "（预付款项+其他应收款）/总资产":
                    result_list.append(data < 0.10 and "风险小" or "风险大")

                # < 其他分析指标 >
                if target_name == "与企业经营无关的资产/总资产":  # < 需要手动判断 >
                    result_list.append(data <= 0.10 and "优秀" or (data <= 0.25 and "一般" or "质量较差"))
                if target_name == "准货币资金/资产总计":
                    result_list.append(data >= 0.5 and "非常优秀" or (data >= 0.25 and "优秀" or (data > 0.20 and "一般" or "质量较差")))
                if target_name == "预付款项/资产总计":
                    result_list.append(data <= 0.01 and "风险小" or (data <= 0.03 and "一般" or "风险大"))
                if target_name == "营业外收入净额/利润总额":
                    result_list.append(abs(data) < 0.05 and "质量较好" or "质量较差")
                if target_name == "销售商品/营业收入":
                    result_list.append(data >= 1 and "优秀" or (data >= 0.75 and "一般" or "质量较差"))
                if target_name == "经营现金流增长率":
                    result_list.append(data > 0.1 and "优秀" or (data > 0 and "一般" or "质量较差"))
                if target_name in ["现金+分红", "期末现金及现金等价物余额"]:
                    result_list.append(data > 0 and "质量较好" or "质量较差")
            sheet_target_result[target_name] = result_list
        return sheet_target_result

    def import_result(self):
        """
          将指标结果保存入"报表分析Excel"
           target_result_dict -> { 工作表名 : { 指标名 : [2020_result,2019_result,2018_result,2017_result,2016_result,2015_result] } }
           target_info_dict -> { 工作表名 : { 指标名 : 行号 } }
        """
        for sheet_name, result_data in self.target_result_dict.items():
            wb = openpyxl.load_workbook(self.analysisFile)
            sheet = wb.get_sheet_by_name(sheet_name)
            for target_name, result_list in result_data.items():
                # 获取需要更新的行号
                row_num = self.target_info_dict[sheet_name][target_name] + 1
                # 修改单元格数据
                for col_i, result in enumerate(result_list):
                    sheet.cell(row=row_num, column=col_i + 3, value=result)
            wb.save(self.analysisFile)  # 将修改完的数据保存入Excel


if __name__ == '__main__':

    pathDir = "/Users/micllo/Downloads/A年报数据抓取/"
    basicFile = pathDir + "原始数据.xlsx"
    analysisFile = pathDir + "报表分析.xlsx"
    md = MobeleData(basicFile=basicFile, analysisFile=analysisFile)

    """
     [ 执 行 步 骤 ]
     1.运行导入数据
     2.打开excel,手动保存
     3.运行导入分析结果
     4.手动判断剩余指标
    """
    md.run_import()
    # md.run_analysis_result()

    md.show()

    """
    【 手 动 判 断 剩 余 指 标 】

     < 8个关键指标 >
       1.净利润现金比率
       2.分红率

     < 18步分析指标 >
       1.准货币资金-有息负债
       2.应付预收-应收预付差额
       3.投资类资产占资产总计的比率
       4.毛利率波动幅度（毛利率）
       5.主营利润/营业利润（主营利润率）

     < 财务造假分析 >
       1.利息支出/净利润
       2.在建工程/总资产

     < 其他分析指标 >
       1.与企业经营无关的资产/总资产
       2.经营现金流增长率
       3.公司类型
       4.现金+分红
    """


