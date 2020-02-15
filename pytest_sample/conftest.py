#!/usr/bin/env python
# coding=utf-8
import pytest


# 每个使用的方法(函数)都会执行一次
@pytest.fixture(scope='function')
def exec_function():
    print("\n方法：初始化\n")  # 每个用例执行前的初始化操作
    yield
    print("\n方法：还原操作\n")  # 每个用例执行后的还原操作


# 每个类都会执行一次，类中有多个方法调用的，只在第一个方法调用时使用
@pytest.fixture(scope='class')
def exec_class():
    print("\n类：初始化\n")
    yield
    print("\n类：还原操作\n")


# 一个 .py 文件执行一次。一个.py文件可能包含多个类和方法
@pytest.fixture(scope='module')
def exec_module():
    print("\npy文件：初始化\n")
    yield
    print("\npy文件：还原操作\n")