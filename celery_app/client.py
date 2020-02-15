# -*- coding: utf-8 -*-
from celery_app import task1, task2

result_list = []


def exec_task():
    print '任务调度。。。。。。'
    # task1.add.apply_async(args=[2, 8])
    # task2.multiply.apply_async(args=[3, 7])
    result = task1.add.delay(2, 8)
    print result.id
    print type(result.id)
    # result_list.append(task2.multiply.delay(3, 7))
    # for i in range(1, 21):
    #     result_list.append(task1.add.delay(100, i))


def get_result():
    """
      [ 获取结果 （ CELERY_RESULT_BACKEND ）]
    """
    print "获取结果。。。。。。"
    for i, result in enumerate(result_list):
        print result.id  # 获取redis的唯一ID
        print result.status  # 获取任务状态：PENDING, START, SUCCESS
        try:
            print result.get(timeout=15)
        except Exception:
            print "未获取到结果"
        finally:
            print "执行完毕！"


if __name__ == "__main__":
    exec_task()
    # get_result()
