# -*- coding:utf-8 -*-
import re, xlrd, openpyxl
from urllib import request
from bs4 import BeautifulSoup


class GainStockInfo:

    def __init__(self, xq_base_url, ths_base_url, file, gd_link=False):
        """
        :param xq_base_url: 雪球网地址
        :param ths_base_url: 同花顺网地址
        :param file:
        :param gd_link: 是否需要获取十大股东连接
        """
        self.xq_base_url = xq_base_url
        self.ths_base_url = ths_base_url
        self.xq_gd_url = self.xq_base_url + "snowman/S/"
        self.stock_info_url = self.xq_base_url + "S/"
        self.file = file
        self.gd_link = gd_link
        self.stock_row_num_dict = {}  # 从"价格指标-副本"中获取股票行号字典
        self.stock_info_dict = {}     # 通过雪球网获取对应股票的相关信息字典

    def run(self):
        """
           【 更新当前价格信息：股价、每股收益、TTM股息、总股本 】
           1.从"价格指标-副本"中获取股票行号字典
              { "三一重工_600031"：33 }
           2.通过雪球网获取对应股票的相关信息字典
              { "三一重工_600031"：{'行号': 33, '当前股价': '36.81', '每股收益': '1.70', '股息(TTM)': '0.42', '总股本': '84.84',
                                  '雪球连接': 'xxxx', '同花顺连接': 'xxxxx'}}
           3.更新数据

           [ 参 考 资 料 ] https://cuiqingcai.com/1319.html

           [ 备 注 ] 如果 gd_link = True 则表示需要获取十大股东连接
            < 雪球网 > 十大股东_SDGD、十大流通股东_LTGD
            603605 -> https://xueqiu.com/snowman/S/SH603605/detail#/SDGD
                      https://xueqiu.com/snowman/S/SH603605/detail#/LTGD
            002821 -> https://xueqiu.com/snowman/S/SZ002821/detail#/SDGD
                      https://xueqiu.com/snowman/S/SZ002821/detail#/LTGD

            < 同花顺 > 十大股东_tenholder、十大流通股东_flowholder
            http://stockpage.10jqka.com.cn/600031/holder/#tenholder
            http://stockpage.10jqka.com.cn/600031/holder/#flowholder
        """
        self.get_stock_row_num_dict()  # 从"价格指标-副本"中获取股票行号字典
        self.get_stock_info_dict()     # 通过雪球网获取对应股票的相关信息字典
        self.update_excel()            # 更新原有数据内容
        self.show()                    # 打印获取结果

    def show(self):
        print(self.stock_row_num_dict)
        print(len(self.stock_row_num_dict))
        for key, value in self.stock_info_dict.items(): print(key + str(value))

    # 从"价格指标-副本"中获取股票行号字典 -> { "三一重工_600031"：33}
    def get_stock_row_num_dict(self):
        sheet = xlrd.open_workbook(self.file).sheet_by_index(0)
        for row_num in range(sheet.nrows):
            A_value = sheet.row_values(row_num)[0].strip()
            if "_" in A_value:
                self.stock_row_num_dict[A_value] = row_num + 1

    # 通过雪球网获取对应股票的相关信息字典
    # { "三一重工_600031"：{'行号': 33, '当前股价': '36.81', '每股收益': '1.70', '股息(TTM)': '0.42', '总股本': '84.84',
    #                      '雪球连接': 'xxxx', '同花顺连接': 'xxxxx'} }
    def get_stock_info_dict(self):
        for stock_name, row_num in self.stock_row_num_dict.items():
            stock_code = stock_name.split("_")[1]
            self.stock_info_dict[stock_name] = self.get_stock_info(stock_code, row_num)

    # 通过雪球网获取相关信息(当前股价、每股收益、股息(TTM)、总股本)
    def get_stock_info(self, stock_code, row_num):
        # 判断股票代码开头字母来选择调用地址
        # 600031 -> https://xueqiu.com/S/SH600031
        # 002677 -> https://xueqiu.com/S/SZ002677
        url = stock_code[0] == "6" and self.stock_info_url + "SH" + stock_code or self.stock_info_url + "SZ" + stock_code

        stock_info = {}
        html = self.send_request(url, stock_code)
        soup = BeautifulSoup(html, 'lxml')
        # print(soup.prettify())  # 打印 html
        # 获取 当前股价
        stock_current = soup.select('div[class="stock-current"]')[0].get_text()
        stock_info["当前股价"] = stock_current[1:]
        # 获取 每股收益、股息(TTM)、总股本
        table_ele = soup.select('table[class="quote-info"]')[0]
        stock_profit_match = re.match(r'(.*)每股收益：<span>(.*)</span></td><td>股息\(TTM\)', str(table_ele))
        stock_interest_match = re.match(r'(.*)股息\(TTM\)：<span>(.*)</span></td><td>总股本', str(table_ele))
        stock_num_match = re.match(r'(.*)总股本：<span>(.*)</span></td><td>总市值', str(table_ele))
        stock_info["每股收益"] = stock_profit_match.group(2)
        stock_info["股息(TTM)"] = stock_interest_match.group(2)
        stock_info["总股本"] = stock_num_match.group(2)[:-1]
        stock_info["行号"] = row_num
        if self.gd_link:
            xq_base_url = stock_code[0] == "6" and self.xq_gd_url + "SH" + stock_code or self.xq_gd_url + "SZ" + stock_code
            xq_sdgd_url = xq_base_url + "/detail#/SDGD"
            xq_ltgd_url = xq_base_url + "/detail#/LTGD"
            ths_tenholder_url = self.ths_base_url + stock_code + "/holder/#tenholder"
            ths_flowholder_url = self.ths_base_url + stock_code + "/holder/#flowholder"
            stock_info["雪球连接"] = xq_sdgd_url
            stock_info["同花顺连接"] = ths_tenholder_url
        return stock_info

    def send_request(self, url, stock_code):
        try:
            # 发送请求获取html
            headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0'}
            req = request.Request(url, headers=headers, method='GET')
            html = request.urlopen(req, timeout=30)
        except:
            print(stock_code + " 该股票代码有误 ！")
        finally:
            return html

    # 更新原有数据内容
    def update_excel(self):
        wb = openpyxl.load_workbook(self.file)
        sheet = wb.get_sheet_by_name("A股")
        for stock_name, stock_info in self.stock_info_dict.items():
            # 修改单元格数据
            row_num = int(stock_info["行号"])
            sheet.cell(row=row_num, column=3, value=stock_info["当前股价"])
            sheet.cell(row=row_num, column=14, value=stock_info["每股收益"])
            sheet.cell(row=row_num, column=15, value=stock_info["股息(TTM)"])
            sheet.cell(row=row_num, column=16, value=stock_info["总股本"])
            if self.gd_link:
                sheet.cell(row=row_num, column=31, value=stock_info["雪球连接"])
                sheet.cell(row=row_num, column=32, value=stock_info["同花顺连接"])
        wb.save(self.file)  # 将修改完的数据保存入Excel


if __name__ == '__main__':
    file = "/Users/micllo/Downloads/A年报数据抓取/价格指标-副本.xlsx"
    xq_base_url = "https://xueqiu.com/"
    ths_base_url = "http://stockpage.10jqka.com.cn/"
    gsi = GainStockInfo(xq_base_url, ths_base_url, file, gd_link=True)
    gsi.run()


