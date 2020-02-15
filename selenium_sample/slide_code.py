# coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver import ActionChains

driver = webdriver.Chrome()
# driver = webdriver.Firefox()
#
# # 远程启动 mac-win10虚拟机 （ 10.211.55.6 ）
# driver = webdriver.Remote(command_executor='http://10.211.55.6:4444/wd/hub',
#                       desired_capabilities=DesiredCapabilities.CHROME)


# 打开携程注册页面
driver.get("https://passport.ctrip.com/user/reg/home")
time.sleep(1)

# 点击"同意并继续"按钮
driver.find_element_by_css_selector("#agr_pop>div.pop_footer>a.reg_btn.reg_agree").click()
time.sleep(1)

# 获取滑块元素的宽和高
sour = driver.find_element_by_css_selector("#slideCode>div.cpt-drop-box>div.cpt-drop-btn")
print(sour.size['width'])
print(sour.size['height'])

# 获取滑块区域的宽和高
ele = driver.find_element_by_css_selector("#slideCode>div.cpt-drop-box>div.cpt-bg-bar")
print(ele.size['width'])
print(ele.size['height'])

# 拖动滑块
# source：鼠标拖动的原始元素
# xoffset：鼠标把元素拖动到另外一个位置的x坐标
# yoffset：鼠标把元素拖动到另外一个位置的y坐标
ActionChains(driver).drag_and_drop_by_offset(sour, ele.size['width'], ele.size['height']).perform()
time.sleep(3)

driver.quit()