# -*- coding:utf-8 -*-
import xlrd, openpyxl


class OrganizeData:

    def __init__(self, reportFormFile, analysisFile, year_num=2, basicFile1=None, basicFile2=None, basicFile3=None):
        """
        :param reportFormFile: 合并报表 Excel
        :param analysisFile:   分析报表 Excel
        :param basicFile1: 基础数据文件1 Excel（2019）
        :param basicFile2: 基础数据文件2 Excel（2017）
        :param basicFile3: 基础数据文件3 Excel（2015）
        :param year_num: 获取'基础数据文件1'中哪年的数据（ 1：表示仅获取当年的数据、2：表示获取两年的数据 ）
                        （eg: 若'basicFile1'与'basicFile2'是相邻的年份，则year_num=1，否则year_num=2）
        """
        self.reportFormFile = reportFormFile
        self.analysisFile = analysisFile
        self.year_num = year_num
        self.basicFile1 = basicFile1
        self.basicFile2 = basicFile2
        self.basicFile3 = basicFile3
        self.reportForm_list = []   # 合并报表字段列表
        self.basic1_dict = {}       # 基础数据字典1 {字段名:[当期数据,上期数据]} or {字段名:[当期数据]}
        self.basic2_dict = {}       # 基础数据字典2 {字段名:[当期数据,上期数据]}
        self.basic3_dict = {}       # 基础数据字典3 {字段名:[当期数据,上期数据]}
        self.reportForm_dict = {}   # 合并报表字典  {字段名:[数据1,数据2,数据3，数据4,数据5]}

    def show(self):
        # for i in self.reportForm_list: print(i)
        # for key, value in self.basic1_dict.items(): print(key + " : " + str(value) + "\n")
        # for key, value in self.basic2_dict.items(): print(key + " : " + str(value) + "\n")
        # for key, value in self.basic3_dict.items(): print(key + " : " + str(value) + "\n")
        for key, value in self.reportForm_dict.items(): print(key + " : " + str(value) + "\n")

    def run(self):
        """
           [ 运 行 ]
           第一步：将所有'基础数据文件'整合入'合并报表'中
           第二步：将'合并报表'中的数据导入'分析报表'的不同工作表中
        """
        self.organize_data()
        self.import_analysisFile()

    """ 
        #####################################################################################
        ####################################  第  一  步  ####################################
        #####################################################################################
    """

    def organize_data(self):
        """
            [ 将所有'基础数据文件'整合入'合并报告'中 ]
            1.获取'合并报表'中需要的字段列表 -> reportForm_list
            2.获取'基础数据文件1|2|3'中的数据内容'基础数据字典1|2|3' -> basic1_dict1|2|3
                < 注意：这 里 将 所 有 的 负 数 转 换 成 正 数 >
            3.将'基础数据字典1|2|3'整合入'合并报表字典' -> reportForm_dict
            4.将'合并报表字典'导入'合并报表'
        """
        # 1.获取'合并报表'中需要的字段列表 -> reportForm_list
        self.get_reportForm_list()

        # 2.获取'基础数据文件1|2|3'中的数据内容'基础数据字典1|2|3' -> basic1_dict1|2|3
        self.basic1_dict = self.get_basic_data(self.basicFile1, col=self.year_num)
        self.basic2_dict = self.get_basic_data(self.basicFile2, col=2)
        basic3_dict_col_num = self.year_num == 2 and 1 or 2
        self.basic3_dict = self.get_basic_data(self.basicFile3, col=basic3_dict_col_num)

        # 3.将'基础数据字典1|2|3'整合入'合并报表字典' -> reportForm_dict
        self.capture_reportForm_data()

        # 4.将'合并报表字典'导入'合并报表'
        self.import_reportFormFile()

    def get_reportForm_list(self):
        """
            获取'合并报表'中需要的字段列表 -> reportForm_list
        """
        # 获取'合并报表'中所有的字段
        rff_sheet = xlrd.open_workbook(self.reportFormFile).sheet_by_index(0)
        self.reportForm_list = [rff_sheet.row_values(row_num)[0].strip() for row_num in range(rff_sheet.nrows)]
        # self.reportForm_list = []
        # for row_num in range(rff_sheet.nrows):
        #     self.reportForm_list.append(rff_sheet.row_values(row_num)[0].strip())

        # 删除不需要的字段
        no_need_field_list = ["", "", "企业名称", "报表类型", "合并资产负债表", "流动资产", "应收票据及应收账款", "非流动资产",
                              "流动负债", "非流动负债","所有者权益（或股东权益）", "合并利润表", "合并现金流量表",
                              "一、经营活动产生的现金流量", "二、投资活动产生的现金流量", "三、筹资活动产生的现金流量"]
        for field in no_need_field_list:
            self.reportForm_list.remove(field)

    def get_basic_data(self, filename, col=2):
        """
            :param col: 获取几列数据，默认是两列（当期数据、前期数据）

            获取'基础数据字典'
            1.获取前2列or3列内容 {字段名:[当期数据]} or {字段名:[当期数据,上期数据]}
            2.将特殊的科目保留正负值，其余全部转成正数（针对'利润表、现金流量表'中相应的科目需要保留负数）
            3.将缺少的'合并报表字段'补充完整

            注：abs() 将 负数 转成 正数
        """
        cash_flow_field_list = ["经营活动产生的现金流量净额", "投资活动产生的现金流量净额", "筹资活动产生的现金流量净额",
                                "销售商品、提供劳务收到的现金", "购建固定资产、无形资产和其他长期资产支付的现金", "财务费用",
                                "分配股利、利润或偿付利息支付的现金", "现金及现金等价物净增加额", "期末现金及现金等价物余额"]

        data_dict = {}
        if filename:
            # 1.获取前2列or3列内容
            sheet = xlrd.open_workbook(filename).sheet_by_index(0)
            for row_num in range(sheet.nrows):
                field = sheet.row_values(row_num)[0].strip()
                amount1 = sheet.row_values(row_num)[1]
                amount2 = sheet.row_values(row_num)[2]
                # 目的：出错时的提示
                if isinstance(amount1, str) or isinstance(amount2, str):
                    print("字段 '" + field + "' 对应金额的类型是字符串 -> " + str(amount1) + " 、 " + str(amount2))

                # 2.将特殊的科目保留正负值（针对'利润表、现金流量表'中相应的科目）
                if field in cash_flow_field_list:
                    data_dict[field] = col == 2 and [amount1, amount2] or [amount1]
                else:
                    data_dict[field] = col == 2 and [abs(amount1), abs(amount2)] or [abs(amount1)]

            # 3.将缺少的'合并报告字段'补充完整
            for field in self.reportForm_list:
                if field not in data_dict.keys():
                    data_dict[field] = col == 2 and [0.0, 0.0] or [0.0]
        return data_dict

    def capture_reportForm_data(self):
        """
            将'基础数据字典1|2|3'整合入'合并报表字典' -> reportForm_dict
            < 利润表中的特殊处理 >
            （1）原因："归属于母公司所有者的净利润"、"归属于母公司股东的净利润" 这是同一个科目，但是每个公司报表的叫法不同
            （2）解决：将这两个科目赋予相同的值
            （3）举例：归母所有者 -> [1.1, 1.2, 1.3, 1.4, 0.0]
                      归母股东  -> [0.0, 0.0, 0.0, 0.0, 1.5]
                        合并   -> [1.1, 1.2, 1.3, 1.4, 1.5]
        """
        for field in self.reportForm_list:
            self.reportForm_dict[field] = []
            self.reportForm_dict[field] += self.basic1_dict[field]
            if self.basicFile2:
                self.reportForm_dict[field] += self.basic2_dict[field]
                if self.basicFile3:
                    self.reportForm_dict[field] += self.basic3_dict[field]

        # 利润表中的特殊处理
        # cc = [x + y for x, y in zip(aa, bb)]
        list1 = list(self.reportForm_dict["归属于母公司所有者的净利润"])
        list2 = list(self.reportForm_dict["归属于母公司股东的净利润"])
        list3 = [x + y for x, y in zip(list1, list2)]
        self.reportForm_dict["归属于母公司所有者的净利润"] = list3
        self.reportForm_dict["归属于母公司股东的净利润"] = list3

    def import_reportFormFile(self):
        """
            将'合并报表字典'导入'合并报告'
            1.遍历[合并报表]的行，判断A列中的字段名是否存在于[合并报表字典]的key中
            2.将匹配成功的字段值对应的'数值列表'赋值给后续的列字段（B列、C列、D列、E列、F列）

        """
        wb = openpyxl.load_workbook(self.reportFormFile)
        sheet = wb[wb.active.title]
        for row_i, row_data in enumerate(sheet.rows):
            # 获取A列字段值，非空情况下去掉首尾的空格
            A_field = sheet['A' + str(row_i+1)].value  # 查询单元格数据
            A_field = A_field and A_field.strip()
            # 判断A列中的字段名是否存在于[指定字典内容]的key中
            if A_field in list(self.reportForm_dict.keys()):
                # 遍历数值列表，依次修改后续的列字段（B列、C列、D列、E列、F列）
                for col_i, col_value in enumerate(self.reportForm_dict[A_field]):
                    sheet.cell(row=row_i + 1, column=col_i + 2, value=col_value)  # 修改单元格数据
        wb.save(self.reportFormFile)  # 将修改完的数据保存入Excel

    """ 
        #####################################################################################
        ####################################  第  二  步  ####################################
        #####################################################################################
    """

    def import_analysisFile(self):
        """
            [ 将'合并报表'中的数据导入'分析报表'的不同工作表中 ]
            1.导入'资产负债表分析1'工作表
            2.导入'资产负债表分析2'工作表
            3.导入'财务造假分析'工作表
            4.导入'利润表分析'工作表
            5.导入'现金流量表分析'工作表
        """
        self.import_balance_sheet_1()
        self.import_balance_sheet_2()
        self.import_balance_sheet_3()
        self.import_profit_sheet()
        self.import_cashflow_sheet()

    def save_sheet(self, sheet_name, import_field_dict):
        """
            导入工作表（公共模块）
            :param sheet_name:  工作表名称
            :param import_field_dict: 需要导入的字段字典
            :return:
        """
        # 从'合并报表字典'中找到相应的数据，根据对应的行数，依次填入相应的列中
        wb = openpyxl.load_workbook(self.analysisFile)
        sheet = wb.get_sheet_by_name(sheet_name)
        # 遍历需要的字段和行数
        for field, row_num in import_field_dict.items():
            # 找到对应的数据列表 依次填入相应的列中
            for col_i, col_value in enumerate(self.reportForm_dict[field]):
                sheet.cell(row=row_num, column=col_i + 3, value=col_value)  # 修改单元格数据
        wb.save(self.analysisFile)  # 将修改完的数据保存入Excel

    def import_balance_sheet_1(self):
        """ 导入'资产负债表分析1'工作表 """

        # 整理需要导入的字段 {字段名:行数}
        field_dict = {"货币资金": 5, "交易性金融资产": 6, "应收票据": 9, "应收账款": 10, "应收款项融资": 11, "预付款项": 12,
                      "存货": 13, "合同资产": 14, "长期应收款": 15, "固定资产": 16, "在建工程": 17, "使用权资产": 18,
                      "无形资产": 19, "开发支出": 20, "长期待摊费用": 21, "递延所得税资产": 22, "资产总计": 25}
        self.save_sheet(sheet_name='14.资产负债表分析1', import_field_dict=field_dict)

    def import_balance_sheet_2(self):
        """ 导入'资产负债表分析2'工作表 """

        # 整理需要导入的字段 {字段名:行数}
        field_dict = {"资产总计": 5, "负债合计": 11, "货币资金": 18, "交易性金融资产": 19, "短期借款": 23, "长期借款": 24,
                      "一年内到期的非流动负债": 25, "应付债券": 26, "长期应付款": 27, "应收账款": 34, "合同资产": 35,
                      "固定资产": 42, "在建工程": 43, "工程物资": 44, "以公允价值计量且其变动计入当期损益的金融资产": 52,
                      "可供出售金融资产": 53, "其他非流动金融资产": 54, "其他权益工具投资": 55, "其他债权投资": 56, "债权投资": 57,
                      "持有至到期投资": 58, "长期股权投资": 59, "投资性房地产": 60, "商誉": 68, "应付票据": 75, "应付账款": 76,
                      "预收款项": 77, "合同负债": 78, "应收票据": 80, "应收款项融资": 81, "预付款项": 84, "存货": 98, }
        self.save_sheet(sheet_name='15.资产负债表分析2', import_field_dict=field_dict)

    def import_balance_sheet_3(self):
        """ 导入'财务造假分析'工作表 """

        # 整理需要导入的字段 {字段名:行数}
        field_dict = {"货币资金": 5, "净利润": 9, "应收账款": 16, "资产总计": 17, "预付款项": 23, "其他应收款": 24, "在建工程": 32}
        self.save_sheet(sheet_name='16.财务造假分析', import_field_dict=field_dict)

    def import_profit_sheet(self):
        """ 导入'利润表分析'工作表 """

        # 整理需要导入的字段 {字段名:行数}
        field_dict = {"营业收入": 5, "营业成本": 12, "销售费用": 20, "管理费用": 21, "研发费用": 22, "财务费用": 23,
                      "税金及附加": 46, "营业利润": 47, "营业外收入": 55, "营业外支出": 56, "利润总额": 58,
                      "归属于母公司股东的净利润": 64}
        self.save_sheet(sheet_name='17.利润表分析', import_field_dict=field_dict)

    def import_cashflow_sheet(self):
        """ 导入'现金流量表分析'工作表 """

        # 整理需要导入的字段 {字段名:行数}
        field_dict = {"销售商品、提供劳务收到的现金": 5, "营业收入": 6, "净利润": 13, "经营活动产生的现金流量净额": 19,
                      "购建固定资产、无形资产和其他长期资产支付的现金": 25, "分配股利、利润或偿付利息支付的现金": 32,
                      "投资活动产生的现金流量净额": 40, "筹资活动产生的现金流量净额": 41,
                      "现金及现金等价物净增加额": 47, "期末现金及现金等价物余额": 54}
        self.save_sheet(sheet_name='18.现金流量表分析', import_field_dict=field_dict)


