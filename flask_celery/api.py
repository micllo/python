# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../")
from flask import request
from flask_celery import flask_app
from flask_celery import tasks
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor
import datetime
import time


def get_tasks_mongo():
    mongo = MongoClient("127.0.0.1", 27017)
    task_db = mongo.celery_task       # 指定 celery_task 数据库
    tasks_collection = task_db.tasks  # 指定 tasks 集合
    return tasks_collection


# http://192.168.23.250:5678/flash_celery/analyze_id_ard?id_card=310102198602114417
@flask_app.route('/flash_celery/analyze_id_card', methods=['get'])
def analyze_id_card():
    """
      [ 解析身份证 API ]
    """
    id_card = request.args.get("id_card")
    result = tasks.analyze_id_card_task.delay(id_card)
    # <future> 设置线程池数量，并启动线程
    ThreadPoolExecutor(10).submit(save_result, id_card, result)
    return "身份证'" + id_card + "'解析任务已提交，请稍后查询，查询ID：" + result.id


# http://192.168.23.250:5678/flash_celery/batch_analyze_id_ard
@flask_app.route('/flash_celery/batch_analyze_id_card', methods=['get'])
def analyze_id_card_batch():
    """
      [ 批量解析20个身份证 API ]
    """
    task_id_list = []
    id_card_list = ["45022219820205068X", "320583198705178765", "440600198907063407", "610103197501044707", "632724198306131877",
                    "330681198004262133", "653001198002189078", "622923199303244566", "440600199412121702", "230381197706061702",
                    "321111197901227096", "230606199010059060", "371521199107027022", "130631197501176142", "371482198303270663",
                    "330303198407230042", "652924198601249899", "411324198810013323", "411323197905061722", "150502197811162076"]
    for i, id_card in enumerate(id_card_list):
        result = tasks.analyze_id_card_task.delay(id_card)
        task_id_list.append(result.id)
        ThreadPoolExecutor(10).submit(save_result, id_card, result)
    return "身份证解析任务已提交，请稍后查询，查询ID：" + str(task_id_list)


def save_result(id_card, result):
    """
      [ 保存解析结果（ 线程中执行 ）]
    """
    print result.id      # 获取redis的唯一ID
    print result.status  # 获取任务状态：PENDING, START, SUCCESS
    tasks_collection = get_tasks_mongo()
    result_dict = {}
    try:
        result_dict["task_result"] = result.get(timeout=15)
    except Exception:
        result_dict["task_result"] = "未获取到结果"
        print "未获取到结果"
    finally:
        result_dict["id_card"] = id_card
        result_dict["task_id"] = result.id
        result_dict["task_status"] = result.status
        tasks_collection.insert(result_dict)
        print "线程执行完毕！"


@flask_app.route('/flash_celery/get_analyze_result/<task_id>', methods=['get'])
def get_analyze_result(task_id):
    """
      [ 通过'task_id'获取结果 ]
    """
    tasks_collection = get_tasks_mongo()
    result = tasks_collection.find_one({"task_id": task_id})
    return "id_card : " + result["id_card"] + " -> " + result["task_result"]


if __name__ == "__main__":
    flask_app.run(host='0.0.0.0', port=6666, debug=True)