# coding=utf-8
from selenium.webdriver.common.action_chains import ActionChains


def browser_close(driver):
    driver.quit()


def open_base_site(driver, url):
    driver.get(url)


def locator_id(driver, element):
    return driver.find_element_by_id(element)


def locator_css(driver, element):
    return driver.find_element_by_css_selector(element)


def locator_xpath(driver, element):
    return driver.find_element_by_xpath(element)


def locator_js_for_remove_readonly(driver, element):
    """
    通过js移除元素的readonly属性
    :param element:
    :return:
    """
    driver.execute_script("document.getElementById(" + "'" + element + "'" + ").removeAttribute('readonly')")


def click_blank(driver):
    """
    点击页面空白处的操作
    :return:
    """
    ActionChains(driver).move_by_offset(0, 0).click().perform()


# class BrowserAction(object):
#
#     def __init__(self):
#         self.driver = None
#
#     def start(self, driver_type):
#         if driver_type == 'chrome':
#             self.driver = webdriver.Chrome()
#         else:
#             self.driver = webdriver.Firefox()
#         self.driver.implicitly_wait(10)
#
#     def close(self):
#         self.driver.quit()
#
#     def get_driver(self):
#         return self.driver
#
#     def open_base_site(self, url):
#         self.driver.get(url)
#
#     def locator_id(self, element):
#         return self.driver.find_element_by_id(element)
#
#     def locator_css(self, element):
#         return self.driver.find_element_by_css_selector(element)
#
#     def locator_xpath(self, element):
#         return self.driver.find_element_by_xpath(element)
#
#     def locator_js_for_remove_readonly(self, element):
#         """
#         通过js移除元素的readonly属性
#         :param element:
#         :return:
#         """
#         self.driver.execute_script("document.getElementById("+"'"+element+"'"+").removeAttribute('readonly')")
#
#     def click_blank(self):
#         """
#         点击页面空白处的操作
#         :return:
#         """
#         # 取代 from selenium.webdriver.common.action_chains import ActionChains 的方式
#         # 通过导入的'webdriver'包中的'__init__.py'初始化导入配置文件，找到'action_chains.py'文件的'ActionChains'类并实例化
#         action_chains = webdriver.ActionChains(self.driver)
#         action_chains.move_by_offset(0, 0).click().perform()


if __name__ == "__main__":
   pass
