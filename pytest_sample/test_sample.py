#!/usr/bin/env python
# coding=utf-8
import pytest

# 自动引入同级目录中的conftest.py配置文件
# @pytest.fixture(scope='function')
# def login():
#     print("登录")  # 每个用例执行前的初始化操作
#     yield
#     print("注销")  # 每个用例执行后的还原操作


class TestClassOne:

    def test_1(self):
        print('测试用例1')

    def test_2(self, exec_function, exec_class, exec_module):
        print('测试用例2')

    def test_3(self, exec_function, exec_class, exec_module):
        print('测试用例3')


class TestClassTwo:

    def test_one(self, exec_function, exec_class, exec_module):
        print('类中的方法1')
        x = "this"
        assert 'w' in x

    @pytest.mark.skip # 跳过执行
    def test_two(self, exec_function, exec_class, exec_module):
        print('类中的方法2')
        x = "this"
        assert 'h' in x

    @pytest.mark.abc
    @pytest.mark.parametrize("input1, input2, output", [(5, 5, 10), (3, 5, 12)])  # 参数化测试
    def test_add(self, input1, input2, output):
        assert input1 + input2 == output, "failed error!"




if __name__ =="__main__":
    # pytest.main()

    # -s 表示显示print中的内容
    # --html=report.html 表示当前目录生成测试报告
    # -n NUM 表示多进程运行case
    # --reruns NUM 表示失败后重试的次数
    # -m 表示仅执行带有mark标记的case
    # -v 表示显示每个测试函数的执行结果
    # pytest.main(['test_sample.py', '-s', '--html=report.html'])
    # pytest.main(['test_sample.py', '-s', "-m=abc", '--html=report.html'])
    # pytest.main(['test_sample.py', '-v', '-s', '--html=report.html'])
    pytest.main(['test_sample.py::TestClassOne::test_2', '-v', '-s', '--html=report.html'])
