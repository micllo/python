# coding=utf-8
import unittest
import time


class Test3(unittest.TestCase):

    def setUp(self):
        time.sleep(1)
        print("\n================ 开始执行 case03 ================\n")

    def tearDown(self):
        time.sleep(1)
        print("\n++++++++++++++++ case03 执行完毕 ++++++++++++++++\n")

    def test_05(self):
        print("【 执行 文件case03 - 用例test_05 】")

    def test_06(self):
        print("【 执行 文件case03 - 用例test_06 】")


if __name__ == "__main__":
    unittest.main()