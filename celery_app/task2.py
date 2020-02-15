# -*- coding: utf-8 -*-
import time
from celery_app import app


@app.task(name="abc")
def multiply(x, y):
    time.sleep(5)
    return x * y