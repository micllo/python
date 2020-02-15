# coding=utf-8
from selenium_project.dialogs.booking_dialog import *
import time


# 预订G104车次的车票
def booking_action(driver, name):
    name_field(driver).send_keys(name)
    time.sleep(3)
