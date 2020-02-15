# -*- coding: utf-8 -*-

# 【 主配置文件 】/etc/default/celeryd
BASE_PATH = "/Users/micllo/Documents/works/GitLab/python/"
# work 任务节点
CELERYD_NODES = "MAC_192.168.56.213"
# celery 命令的绝对路径
CELERY_BIN = BASE_PATH + "venv/bin/celery"
# celery 实例对象（ 包名称.celery实例对象名称 ）
CELERY_APP = "flask_celery.celery_app"
# 项目根目录
CELERYD_CHDIR = BASE_PATH
# worker 并发数
CELERYD_OPTS = "--concurrency=8"
# CELERYD_LOG_FILE = BASE_PATH + "logs/test.log"
# CELERYD_LOG_FILE = BASE_PATH + "logs/%N.log"
# CELERYD_PID_FILE = BASE_PATH + "logs/%N.pid"
CELERYD_USER = "centos"
CELERYD_GROUP = "centos"
# 自动创建日志和 pid 文件
CELERY_CREATE_DIRS = 1


# 【 项目配置 】
# queue 镜像的备份策略，如果是'all'，则在所有 RabbitMQ 节点都备份 queue 镜像，也可以设置为节点名称列表
CELERY_QUEUE_HA_POLICY = 'all'

# 任务发送完成是否需要确认（ 若celery服务挂了，未完成的任务会重新进入队列 ）
CELERY_ACKS_LATE = True

# 结果持久化 （ 若rabbitmq服务重启了，其result仍然保留着 ）
# CELERY_RESULT_PERSISTENT = True

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
BROKER_URL = 'amqp://micllo:micllo@127.0.0.1:5672/fxc'

# 指定时区，默认是 UTC
CELERY_TIMEZONE = 'Asia/Shanghai'
# CELERY_TIMEZONE = 'UTC'

# 并发worker数
CELERYD_CONCURRENCY = 8

# 指定导入的任务模块（ .py 文件 ）
CELERY_IMPORTS = ('flask_celery.tasks')

# 指定 Backend ( 可以不指定 )
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/4'
CELERY_RESULT_BACKEND = 'amqp://micllo:micllo@127.0.0.1:5672/fxc'
# CELERY_RESULT_BACKEND = 'amqp'

# 某个程序中出现的队列，在broker中不存在，则立刻创建它
# CELERY_CREATE_MISSING_QUEUES = True

# 非常重要,有些情况下可以防止死锁
# CELERYD_FORCE_EXECV = True

# 单任务超时时间设置(强制杀掉worker,但不会报错误信息)
# CELERYD_TASK_TIME_LIMIT = 300

# 单任务超时时间设置(会有杀不掉的worker,会有报错误信息)
# CELERYD_TASK_SOFT_TIME_LIMIT = 300

# 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 90}
