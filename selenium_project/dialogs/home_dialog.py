# coding=utf-8
from selenium_project.support.browser_action import *


# '出发城市'输入框
def from_city_field(driver):
    return locator_id(driver, "notice01")


# '到达城市'输入框
def to_city_field(driver):
    return locator_id(driver, "notice08")


# '出发时间'控件
def departure_time_field(driver):
    return locator_id(driver, "dateObj")


# 移除'出发时间'控件的'readonly'属性
def clear_readonly_attribute_for_departure_time_control(driver):
    locator_js_for_remove_readonly(driver, "dateObj")


# '开始搜索'按钮
def search_btn(driver):
    return locator_id(driver, "searchbtn")
