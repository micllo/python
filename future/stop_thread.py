#! -*- coding: utf-8 -*-

import requests
import time
from concurrent.futures import ThreadPoolExecutor
import inspect
import ctypes
import threading


def get(url):
    print('GET {}'.format(url))
    response = requests.get(url)
    time.sleep(2)
    if response.status_code == 200:  # 200代表状态：下载成功了
        return {'url': url, 'content': response.text}


def parse(res):
    return '%s parse res is %s' % (res['url'], len(res['content']))


def save(res):
    print('save', res)


def task(res):
    res = res.result()
    par_res = parse(res)
    save(par_res)


def stop_thread(thread, exctype=SystemExit):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(thread.ident)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


# [<Thread(ThreadPoolExecutor-0_1, started daemon 123145460658176)>, <Thread(ThreadPoolExecutor-0_0, started daemon 123145455403008)>]
# <class 'threading.Thread'>
if __name__ == '__main__':
    urls = [
        'http://www.cnblogs.com/linhaifeng',
        'https://www.python.org',
        'https://www.baidu.com',
        'https://www.cnblogs.com/maxiaohei/p/7787256.html'
    ]

    pool = ThreadPoolExecutor(2)
    for url in urls:
        # 若要强行停止线程，则不能使用回调函数
        # pool.submit(get, i).add_done_callback(task)
        res = pool.submit(get, url)
        # task(res)
    thread_list = list(pool._threads)
    print(thread_list)
    time.sleep(1)
    for thread in thread_list:
        stop_thread(thread)
    print("stopped")
    print(thread_list)
    pool.shutdown()  # 等待所有线程执行完毕
    print(thread_list)
