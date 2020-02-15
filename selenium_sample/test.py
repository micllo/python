# coding=utf-8
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import time

wd = webdriver.Chrome()
# wd = webdriver.Firefox()

# 远程启动 mac-win10虚拟机 （ 10.211.55.6 ）
# wd = webdriver.Remote(command_executor='http://10.211.55.6:4444/wd/hub',
#                       desired_capabilities=DesiredCapabilities.CHROME)
#
# wd = webdriver.Remote(command_executor='http://10.211.55.6:4444/wd/hub',
#                       desired_capabilities=DesiredCapabilities.FIREFOX)
#
# wd = webdriver.Remote(command_executor='http://10.211.55.6:4444/wd/hub',
#                       desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)


wd.maximize_window()
wd.get("https://www.baidu.com")    # 打开百度浏览器
wd.find_element_by_id("kw").send_keys("selenium")   # 定位输入框并输入关键字
wd.find_element_by_id("su").click()   #点击[百度一下]搜索
time.sleep(3)   #等待3秒
wd.quit()   #关闭浏览器


