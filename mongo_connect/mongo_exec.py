# coding:UTF-8
import pymongo
import pandas as pd
import numpy as np

if __name__ == '__main__':

    """
      【 参 考 资 料 】
       http://www.runoob.com/python3/python-mongodb.html
    """

    # 创建mongo连接
    # myclient = pymongo.MongoClient('mongodb://localhost:27017/')  # monitor_lilou [local]
    myclient = pymongo.MongoClient('mongodb://192.168.25.202:25017/')  # monitor_lilou [uat]
    # myclient = pymongo.MongoClient('mongodb://10.76.88.75:27101/')  # monitor_lilou [wuxi]

    # # 连接 数据库
    # mydb = myclient['platform_config']
    #
    # # 获取指定数据库中的文档列表
    # collist = mydb.collection_names()
    # print collist
    # if "monitor_func" in collist:
    #     print("集合已存在！")
    # else:
    #     print "集合不存在"
    #
    # # 指定文档名
    # mycol = mydb['monitor_func']

    # # 为文档添加内容
    # env_id = u"uat_basic_ac"
    # database_id = u"sin_uat_ac"
    # st = u"2018-10-25 23:50:00"
    # et = u"2018-10-25 23:50:01"
    #
    # std_status = u"success"
    # var_status = u"success"
    # model_status = u"success"
    # acrm_status = u"success"
    # status = u"success"
    #
    # start_module = u"Strawberry"
    # end_module = u'FruitSalad'
    # interface_func = u"True"
    # extend = u"False"
    # specify_file = u"False"
    # rerun_func = u"union"
    #
    # rerun_condition = {"env_id": env_id, "database_id": database_id, "st": st, "et": et,
    #                    "std_status": std_status, "var_status": var_status, "model_status": model_status, "acrm_status": acrm_status, "status": status,
    #                    "start_module": start_module, "end_module": end_module, "interface_func": interface_func, "extend": extend, "specify_file": specify_file, "rerun_func": rerun_func}
    # mydict = {"func_nm": "rerun", "task_cnt": 100, "status": "success", "ct": 1542878249149, "ut": 1542878249149, "done_cnt": 0, "progress_percent": 0, "rerun_condition": rerun_condition}
    # res = mycol.insert_one(mydict)
    # print res

    # 修改文档内容
    # query = {"func_nm": "rerun"}
    # update = {"$set": {"rerun_condition": rerun_condition}}
    # mycol.update_one(query, update)

    # # 查询文档内容
    # query = {"func_nm": "rerun"}
    # res = mycol.find_one(query, {"_id": 0})
    # print res
    # rerun_condition = res.get("rerun_condition")
    # print rerun_condition.get("st")

    ##############################################################################
    ##############################################################################

    # # 连接 数据库
    # mydb = myclient['platform_config']
    #
    # # 获取指定数据库中的文档列表
    # collist = mydb.collection_names()
    # print collist
    # if "switch_env" in collist:
    #     print("集合已存在！")
    # else:
    #     print "集合不存在"
    #
    # # 指定文档名
    # mycol = mydb['switch_env']
    #
    # # 为文档添加内容
    # mydict1 = {"client_ip": "1.1.1.1", "pro_nm": u"葫芦数据", "pro_id": "hulu_op", "current_env": "A", "ct": 1545189689000, "ut": 1545189689000}
    # mydict2 = {"client_ip": "2.2.2.2", "pro_nm": u"索伦项目", "pro_id": "sauron", "current_env": "A", "ct": 1545189689000, "ut": 1545189689000}
    # mydict3 = {"client_ip": "3.3.3.3", "pro_nm": u"解析项目", "pro_id": "cornucopia", "current_env": "A", "ct": 1545189689000, "ut": 1545189689000}
    # res = mycol.insert_one(mydict1)
    # res = mycol.insert_one(mydict2)
    # res = mycol.insert_one(mydict3)
    #
    # # 查询文档内容
    # query = {"pro_id": "hulu_op"}
    # res = mycol.find_one(query, {"_id": 0})
    # print res
    # print res.get("current_env")
    #

    ##############################################################################
    ##############################################################################

    # # 连接 数据库
    # mydb = myclient['platform_config']
    # # 指定文档名称
    # mycol = mydb['project_config']
    # rabbit_cur = mycol.find({"rabbit_monitor": "open"}, {"_id": 0, "rabuser": 1, "rab_ip": 1, "rabpassword": 1, "env_id": 1, "project_id": 1, "email": 1})
    # rabbit_list = [each_one for each_one in rabbit_cur]
    # print rabbit_list
    # rabbit_df = pd.DataFrame(rabbit_list)
    # print rabbit_df
    # print "\n"
    # # 对特定列去重复，还原索引
    # rabbit_mq_df = rabbit_df.drop_duplicates("rab_ip").reset_index(drop=True)
    # print rabbit_mq_df

    ##############################################################################
    ##############################################################################

    # # 在 platform_config > project_config 表中新增一列字段 uwsgi_monitor 并默认赋值为 open
    # # 连接 数据库
    # mydb = myclient['platform_config']
    # # 指定文档名称
    # mycol = mydb['project_config']
    # # 修改文档内容
    # update = {"$set": {"uwsgi_monitor": "close"}}
    # mycol.update({}, update, multi=True)

    ##############################################################################
    ##############################################################################

    # # 在 platform_config > project_config 表中新增一列字段 port 并默认赋值为 80
    # # 连接 数据库
    # mydb = myclient['platform_config']
    # # 指定文档名称
    # mycol = mydb['project_config']
    # # 修改文档内容
    # update = {"$set": {"port": "80"}}
    # mycol.update({}, update, multi=True)

    ##############################################################################
    ##############################################################################

    # # aggregate ：管 道 符
    # # 连接 数据库
    # mydb = myclient['variable']
    # # 指定文档名称
    # mycol = mydb['app_mark_type']
    # app_nm_summary = mycol.aggregate([{"$group": {"_id": "$type", "total_cnt": {"$sum": 1}}}])
    # for each in app_nm_summary:
    #     print each

    # with MongodbUtils(ip=config.DB_PROJECT_SETTING_IP, port=config.DB_PROJECT_SETTING_PORT,
    #                   database=config.DB_PROJECT_SETTING_DATABASE,
    #                   collection=config.DB_PROJECT_SETTING_COLLECTION) as project_db:
    #
    #     agg_pattern = [
    #         {"$group": {"_id": {"project_env": "$project_env"}, "project_name": {"$push": "$project_name"}}},
    #         {"$sort": {"create_time": 1}}
    #     ]
    #
    #     sidebar_projects = project_db.aggregate(agg_pattern)