if __name__ == '__main__':
    """
        【 年 报 数 据 抓 取 步 骤 】
        1.抓取目录/Users/micllo/Downloads/年报数据抓取/ 中需要准备的Excel文件
         （1）'合并报表'、'分析报表' （ 拷贝/Users/micllo/Documents/微淼文档/Excel模板 ）
         （2）'原始数据'3份（ 需要手动获取 ）
        2.使用PDF转换器将年报中的三大合并报表转换成Excel
         （1）每份年报的三大合并报告分别进行转换，然后合并在一个Excel中（eg:原始数据_2019）
         （2）近五年报表需要转三次，生成3份Excel原始数据
        3.调整Excel原始数据格式
         （1）去除不需要的部分，保留主要的三列
         （2）对比原件，调整错行的地方
         （3）通过*1的方式，将文本转换成数值（保留2位小数，使用千分位分隔符）
        4.执行脚本
         （1）将3份原始数据导入'合并报表'中
         （2）将'合并报表'中的内容填入'分析报表'相应的工作表中
        5.分析报表
         
         < 注意：执行脚本中可能会出现的问题 >
         问题：若发现有些数据没有生成，是因为[合并报表]中需要的字段名 与 [原始数据]中的字段名称不一致 导致的
         解决：手动修改[原始数据]中的字段名后，再次执行脚本
    """
    """
        若'basicFile1'与'basicFile2'是相邻的年份，则year_num=1，否则year_num=2
        举例一：
            year_num=2
            basicFile1 = "原始数据_2019.xls"
            basicFile2 = "原始数据_2017.xls"
            basicFile3 = "原始数据_2015.xls"
        举例二：
            year_num=1
            basicFile1 = "原始数据_2020.xls"
            basicFile2 = "原始数据_2019.xls"
            basicFile3 = "原始数据_2017.xls"
        举例三：
            year_num=2
            basicFile1 = "原始数据_2021.xls"
            basicFile2 = "原始数据_2019.xls"
            basicFile3 = "原始数据_2017.xls"
    """

    pathDir = "/Users/micllo/Downloads/年报数据抓取/"
    reportFormFile = pathDir + "合并报表.xlsx"
    analysisFile = pathDir + "分析报表.xlsx"
    basicFile1 = pathDir + "原始数据_2019.xls"
    basicFile2 = pathDir + "原始数据_2017.xls"
    basicFile3 = pathDir + "原始数据_2015.xls"
    od = OrganizeData(reportFormFile=reportFormFile, analysisFile=analysisFile, year_num=2,
                      basicFile1=basicFile1, basicFile2=basicFile2, basicFile3=basicFile3)
    od.run()
    od.show()

