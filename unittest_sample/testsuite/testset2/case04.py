# coding=utf-8
import unittest
import time


class Test4(unittest.TestCase):

    def setUp(self):
        time.sleep(1)
        print("\n================ 开始执行 case04 ================\n")

    def tearDown(self):
        time.sleep(1)
        print("\n++++++++++++++++ case04 执行完毕 ++++++++++++++++\n")

    def test_07(self):
        print("【 执行 文件case04 - 用例test_07 】")

    def test_08(self):
        print("【 执行 文件case04 - 用例test_08 】")


if __name__ == "__main__":
    unittest.main()