# coding=utf-8
import unittest
import time


class Test1(unittest.TestCase):

    def setUp(self):
        time.sleep(1)
        print("\n================ 开始执行 case01 ================\n")

    def tearDown(self):
        time.sleep(1)
        print("\n++++++++++++++++ case01 执行完毕 ++++++++++++++++\n")

    def test_01(self):
        print("【 执行 文件case01 - 用例test_01 】")

    def test_02(self):
        print("【 执行 文件case01 - 用例test_02 】")


if __name__ == "__main__":
    unittest.main()