#! -*- coding: utf-8 -*-

import requests
import time
from concurrent.futures import ThreadPoolExecutor


def get(url):
    print('GET {}'.format(url))
    response = requests.get(url)
    time.sleep(2)
    if response.status_code == 200:  # 200代表状态：下载成功了
        return {'url': url, 'content_len': len(response.text)}


if __name__ == '__main__':
    urls = [
        'http://www.cnblogs.com/linhaifeng',
        'https://www.python.org',
        'https://www.openstack.org',
    ]

    pool = ThreadPoolExecutor(2)
    # map取代了for+submit
    # res = pool.map(get, "url1","url2","url3")
    res = pool.map(get, urls)

    pool.shutdown()  # 相当于进程池里的close和join
    print('=' * 30)
    for r in res:  # 返回的是一个迭代器
        print(r)
