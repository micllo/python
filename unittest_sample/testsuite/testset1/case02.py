# coding=utf-8
import unittest
import time


class Test2(unittest.TestCase):

    def setUp(self):
        time.sleep(1)
        print("\n================ 开始执行 case02 ================\n")

    def tearDown(self):
        time.sleep(1)
        print("\n++++++++++++++++ case02 执行完毕 ++++++++++++++++\n")

    def test_03(self):
        print("【 执行 文件case02 - 用例test_03 】")

    def test_04(self):
        print("【 执行 文件case02 - 用例test_04 】")


if __name__ == "__main__":
    unittest.main()