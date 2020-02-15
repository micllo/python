# -*- coding: utf-8 -*-

import sys
sys.path.append("./")
from tqdm import tqdm, trange
import contextlib
from time import sleep


class DummyTqdmFile(object):
    """
    进度条类
    """
    file = None

    def __init__(self, file):
        self.file = file

    def write(self, x):
        # 输出打印进度条
        if len(x.rstrip()) > 0:
            tqdm.write(x, file=self.file)


@contextlib.contextmanager
def stdout_redirect_to_tqdm():
    """
    进度条显示
    :return:
    """
    save_stdout = sys.stdout
    try:
        sys.stdout = DummyTqdmFile(sys.stdout)
        yield save_stdout
    # 出错跳出
    except Exception as exc:
        raise exc
    # 结束终止
    finally:
        sys.stdout = save_stdout


def test_bar():
    with stdout_redirect_to_tqdm() as save_stdout:
        for index_num in tqdm(range(5), file=save_stdout, dynamic_ncols=True):
            print index_num
            sleep(1)
    print 'Done!'


def test_bar2():
    for index_num in tqdm(range(5), file=sys.stdout):
        print index_num
        sleep(1)
    print 'Done!'


if __name__ == '__main__':

    test_bar()
    print " "
    test_bar2()
    # aaa = sys.stdout
    # print type(sys.stdout)
    # sys.stdout = DummyTqdmFile(sys.stdout)
    # print type(sys.stdout)
    # sys.stdout = aaa
    # print type(sys.stdout)
    #
    # print "111111"

    # text = ""
    # for char in tqdm(["a", "b", "c", "d"]):
    #     text = text + char
    #     sleep(1)
    # print text

    # for i in trange(100):
    #     sleep(0.01)

    # pbar = tqdm(["a", "b", "c", "d"])
    # for char in pbar:
    #     sleep(0.1)
    #     pbar.set_description("Processing %s" % char)

    # for i in tqdm(range(3), desc='1st loop'):
    #     for j in trange(10, desc='2nd loop', leave=True):
    #         sleep(0.1)
    #     print " "