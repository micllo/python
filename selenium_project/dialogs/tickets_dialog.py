# coding=utf-8
from selenium_project.support.browser_action import *


# G104车次的 '预订'按钮
def booking_btn_for_g104(driver):
    return locator_xpath(driver, "//*[starts-with(@id,'tbody-01-G1040')]/div[1]/div[6]/div[1]/a")

