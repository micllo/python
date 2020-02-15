# -*- coding:utf-8 -*-
import unittest
import os
# import sys
# sys.path.append(r'..')
import HTMLTestRunnerCN


# 测试用例
class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCase1(self):
        self.assertEqual(2, 2, "testError")

    def testCase2(self):
        self.assertEqual(2, 3, "testError")

    def testCase3(self):
        self.assertEqual(2, 5, "测试错误")

    def testCase4(self):
        self.assertEqual(2, 1, "测试错误")

    def testCase5(self):
        pass


class APITestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCase1(self):
        self.assertEqual(2, 2, "testError")

    def testCase2(self):
        self.assertEqual(3, 3, "testError")

    def testCase3(self):
        self.assertEqual(5, 5, "testError")

    def testCase4(self):
        self.assertEqual(2, 1, "测试错误")

    def testCase5(self):
        self.assertEqual(2, 9, "testError")

    def testCase6(self):
        pass


# 添加Suite
def suite():
    # 定义一个单元测试容器
    suite_test = unittest.TestSuite()
    # 将测试用例加入到容器
    suite_test.addTest(MyTestCase("testCase1"))
    suite_test.addTest(MyTestCase("testCase2"))
    suite_test.addTest(MyTestCase("testCase3"))
    suite_test.addTest(MyTestCase("testCase4"))
    suite_test.addTest(MyTestCase("testCase5"))
    suite_test.addTest(APITestCase("testCase1"))
    suite_test.addTest(APITestCase("testCase2"))
    suite_test.addTest(APITestCase("testCase3"))
    suite_test.addTest(APITestCase("testCase4"))
    suite_test.addTest(APITestCase("testCase5"))
    suite_test.addTest(APITestCase("testCase6"))
    return suite_test


'''
   【 pycharm编辑器的执行问 】
   由于 Preferences 中设置了 Tools > Python Integrated Tools > Default test runner : Unittests
   所以 pycharm 运行该脚本时会默认执行 Unittests 框架设置的内容 此时的 __name__ = HTMLTestReport.test_HTMLTestRunner
   从而忽略执行 if __name__ == '__main__': 下面的代码
   解决方案：手动赋值 __name__ = '__main__'
'''
print(__name__)
__name__ = '__main__'

if __name__ == '__main__':

    current_path = os.path.join(os.getcwd())
    print(current_path)

    # 确定生成报告的路径
    filePath = 'HTMLTestReport/report/test_report.html'
    fp = open(filePath, 'wb')
    # 生成报告的Title,描述
    runner = HTMLTestRunnerCN.HTMLTestRunner(stream=fp, title='自动化测试报告', description='详细测试用例结果', tester="费晓春")
    # 运行测试用例
    runner.run(suite())
    # 关闭文件，否则会无法生成文件
    fp.close()
