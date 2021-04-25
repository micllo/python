# -*- coding: utf-8 -*-
import time, random
from functools import wraps
from json import dumps


"""
    [ 函 数 装 饰 器 ]
"""
def first(func):
    @wraps(func)  # 不改变使用装饰器原有函数的结构(如__name__, __doc__)
    def wrapper(*args, **kwargs):
        """__doc__ : first"""
        print("第一层装饰器 start ....")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("运行时间为%s" % (end_time - start_time))
        print("第一层装饰器 end ....")
        return result
    return wrapper


def second(func):
    @wraps(func)  # 不改变使用装饰器原有函数的结构(如__name__, __doc__)
    def wrapper(*args, **kwargs):
        """__doc__ : second"""
        print("第二层装饰器 start 。。。。")
        result = func(*args, **kwargs)
        print("第二层装饰器 end 。。。。")
        return result
    return wrapper


@second  # add = second(first(add))
@first   # add = first(add)
def add(x, y):
    """__doc__ : add"""
    time.sleep(random.randrange(1, 3))
    print("x + y =  %s" % (x + y))
    return "sum :" + str(x + y), "second_param"


# res = add(4, 5)  # 调用函数装饰器
# print "=============="
# print res
# print add.__name__
# print add.__doc__


"""
    [ 类 装 饰 器（函数调用）]
"""
class Foo(object):
    def __init__(self, func):
        self._func = func

    def __call__(self):
        print('class decorator runing')
        self._func()
        print('class decorator ending')


@Foo  # bar = Foo(bar)
def bar():
    print('bar')

# bar()  # 函数调用类装饰器


"""
    [ 类 装 饰 器（类函数调用）]
"""
class Foo2(object):
    def __init__(self):
        pass

    def __call__(self, func):
        def _call(*args, **kw):
            print('class decorator runing')
            result = func(*args, **kw)
            print('class decorator ending')
            return result
        return _call


class Test(object):
    @Foo2()  # bar = Foo2()(bar)
    def bar(self, x, y):
        print("sum : " + str(x + y))
        return x + y


# print Test().bar(3, 8)  # 类函数调用类装饰器


"""
    [ 装 饰 器（带参数）]
    1.先执行'log_slow_call(threshold=2)'方法返回装饰器<decorator>，然后用装饰器<decorator>装饰'sleep_secondes'方法
"""


def log_slow_call(func=None, threshold=1):
    def decorator(func):
        def proxy(*args, **kwargs):
            start_ts = time.time()
            result = func(*args, **kwargs)
            end_ts = time.time()
            seconds = end_ts - start_ts
            print(seconds)
            if seconds > threshold:
                print('slow call: {name} in {seconds}s'.format(name=func.func_name, seconds=seconds))
            return result
        return proxy

    if func is None:
        return decorator
    else:
        return decorator(func)


@log_slow_call(threshold=2)  # sleep_seconds = (log_slow_call(sleep_seconds, threshold=2))(sleep_seconds)
def sleep_seconds(seconds):
    time.sleep(seconds)
    return "执行完毕"

# sleep_seconds(3)


if __name__ == "__main__":
    # res = add(4, 5)  # 调用函数装饰器
    # print("==============")
    # print(res)
    # print(add.__name__)
    # print(add.__doc__)

    # bar()  # 函数调用类装饰器
    # print(Test().bar(3, 8))  # 类函数调用类装饰器
    # print(add.__name__, add.__doc__)

    print(sleep_seconds(3))
