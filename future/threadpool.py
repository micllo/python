#! -*- coding: utf-8 -*-

from concurrent import futures

from flags import save_flag, get_flag, show, main

# 设定ThreadPoolExecutor 类最多使用几个线程
MAX_WORKERS = 20


# 下载一个图片
def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')
    return cc


def download_many(cc_list):
    # 设定工作的线程数量，使用约需的最大值与要处理的数量直接较小的那个值，以免创建多余的线程
    workers = min(MAX_WORKERS, len(cc_list))  # <4>
    # 使用工作的线程数实例化ThreadPoolExecutor类；
    # executor.__exit__方法会调用executor.shutdown(wait=True)方法，
    # 它会在所有线程都执行完毕前阻塞线程
    with futures.ThreadPoolExecutor(workers) as executor:  # <5>
        # map 与内置map方法类似，不过download_one 函数会在多个线程中并发调用；
        # map 方法返回一个生成器，因此可以迭代，
        # 迭代器的__next__方法调用各个Future 的 result 方法
        res = executor.map(download_one, sorted(cc_list))

    # 返回获取的结果数量；如果有现成抛出异常，会在这里抛出
    # 这与隐式调用next() 函数从迭代器中获取相应的返回值一样。
    return len(list(res))  # <7>
    return len(results)


if __name__ == '__main__':
    main(download_many)