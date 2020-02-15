# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../")
from flask_celery import celery_app
from parse_idcard import AnalyzeIDCard
import time


# 身份证解析任务
@celery_app.task
def analyze_id_card_task(id_card):
    analyze = AnalyzeIDCard(id_card)
    time.sleep(10)
    return analyze.analyze_id_card()
