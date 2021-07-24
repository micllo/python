"""
    实现 单例模式
"""

# 方法一：
class Singleton1(type):

    def __init__(cls, name, bases, dict):
        super(Singleton1, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton1, cls).__call__(*args, **kwargs)
        return cls.instance


class MyClass(object):
    __metaclass__ = Singleton1


# 方法二：
def singleton2(cls):
    cls_instance = {}  # { 类：实例对象 }

    def get_instance(*args, **kwargs):
        if cls_instance.get(cls) is None:
            cls_instance[cls] = cls(*args, **kwargs)
        return cls_instance[cls]

    return get_instance


@singleton2
class test(object):

    def __init__(self, name):
        self.name = name


if __name__ == '__main__':

    t1 = test("messi")
    t2 = test("gio")
    print(id(t1))
    print(id(t2))
    print(t1.name)
    print(t2.name)
