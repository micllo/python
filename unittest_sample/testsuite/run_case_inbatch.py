# coding=utf-8
import unittest
import os


def all_cases(testset_name):
    # 查询测试用例路径
    case_path = os.path.join(os.getcwd(), testset_name)
    print(case_path)

    discover = unittest.defaultTestLoader.discover(case_path, pattern="case*.py", top_level_dir=None)
    print(discover)
    return discover


if __name__ == "__main__":
    runner =unittest.TextTestRunner()
    # 批量执行 testset1 目录下的测试用例文件
    runner.run(all_cases("testset1"))

