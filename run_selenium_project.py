# coding=utf-8
import unittest
from HTMLTestRunnerCN import HTMLTestRunner
import os
from selenium_project.testcase.test_booking_tickets import BookingTickets


# 终端执行：
# python3 /Users/micllo/Documents/works/GitLab/python/run_selenium_project.py
if __name__ == "__main__":

    # 添加 '测试类'中的'测试方法'
    suite = unittest.TestSuite()
    suite.addTest(BookingTickets("test_search_tickets"))
    suite.addTest(BookingTickets("test_demo"))

    current_path = os.path.join(os.getcwd())
    print("\n" + current_path + "\n")

    # 确定生成报告的路径
    filePath = 'selenium_project/report/testReport.html'
    fp = open(filePath, 'wb')
    # 生成报告的Title,描述
    runner = HTMLTestRunner(stream=fp, title='自动化测试报告', description='详细测试用例结果', tester="费晓春")
    # 运行测试用例
    runner.run(suite)
    # 关闭文件，否则会无法生成文件
    fp.close()