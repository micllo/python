#! -*- coding: utf-8 -*-

from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from threading import currentThread
import os, time, random


def task(n):
    print("%s is running " % os.getpid())
    time.sleep(random.randint(1, 3))
    return n * 2


if __name__ == '__main__':
    start = time.time()
    # 创建进程池（设定最多使用4个进程）
    executor = ProcessPoolExecutor(4)

    res = []
    for i in range(10):
        # 异步提交任务 submit(方法名称，方法参数)
        future = executor.submit(task, i)
        res.append(future)

    # 等待所有进程执行完毕
    executor.shutdown()
    print("++++>")
    for r in res:
        print(r.result())

    end = time.time()
    print(end - start)