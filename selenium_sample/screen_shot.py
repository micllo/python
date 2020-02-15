# coding=utf-8
import time
from selenium import webdriver
from PIL import Image
import os

driver = webdriver.Chrome()
driver.get("https://user.qunar.com/passport/login.jsp?")
time.sleep(2)
driver.maximize_window()

driver.find_element_by_link_text("密码登录").click()
time.sleep(1)

current_path = os.path.join(os.getcwd())
print(current_path)

image_path = current_path + "/img/qu.png"
imgCode_path = current_path + "/img/t.png"
print(image_path)
print(imgCode_path)

# 页面截图
driver.save_screenshot(image_path)
time.sleep(1)

# 获取图片验证码位置
imgcode = driver.find_element_by_id("vcodeImg")
left = imgcode.location['x']
top = imgcode.location['y']
right = left + imgcode.size["width"]
bottom = top + imgcode.size["height"]
print("图片验证码左侧与屏幕左侧的距离：" + str(left))
print("图片验证码顶部与屏幕顶部的距离：" + str(top))
print("图片验证码右侧与屏幕左侧的距离：" + str(right))
print("图片验证码底部与屏幕顶部的距离：" + str(bottom))

# 裁剪截图中的图片验证码
im = Image.open(image_path)
im = im.crop((left, top, right, bottom))
im.save(imgCode_path)

driver.quit()