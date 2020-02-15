# coding=utf-8
from selenium_project.dialogs.home_dialog import *
from selenium_project.support import tools
import time


# 搜索车票（出发城市、到达城市、日期<当前日期往后几天>）
def search_ticket(driver, from_station, to_station, n):

    # 输入'出发城市'
    from_city_field(driver).clear()
    from_city_field(driver).send_keys(from_station)
    time.sleep(2)

    # 输入'到达城市'
    to_city_field(driver).clear()
    to_city_field(driver).send_keys(to_station)
    time.sleep(2)

    # 移除'出发时间'控件的'readonly'属性
    clear_readonly_attribute_for_departure_time_control(driver)
    time.sleep(2)

    # 清除'出发时间'控件的默认内容
    departure_time_field(driver).clear()
    time.sleep(2)

    # 在'出发时间'控件中输入日期
    departure_time_field(driver).send_keys(tools.date_n(n))

    # 点击页面空白处，使得'出发时间'控件的日历弹框消失
    click_blank(driver)
    time.sleep(2)

    # 单击'开始搜索'按钮
    search_btn(driver).click()
    time.sleep(2)

