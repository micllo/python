# -*- coding: utf-8 -*-
from datetime import timedelta
from celery.schedules import crontab


# 【 主配置文件 】/etc/default/celeryd
BASE_PATH = "/Users/micllo/Documents/works/GitLab/python/"
# 设置 celery 服务器 hostname
CELERYD_NODES = "MAC_192.168.3.102"
CELERY_BIN = BASE_PATH + "venv/bin/celery"
# 设置 celery 实例对象
CELERY_APP = "celery_app.app"  # 当前目录名称.celery实例名称
CELERYD_CHDIR = BASE_PATH
# 设置 worker 并发数
CELERYD_OPTS = "--concurrency=8"
# CELERYD_LOG_FILE = BASE_PATH + "logs/%N.log"
# CELERYD_PID_FILE = BASE_PATH + "logs/%N.pid"
CELERYD_USER = "centos"
CELERYD_GROUP = "centos"
CELERY_CREATE_DIRS = 1


# 【 项目配置 】
CELERY_QUEUE_HA_POLICY = 'all'

# 任务发送完成是否需要确认（ 若celery服务挂了，未完成的任务会重新进入队列 ）
CELERY_ACKS_LATE = True

# 结果持久化 （ 若rabbitmq服务重启了，其result仍然保留着 ）
CELERY_RESULT_PERSISTENT = True

# celery work 每次去rabbitmq预取任务的数量
CELERYD_PREFETCH_MULTIPLIER = 1

# 任务序列化方式
CELERY_TASK_SERIALIZER = 'json'

# 执行任务结果序列化方式
CELERY_RESULT_SERIALIZER = 'json'

# 指定任务接受的内容序列化类型
CELERY_ACCEPT_CONTENT = ['json']

CELERY_ENABLE_UTC = True

# 指定 Broker
# BROKER_URL = 'redis://127.0.0.1:6379/3'
BROKER_URL = 'amqp://micllo:micllo@127.0.0.1:5672/test'

# 指定 Backend ( 可以不指定 )
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/4'
CELERY_RESULT_BACKEND = 'amqp://micllo:micllo@127.0.0.1:5672/test'

# 指定时区，默认是 UTC
CELERY_TIMEZONE = 'Asia/Shanghai'
# CELERY_TIMEZONE = 'UTC'

# 并发worker数
CELERYD_CONCURRENCY = 8

# 指定导入的任务模块（ .py 文件 ）
CELERY_IMPORTS = ('celery_app.task1', 'celery_app.task2')

# 某个程序中出现的队列，在broker中不存在，则立刻创建它
CELERY_CREATE_MISSING_QUEUES = True

# 非常重要,有些情况下可以防止死锁
CELERYD_FORCE_EXECV = True

# 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死
# CELERYD_TASK_TIME_LIMIT = 60

# 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 90}

# 定时任务
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
         'task': 'celery_app.task1.add',
         'schedule': timedelta(seconds=30),       # 每 30 秒 执行一次
         'args': (5, 8)                           # 任务函数参数
    },
    'multiply-at-some-time': {
        'task': 'abc',
        'schedule': crontab(hour=9, minute=50),    # 每天早上 9 点 50 分执行一次
        'schedule': crontab(minute="*/1"),          # 每 分 钟 执行一次
        'schedule': crontab(minute=0, hour="*/1"),  # 每 小 时 执行一次
        'args': (3, 7)                              # 任务函数参数
    }
}


################################################

# *** 启动 定时（发布任务）***
# celery -A celery_app.app beat --loglevel=info

# *** 启动 worker（执行任务）***
# celery -A celery_app.app worker --loglevel=info
# celery -A celery_app.app worker -Q celery --loglevel=info

# *** 合 并 启 动 ***
# celery -B -A celery_app.app worker --loglevel=info


# *** 其他格式 ***
# nohup celery beat -s /var/log/celerybeat-schedule  --logfile=/var/log/celerybeat.log  -l info &
# nohup celery worker -f /var/log/boas_celery.log -l INFO &

################################################
