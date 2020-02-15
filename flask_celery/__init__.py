# -*- coding: utf-8 -*-

from flask import Flask
from celery import Celery


flask_app = Flask(__name__)

# 在 flask_celery 包同级目录下执行 Celery Worker 监听任务
# celery -A flask_celery worker --loglevel=info
# celery -A flask_celery.celery_app worker --loglevel=info
# 注：-A 可不指定celery的实例对象，会自动搜索到 flask_celery 包下的 __init__.py文件中的该对象
celery_app = Celery(flask_app.name)
celery_app.config_from_object('flask_celery.config')
