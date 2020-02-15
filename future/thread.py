#! -*- coding: utf-8 -*-
import threading
from time import sleep


def display_name(name):
    sleep(2)
    print("用户名：" + name)


class MyTest(threading.Thread):

    def __init__(self, func, args):
        super(MyTest, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        print("ThreadName：" + self.name)
        self.func(self.args)


if __name__ == '__main__':
    t1 = MyTest(func=display_name, args="小王")
    t2 = MyTest(func=display_name, args="小张")
    t1.start()
    t2.start()

    t1.join()
    t2.join()
    print('线程结束')