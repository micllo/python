# coding=utf-8
from selenium_project.dialogs.tickets_dialog import *
import time


# 预订G104车次的车票
def booking_g104(driver):
    booking_btn_for_g104(driver).click()
    time.sleep(5)
