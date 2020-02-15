# coding:UTF-8
import pymongo
import pandas as pd
import numpy as np

if __name__ == '__main__':

    """
     【 部署平台 - 新增 用户 关联 项目 】
      在 deploy > project_status 表中新增一条记录
    """

    # 创建mongo连接
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')  # monitor_lilou [local]
    # myclient = pymongo.MongoClient('mongodb://192.168.25.101:27017/')  # monitor_lilou [uat]


    # 连接 数据库
    mydb = myclient['deploy']
    # 指定文档名称
    mycol = mydb['project_status']

    # 插入相关记录
    # mydict = {"group": 1, "name": "feixiaochun", "project_names": ["Lilou", "test"]}
    # res = mycol.insert_one(mydict)
    # print res

    # 修改相关记录
    query = {"name": "feixiaochun"}
    update = {"$set": {"project_names": ["Lilou"]}}
    mycol.update(query, update)

    # 查询
    res = mycol.find_one({"name": "feixiaochun"}, {"_id": 0})
    print res