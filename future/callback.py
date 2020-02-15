#! -*- coding: utf-8 -*-

import requests
import time
from concurrent.futures import ThreadPoolExecutor


def get(url):
    print('GET {}'.format(url))
    response = requests.get(url)
    time.sleep(2)
    if response.status_code == 200:  # 200代表状态：下载成功了
        return {'url': url, 'content': response.text}


def parse(res):
    print('%s parse res is %s' % (res['url'], len(res['content'])))
    return '%s parse res is %s' % (res['url'], len(res['content']))


def save(res):
    print('save', res)


def task(res):
    res = res.result()
    par_res = parse(res)
    save(par_res)


if __name__ == '__main__':
    urls = [
        'http://www.cnblogs.com/linhaifeng',
        'https://www.python.org',
        'https://www.openstack.org',
    ]

    pool = ThreadPoolExecutor(2)
    for i in urls:
        # 回调函数
        # 先调用get方法，当该方法返回res结果后，再调用task方法(res作为参数)
        # 如同：res = pool.submit(get, i)  task(res)
        # 目的：哪个线程执行完毕了，可马上执行回调函数
        pool.submit(get, i).add_done_callback(task)
    pool.shutdown()  # 等待所有线程执行完毕

