# -*- coding: utf-8 -*-

import time
from celery_app import app


@app.task
def add(x, y):
    time.sleep(10)
    return x + y