# coding=utf-8
import unittest
from selenium import webdriver
from selenium_project.support import tools
from selenium_project.pages import home_page
from selenium_project.pages import tickets_page
from selenium_project.pages import booking_page


class BookingTickets(unittest.TestCase):

    def setUp(self):
        # 启动浏览器
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)

    def tearDown(self):
        # 关闭浏览器
        self.driver.quit()

    # 用例一
    # 1.打开网址
    # 2.搜索火车票（首页）
    # 3.选择火车票（预订页）
    # 4.跳过登录（登录页）
    def test_search_tickets(self):

        tools.log("操作步骤：1.打开网址")
        self.driver.get("https://trains.ctrip.com/TrainBooking/SearchTrain.aspx")

        tools.log("操作步骤：2.搜索火车票（首页）")
        home_page.search_ticket(self.driver, "上海", "北京", 1)

        tools.log("操作步骤：3.选择火车票（预订页）")
        tickets_page.booking_g104(self.driver, )

        tools.log("操作步骤：4.跳过登录（登录页）")
        booking_page.booking_action(self.driver, "测试人员")

    # 用例二
    def test_demo(self):
        tools.log("用例二：1111111")
        self.driver.get("https://trains.ctrip.com/TrainBooking/SearchTrain.aspx")

        tools.log("用例二：2222222")
        home_page.search_ticket(self.driver, "上海", "北京", 1)
