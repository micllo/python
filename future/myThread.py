#! -*- coding: utf-8 -*-

from threading import Thread, currentThread
import time
import queue


class MyThread(Thread):

    def __init__(self, queue):
        super(MyThread, self).__init__()
        self.queue = queue
        self.daemon = True  # 子线程跟着主线程一起退出
        self.start()

    def run(self):
        """
                1、让他始终去运行，
                2、去获取queue里面的任务，
                3、然后给任务分配函数去执行（获取任务在执行）
                :return:
        """
        while True:
            func, args, kwargs = self.queue.get()  # 从队列中获取任务
            func(*args, **kwargs)
            self.queue.task_done()  # 计数器  执行完这个任务后  （队列-1操作)


class MyPool(object):
    """
    在任务来到之前，提前创建好线程，等待任务
    """

    def __init__(self, num):  # 线程数量
        self.num = num
        self.queue = queue.Queue()
        for i in range(self.num):
            MyThread(self.queue)

    def submit(self, func, args=(), kwargs={}):
        self.queue.put((func, args, kwargs))

    def join(self):
        self.queue.join()  # 等待队列里面的任务处理完毕


def task(i):
    print(currentThread().getName(), i)
    time.sleep(2)


if __name__ == '__main__':
    start = time.time()
    pool = MyPool(3)  # 实例化一个线程池
    for i in range(4):
        pool.submit(task, args=(i,))
    pool.join()
    print('运行的时间{}秒'.format(time.time() - start))