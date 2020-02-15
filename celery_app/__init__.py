# -*- coding: utf-8 -*-

from celery import Celery

# 在 celery_app 包同级目录下执行 Celery Worker 监听任务
# celery -A celery_app worker --loglevel=info
app = Celery('demo')                          # 创建 Celery 实例
app.config_from_object('celery_app.config')   # 通过 Celery 实例加载配置模块