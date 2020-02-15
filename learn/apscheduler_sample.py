# coding:utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import datetime
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='../logs/apscheduler_log.txt',
                    filemode='a')


def aps_test(x):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)


def aps_error(x):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)
    print(1/0)


# 根据'id'删除相关任务
def aps_remove(x):
    scheduler.remove_job('interval_task')
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)


# 根据'id'停止相关任务
def aps_pause(x):
    scheduler.pause_job('cron_task')
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)


# 根据'id'恢复相关任务
def aps_resume(x):
    scheduler.resume_job('cron_task')
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)


# 监听出错的任务
def my_listener(event):
    if event.exception:
        print('任务出错了！！！！！！')
    else:
        print('任务照常运行...')


scheduler = BlockingScheduler()

scheduler.add_job(func=aps_test, args=('定时任务',), trigger='cron', second='*/5', id='cron_task')

scheduler.add_job(func=aps_error, args=('循环任务(会出错)',), trigger='interval', seconds=3, id='interval_task')

scheduler.add_job(func=aps_remove, args=('一次性任务,删除-循环任务(会出错)',),
                  next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=12), id='remove_task')

scheduler.add_job(func=aps_pause, args=('一次性任务,暂停-定时任务',),
                  next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=16), id='pause_task')

scheduler.add_job(func=aps_resume, args=('一次性任务,恢复-定时任务',),
                  next_run_time=datetime.datetime.now() + datetime.timedelta(seconds=30), id='resume_task')

scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

scheduler._logger = logging

scheduler.start()