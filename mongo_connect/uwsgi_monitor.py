# coding:UTF-8
import pymongo
import pandas as pd
import numpy as np

if __name__ == '__main__':

    """
    【 离娄项目 - uwsgi 监控 】
     在 platform_config > project_config 表中新增一列字段 uwsgi_monitor 并默认赋值为 open
    """

    # 创建mongo连接
    # myclient = pymongo.MongoClient('mongodb://localhost:27017/')  # monitor_lilou [local]
    myclient = pymongo.MongoClient('mongodb://192.168.25.202:25017/')  # monitor_lilou [uat]
    # myclient = pymongo.MongoClient('mongodb://10.76.88.75:27101/')  # monitor_lilou [wuxi]

    # 连接 数据库
    mydb = myclient['platform_config']
    # 指定文档名称
    mycol = mydb['project_config']
    # 修改文档内容
    update = {"$set": {"uwsgi_monitor": "close"}}
    mycol.update({}, update, multi=True)
