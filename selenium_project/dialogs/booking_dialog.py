# coding=utf-8
from selenium_project.support.browser_action import *


# '姓名'输入框
def name_field(driver):
    return locator_css(driver, "#pasglistdiv > div > ul > li:nth-child(2) > input")
