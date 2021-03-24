# -*- coding:utf-8 -*-
import re, xlrd, openpyxl
from urllib import request
from bs4 import BeautifulSoup


# 通过雪球网获取相关信息(当前股价、每股收益、股息(TTM)、总股本)
def get_stock_info(xueqiu_url, stock_code, row_num):
    # 判断股票代码开头字母来选择调用地址
    # 600031 -> https://xueqiu.com/S/SH600031
    # 002677 -> https://xueqiu.com/S/SZ002677
    if stock_code[0] == "6":
        url = xueqiu_url + "SH" + stock_code
    else:
        url = xueqiu_url + "SZ" + stock_code

    stock_info = {}
    try:
        # 发送请求获取html
        headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0'}
        req = request.Request(url, headers=headers, method='GET')
        html = request.urlopen(req, timeout=30)
    except:
        print(stock_code + " 该股票代码有误 ！")
    else:
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
    return stock_info


# 从"价格指标-副本"中获取股票行号字典 -> { "三一重工_600031"：33}
def get_stock_row_num_dict(file):
    stock_row_num_dict = {}
    sheet = xlrd.open_workbook(file).sheet_by_index(0)
    for row_num in range(sheet.nrows):
        A_value = sheet.row_values(row_num)[0].strip()
        if "_" in A_value:
            stock_row_num_dict[A_value] = row_num + 1
    return stock_row_num_dict


# 通过雪球网获取对应股票的相关信息字典
# { "三一重工_600031"：{'行号': 33, '当前股价': '36.81', '每股收益': '1.70', '股息(TTM)': '0.42', '总股本': '84.84'} }
def get_stock_info_dict(xueqiu_url, stock_row_num_dict):
    stock_info_dict = {}
    for stock_name, row_num in stock_row_num_dict.items():
        stock_code = stock_name.split("_")[1]
        stock_info_dict[stock_name] = get_stock_info(xueqiu_url, stock_code, row_num)
    return stock_info_dict


# 更新原有数据内容
def update_excel(file, stock_info_dict):
    wb = openpyxl.load_workbook(file)
    sheet = wb.get_sheet_by_name("A股")
    for stock_name, stock_info in stock_info_dict.items():
        # 修改单元格数据
        row_num = int(stock_info["行号"])
        sheet.cell(row=row_num, column=3, value=stock_info["当前股价"])
        sheet.cell(row=row_num, column=14, value=stock_info["每股收益"])
        sheet.cell(row=row_num, column=15, value=stock_info["股息(TTM)"])
        sheet.cell(row=row_num, column=16, value=stock_info["总股本"])
    wb.save(file)  # 将修改完的数据保存入Excel


def run(file, xueqiu_url):
    """
       【 更新当前价格信息：股价、每股收益、TTM股息、总股本 】
       1.从"价格指标-副本"中获取股票行号字典
          { "三一重工_600031"：33 }
       2.通过雪球网获取对应股票的相关信息字典
          { "三一重工_600031"：{'行号': 33, '当前股价': '36.81', '每股收益': '1.70', '股息(TTM)': '0.42', '总股本': '84.84'}}
       3.更新数据

       参考资料：
       https://cuiqingcai.com/1319.html
    """

    # 从"价格指标-副本"中获取股票行号字典
    stock_row_num_dict = get_stock_row_num_dict(file)
    print(stock_row_num_dict)
    print(len(stock_row_num_dict))

    # 通过雪球网获取对应股票的相关信息字典
    stock_info_dict = get_stock_info_dict(xueqiu_url, stock_row_num_dict)
    for key, value in stock_info_dict.items(): print(key + str(value))

    # 更新原有数据内容
    update_excel(file, stock_info_dict)


if __name__ == '__main__':

    file = "/Users/micllo/Downloads/A年报数据抓取/价格指标-副本.xlsx"
    xueqiu_url = "https://xueqiu.com/S/"
    run(file, xueqiu_url)
