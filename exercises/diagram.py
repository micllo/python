# coding:UTF-8
from search import Search
import re
import matplotlib.pyplot as plt
import numpy as np

# 定义编码格式
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Diagram(Search):

    def __init__(self, price, start_date, end_date):
        Search.__init__(self, price, start_date, end_date)
        # super(Diagram, self).__init__(price, start_date, end_date)
        self.data = []
        self.month_list = []
        self.average_data = []

    def get_data_from_mongo(self):
        """
         [ 从mongo中获取 "货币名称"、"中行折算价"、"发布时间"、"年份"、"月份"；保存入 data ]
        """
        result = self.pyset.find()
        print "总共有 " + str(result.count()) + " 条记录"
        for res in result:
            record = {}
            record["货币名称"] = res.get(u"货币名称", "default")
            record["中行折算价"] = res.get(u"中行折算价", "default")
            record["发布时间"] = res.get(u"发布时间", "default")
            re_result = re.match(r'(.*)\.(.*)\.(.*)', record["发布时间"])
            record["年份"] = re_result.group(1)
            record["月份"] = re.sub(r'^0', "", re_result.group(2))
            self.data.append(record)

    def get_month_from_data(self):
        """
          [ 获取月份的种类：去重、排序 ]
        """
        self.month_list = [int(i["月份"]) for i in self.data]
        self.month_list = list(set(self.month_list))
        self.month_list.sort()

    def get_average_price(self):
        """
          [ 获取 "货币名称"、"月份"、"中行折算价总数"、"中行折算价总和"、"中行折算价每月平均值"；保存入 average_data]
        """
        for i, item in enumerate(self.month_list):
            test_record = {}
            test_record["月份"] = item
            test_record["中行折算价当月总数"] = 0
            test_record["中行折算价当月总和"] = 0.00
            for res in self.data:
                if int(res["月份"]) == item:
                    test_record["货币名称"] = res["货币名称"]
                    test_record["中行折算价当月总数"] += 1
                    test_record["中行折算价当月总和"] += float(res["中行折算价"])
            # 保留两位小数
            test_record["中行折算价当月平均值"] = '%.2f' % (test_record["中行折算价当月总和"] / test_record["中行折算价当月总数"])
            self.average_data.append(test_record)

    def show_matplotlib(self):
        """
          [ 显示曲线图 ]
        """
        # 设置 figure 的长宽
        plt.figure(figsize=(12, 8))
        # 设置横坐标 type -> ndarray
        x = np.array(self.month_list)
        print x
        print type(x)
        # 设置纵坐标 type -> ndarray
        y = np.array([i["中行折算价当月平均值"] for i in self.average_data])
        print y
        print type(y)
        # 设置轴线的label
        plt.xlabel("month")
        plt.ylabel("2018 average price")
        # plt.plot(x, y)
        # 设置线条的：颜色、粗细、样式
        plt.plot(x, y, color='red', linewidth=1.0, linestyle='--')
        plt.show()


if __name__ == '__main__':

    """
        1.从mongo中获取数据（'英镑'、'发布时间'、'中行折算价'）
        2.计算出每月"中行折算价"的平均值
        3.实现"英镑"的'中行折算价每月平均值'曲线图
        4.实现"英镑、美元"的'中行折算价每月平均值'曲线图
    """

    diagram = Diagram("1314", "2018-10-01", "2018-10-23")

    # 显示 标题tab
    table_head = diagram.get_data_for_page("th", diagram.basic_url)
    diagram.show_table_head(table_head)

    # 从mongo中获取 "货币名称"、"中行折算价"、"发布时间"、"年份"、"月份"
    diagram.get_data_from_mongo()
    # for i in diagram.data:
    #     print "货币名称：" + i["货币名称"]
    #     print "中行折算价：" + str(i["中行折算价"])
    #     print "发布时间：" + str(i["发布时间"])
    #     print "年份：" + str(i["年份"])
    #     print "月份：" + str(i["月份"])
    #     print "========================="

    # # 获取月份的种类
    diagram.get_month_from_data()
    # print diagram.month_list
    #
    # # 获取 "货币名称"、"月份"、"中行折算价总数"、"中行折算价总和"、"中行折算价每月平均值"；保存入 average_data
    diagram.get_average_price()
    for i in diagram.average_data:
        print "货币名称：" + i["货币名称"]
        print "月份：" + str(i["月份"])
        print "中行折算价当月总数：" + str(i["中行折算价当月总数"])
        print "中行折算价当月总和：" + str(i["中行折算价当月总和"])
        print "中行折算价当月平均值：" + str(i["中行折算价当月平均值"])
        print "========================="

    # 显示曲线图
    diagram.show_matplotlib()




