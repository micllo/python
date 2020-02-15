# coding:UTF-8

import sys
import requests
from bs4 import BeautifulSoup
import xlrd
import xlwt
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
from threading import currentThread

# reload(sys)
# sys.setdefaultencoding("utf-8")
# print(sys.path)


class Tools:

    @staticmethod
    def get_page_content(method, url):
        """
        [ 抓取网页内容 ]
        :param method:
        :param url:
        :return:
        """
        if method == "get":
            response = requests.get(url)
        elif method == "post":
            response = requests.post(url)
        else:
            response = requests.get(url)
        return BeautifulSoup(response.content, 'html.parser')  # 解析网页数据

    @staticmethod
    def set_style(name, bold, colour, size):
        """
        [ 设置excel样式 ]
        :param name:
        :param bold:
        :param colour:
        :param size:
        :return:
        """
        style = xlwt.XFStyle()  # 初始化样式对象
        font = xlwt.Font()  # 设置：字体、加粗、颜色(索引)、大小(x20)
        font.name = name
        font.bold = bold
        font.colour_index = colour
        font.height = size
        style.font = font
        al_style = xlwt.Alignment()  # 设置：水平居中、垂直居中
        al_style.horz = 0x02
        al_style.vert = 0x01
        style.alignment = al_style
        return style

    @staticmethod
    def get_cell_data(file_name, table_index, row_num, col_num):
        """
        [ 获取某表的某单元格数据 ]
        :param file_name:
        :param table_index:
        :param row_num:
        :param col_num:
        :return:
        """
        data = xlrd.open_workbook(file_name)  # 打开xls文件、获取第x张表
        table = data.sheets()[table_index]
        return table.cell_value(row_num, col_num)

    @staticmethod
    def send_mail(receiver, nickname, subject, content, xls_name):
        """
        [ 发送邮件 ]
        :param receiver:
        :param nickname:
        :param subject:
        :param content:
        :param xls_name:
        :return:
        """
        sender = "error@daihoubang.com"  # 发件人邮箱账号
        sender_passwd = "Abc123456"  # 发件人邮箱密码
        try:
            if xls_name == "NULL" or xls_name == "":
                msg = MIMEText(content, 'plain', 'utf-8')
            else:
                # 将xls作为附件添加到邮件中
                msg = MIMEMultipart()
                # 创建MIMEText对象，保存xls文件
                attach = MIMEText(open(xls_name, 'rb').read(), 'base64', 'utf-8')
                # 指定当前文件格式类型
                attach['Content-type'] = 'application/octet-stream'
                # 配置附件显示的文件名称,当点击下载附件时，默认使用的保存文件的名称
                # gb18030 qq邮箱中使用的是gb18030编码，防止出现中文乱码
                attach['Content-Disposition'] = str("attachment;filename=" + xls_name.split("/")[-1]).decode(
                    'utf-8').encode('gb18030')
                # 把附件添加到msg中
                msg.attach(attach)
            msg['From'] = formataddr(["公司邮箱", sender])  # 发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr([nickname, receiver])  # 收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = subject
            server = smtplib.SMTP()  # 创建smtp对象
            server.connect(host="smtp.mxhichina.com", port="25")  # 连接smtp服务
            # server.set_debuglevel(1)  # 开启发送debug模式，把发送邮箱的过程显示出来
            server.starttls()  # 启动安全传输模式
            server.login(sender, sender_passwd)  # 发件人邮箱账号、邮箱密码
            server.sendmail(sender, receiver, msg.as_string())  # 发送邮件
            # msg_content = string.join(['From:%s' % sender, 'To:%s' % receiver, 'Subject:%s' % subject, '', content], "\r\n")
            # server.sendmail(from_addr=sender, to_addrs=receiver, msg=msg_content)
            server.quit()  # 关闭smtp连接
            print "邮件发送成功！"
        except smtplib.SMTPException:
            print "邮件发送失败！"

    @staticmethod
    def mongo_connect(server, port):
        """
        [ 连接 mongo ]
        :param server:
        :param port:
        :return:
        """
        conn = MongoClient(server, port)
        pydb = conn.pydb  # 连接pydb数据库，没有则自动创建
        pyset = pydb.pyset  # 使用pyset集合，没有则自动创建
        return pyset


class FutureThread:

    def __init__(self, task_num, max_workers):
        self.task_num = task_num
        self.result = []
        self.executor = ThreadPoolExecutor(min(max_workers, task_num))

    def submit(self, func, *args):
        for i in range(self.task_num):
            future = self.executor.submit(func, *args)
            self.result.append(future)

    def join(self):
        self.executor.shutdown()

    def get_result(self):
        return self.result
