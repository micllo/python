import re
import copy
import json
from io import StringIO
import traceback, os
from threading import Thread
import time


# a = 'A234567890'
# if re.match(r'[a-zA-Z\_][0-9a-zA-Z\_]{1,2}', a):
#     print('OK')
# else:
#     print('Failed')
#
# res = re.match(r'[a-zA-Z\_][0-9a-zA-Z\_]{1,2}', a)
# print(res)
# print(res.group(0))
# # print(res.group(1))

def aaa(name, age):
    time.sleep(5)
    print(name, age)


def async_aaa(name, age, is_join=False):
    args = (name, age)
    thr = Thread(target=aaa, args=args)
    thr.start()
    if is_join:
        thr.join()
    print("over")


def singleton(cls):

    cls_instance = {}

    def get_instance(*args, **kwargs):
        if cls_instance.get(cls) is None:
            cls_instance[cls] = cls(*args, **kwargs)
        return cls_instance[cls]

    return get_instance


@singleton
class test(object):

    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    pass
    products = [["iphone", 6888], ["MacPro", 14800], ["小米6", 2499], ["Coffee", 31], ["Book", 60], ["Nike", 699]]
