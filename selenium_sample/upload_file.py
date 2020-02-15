# coding=utf-8
import time
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import ActionChains
from pywinauto.application import Application


# # 方法一【 mac 执行 】：input类型的upload 可以直接在"选择文件"框中输入文件路径
# wd = webdriver.Chrome()
# wd.maximize_window()
# wd.get("file:///Users/micllo/Documents/works/GitLab/python/learn/upload.html")
# wd.find_element_by_id("file").send_keys("/Users/micllo/Documents/works/GitLab/python/selenium_sample/log/test.log")
# time.sleep(2)
# wd.find_element_by_id("upload_btn").click()
# wd.quit()
# print("end")


####################################################################################################


# 方法二【 win 执行 】：非input类型的upload 只能在win系统中使用 AutoIt + pywinauto 进行定位（脚本只能在win中执行）

# 远程启动 mac-win10虚拟机 （ 10.211.55.6 ）
wd = webdriver.Remote(command_executor='http://10.211.55.6:4444/wd/hub',
                      desired_capabilities=DesiredCapabilities.CHROME)

wd.maximize_window()
wd.get("file:///C:/upload-test/upload.html")

# 点击"选择文件"框，开启弹框 （ 注意：由于input标签不能直接使用click方法，所有需要借助 ActionChains 鼠标行为事件 ）
input_file = wd.find_element_by_id("file")
ActionChains(wd).click(input_file).perform()
time.sleep(2)

app = Application()

# 先定位到窗口
# title_re：Basic Window Info > Title (表示窗体的title)
# class_name：Basic Window Info > Class
app = app.connect(title_re=r"打开", class_name=r"#32770")

# 找到"文件名"选择框，输入文件路径
# 第一个[]：Basic Window Info > Title
# 第二个[]：Basic Control Info > Class + Instance
app["打开"]["Edit1"].set_edit_text("C:\\upload-test\\file.txt")
time.sleep(2)

# 单击"打开"按钮,关闭弹框
app["打开"]["Button1"].click()
time.sleep(1)

# 点击"上传"按钮
wd.find_element_by_id("upload_btn").click()
time.sleep(1)

# 关闭浏览器
wd.quit()

print("end")
