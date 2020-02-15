# coding:UTF-8
import re
import time
# 引入tools模块的Tools类
from tools import *
import future

# 定义编码格式
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class Search:

    def __init__(self, price, start_date, end_date):
        self.price = price
        self.start_date = start_date
        self.end_date = end_date
        self.basic_url = "http://srh.bankofchina.com/search/whpj/search.jsp?erectDate=" + start_date + "&nothing=" + end_date + "&pjname=" + price
        self.task_num = 0
        self.executor = ThreadPoolExecutor(min(1, 1))
        self.result_list = []
        self.pyset = Tools.mongo_connect("127.0.0.1", 27017)

    def set_executor(self, task_num, max_workers):
        """
            设置线程池的最大线程数不超过'max_workers'
        """
        self.task_num = task_num
        self.executor = ThreadPoolExecutor(min(self.task_num, max_workers))

    def get_data_for_page(self, kind, request_url):
        """
        [ 获取页面table中的内容 ]
        :param kind:
        :return:
        """
        print("%s is running " % currentThread().getName())
        table = Tools.get_page_content("get", request_url).find_all('table', attrs={'align': 'left'})  # 定位table元素
        page = []
        for trs in table:
            if kind == 'th':
                # for e in trs.find_all(kind):
                #     page.append(e.get_text())
                page = [item.get_text() for item in trs.find_all(kind)]
            else:
                line = []
                for i, e in enumerate(trs.find_all(kind)):
                    line.append(e.get_text())  # 将获取的字段保存入line[]中
                    if ":" in e.get_text():
                        page.append(line)  # 将获取的line[]保存入page[]中
                        line = []  # 清空数据
        return page

    def show_table_head(self, table_head):
        """
        [ 显示 head ]
        :param table_head:
        :return:
        """
        for i, item in enumerate(table_head):
            print(table_head[i]),
        print("\n")

    def show_page_info(self, page_info):
        """
        [ 显示每页数据信息 ]
        :param page_info:
        :return:
        """
        for row_i, row in enumerate(page_info):
            for col_i, col in enumerate(page_info[row_i]):
                print(page_info[row_i][col_i]),
            print("\n")

    def show_search_info(self, search_info):
        """
        [ 显示搜索数据信息 ]
        search_info = []  # 三维list [ 整体搜索数据, [ 每一页 ] , [ [ 每一行 ], [ ] ] ]
        """
        for page_i, page in enumerate(search_info):
            for row_i, row in enumerate(search_info[page_i]):
                for col_i, col in enumerate(search_info[page_i][row_i]):
                    print(search_info[page_i][row_i][col_i]),
                print("\n")
            print("\n========================== 第" + str(page_i + 1) + "页 ==========================\n\n")

    # def show_search_info_with_future(self):
    #     """
    #     [ 显示搜索数据（future） ]
    #     self.result_list = []  二维list # [ [ 每一页 ], <Future at 0x1084ce190 state=finished returned list> ]
    #     < Future .. list >     二维list # [ [ 每一行 ], [ list ] ]
    #     """
    #     for page_i, page in enumerate(self.result_list):
    #         for row_i, row in enumerate(self.result_list[page_i].result()):
    #             for col_i, col in enumerate(self.result_list[page_i].result()[row_i]):
    #                 print(self.result_list[page_i].result()[row_i][col_i]),
    #             print("\n")
    #         print("\n========================== 第" + str(page_i + 1) + "页 ==========================\n\n")

    def show_search_info_with_future(self):
        """
        [ 显示搜索数据（future） ]
        self.result_list = [] # 三维list [ 整体搜索数据, [ 每一页 ] , [ [ 每一行 ], [ ] ] ]
        """
        for page_i, page in enumerate(self.result_list):
            for row_i, row in enumerate(self.result_list[page_i]):
                for col_i, col in enumerate(self.result_list[page_i][row_i]):
                    print(self.result_list[page_i][row_i][col_i]),
                print("\n")
            print("\n========================== 第" + str(page_i + 1) + "页 ==========================\n\n")

    def get_page_num_for_search(self):
        """
        [ 获取搜索的页面数量 ]
        :return:
        """
        # 获取页面内容 <class 'bs4.BeautifulSoup'>
        page_info = Tools.get_page_content("get", self.basic_url)
        # print(type(page_info))
        # 获取所有脚本内容  <class 'bs4.element.ResultSet'>
        script_info_all = page_info.find_all('script', attrs={'language': 'JavaScript'})
        # print(type(script_info_all))
        # 获取需要的脚本内容
        script_info = script_info_all[3]
        # 将脚需要的本内容分割成list
        script_list = str(script_info).split("\n")
        # print(type(script_list))
        for line in script_list:
            re1 = re.match(r'(.*)var m_nRecordCount = (.*);', str(line))
            re2 = re.match(r'(.*)var m_nPageSize = (.*);', str(line))
            if re1:
                record_num = re1.group(2)
            if re2:
                page_size = re2.group(2)
        # 计算获取页面数量
        page_num = float(record_num) / float(page_size)
        # print(page_num)
        # 若有小数则向上取整(即：小数若大于0则整数+1)
        if int(str(page_num).split(".")[1]) > 0:
            return int(str(page_num).split(".")[0]) + 1
        else:
            return int(str(page_num).split(".")[0])

    def get_data_for_search(self):
        """
        [ 获取搜索后所有页面的数据内容 ]
        search_info = []  # 三维list [ 整体搜索数据, [ 每一页 ] , [ [ 每一行 ], [ ] ] ]
        :return:
        """
        search_info = []
        # 获取搜索的页面数量
        page_num = self.get_page_num_for_search()
        print "\n共搜索：" + str(page_num) + "页\n"
        # 根据页面数量，循环获取每页中的数据
        for num in range(1, page_num + 1):
            request_url = self.basic_url + "&page=" + str(num)
            page_info = self.get_data_for_page("td", request_url)
            # show_page_info(page_info)
            search_info.append(page_info)

        self.show_search_info(search_info)
        return search_info

    def get_data_for_search_with_future(self):
        """
        [ 获取搜索后所有页面的数据内容 ]
        self.result_list = []  三维list [ 整体搜索数据, [ 每一页 ] , [ [ 每一行 ], [ "", "" ] ] ]
        """
        # 获取搜索的页面数量
        page_num = self.get_page_num_for_search()
        print "\n共搜索：" + str(page_num) + "页\n"

        # 根据页面数量循环获取每页中的数据(每次最多20个线程)，保存入result_list属性
        self.set_executor(page_num, 20)
        for i in range(1, page_num + 1):
            request_url = self.basic_url + "&page=" + str(i)
            # 执行'add_done_callback'回调函数：将先执行完的线程的结果保存入'result_list'属性中
            self.executor.submit(self.get_data_for_page, "td", request_url).add_done_callback(self.save_future_result)



            # future = self.executor.submit(self.get_data_for_page, "td", request_url)
            # self.result_list.append(future)
        # 等待所有线程执行完毕
        self.executor.shutdown()

        # 将搜索到的内容按照正确的时间顺序排列：按每页第一个'发布时间'进行降序排列
        # ( 根据第二维list<每页>的 第1个list<每行>中的第7个字段进行排序 )
        self.result_list.sort(key=lambda x: x[0][6], reverse=True)
        # 显示搜索内容
        self.show_search_info_with_future()

    def save_future_result(self, future):
        result = future.result()
        self.result_list.append(result)

    def change2doc(self, row_list):
        """
        [ 将list转换成mongo文档 ]
        :param row_list:
        :return:
        """
        doc = {}
        for i, item in enumerate(row_list):
            if i == 0:
                doc.update({"货币名称": row_list[i]})
            elif i == 1:
                doc.update({"现汇买入价": row_list[i]})
            elif i == 2:
                doc.update({"现钞买入价": row_list[i]})
            elif i == 3:
                doc.update({"现汇卖出价": row_list[i]})
            elif i == 4:
                doc.update({"现钞卖出价": row_list[i]})
            elif i == 5:
                doc.update({"中行折算价": row_list[i]})
            elif i == 6:
                doc.update({"发布时间": row_list[i]})
            else:
                print("超出行列表范围")
        return doc

    def get_dict_list(self):
        """
        [ 将搜索内容转换成字典列表 ]
        dict_list = [{"货币名称":""},{"现汇买入价":""},{"现钞买入价":""},{"现汇卖出价":""},{"现钞卖出价":""},{"中行折算价":""},{"发布时间":""}]
        """
        dict_list = []
        for page_i, page in enumerate(self.result_list):
            for row_i, row in enumerate(self.result_list[page_i]):
                dict_list.append(self.change2doc(self.result_list[page_i][row_i]))
        return dict_list

    # 显示字典列表中的内容
    def show_dict_list(self, dict_list):
        for i, item in enumerate(dict_list):
            print("货币名称：" + dict_list[i]["货币名称"])
            print("现汇买入价：" + dict_list[i]["现汇买入价"])
            print("现钞买入价：" + dict_list[i]["现钞买入价"])
            print("现汇卖出价：" + dict_list[i]["现汇卖出价"])
            print("现钞卖出价：" + dict_list[i]["现钞卖出价"])
            print("中行折算价：" + dict_list[i]["中行折算价"])
            print("发布时间：" + dict_list[i]["发布时间"])
            print("==================")

    # 显示mongo库中的文档记录
    def show_doc_mongo(self):
        for i in self.pyset.find():
            print("货币名称：" + i.get(u"货币名称", "default"))
            print("现汇买入价：" + i.get(u"现汇买入价", "default"))
            print("现钞买入价：" + i.get(u"现钞买入价", "default"))
            print("现汇卖出价：" + i.get(u"现汇卖出价", "default"))
            print("现钞卖出价：" + i.get(u"现钞卖出价", "default"))
            print("中行折算价：" + i.get(u"中行折算价", "default"))
            print("发布时间：" + i.get(u"发布时间", "default"))
            print("不存在的key：" + i.get(u"aaaaa", "default"))
            print("===================")

    def get_data_save_mongo(self):
        """
        [ 获取某牌价某时间范围内的所有数据,并存入mongo ]
        """
        # 获取某牌价某时间范围内的所有数据
        # self.get_data_for_search()
        self.get_data_for_search_with_future()

        # # 将搜索内容转换成字典列表
        dict_list = self.get_dict_list()
        # self.show_dict_list(dict_list)

        # 将字典列表插入mongo
        self.pyset.remove()
        self.pyset.insert(dict_list)
        self.show_doc_mongo()


if __name__ == '__main__':

    start = time.time()
    print "开始时间：" + str(start)

    # # 获取某牌价某时间范围内的所有数据,并存入mongo
    search = Search("1314", "2018-10-01", "2018-10-23")

    # 显示 标题tab
    table_head = search.get_data_for_page("th", search.basic_url)
    search.show_table_head(table_head)

    # 获取某牌价某时间范围内的所有数据,并存入mongo
    search.get_data_save_mongo()

    end = time.time()
    print "结束时间：" + str(end)
    print "总共用时：" + str(end - start)



