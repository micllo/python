# -*- coding:utf-8 -*-
from Common.com_func import send_mail, send_DD, log
from Config.pro_config import get_host_by_pro
from Tools.mongodb import MongodbUtils
from Config import config as cfg
from Tools.date_helper import get_current_iso_date
from TestBase.verify_interface import AcquireDependField, VerifyInterface
import re, json
from Common.com_func import is_null


def mongo_exception_send_DD(e, msg):
    """
    发现异常时钉钉通知
    :param e:
    :param msg:
    :return:
    """
    title = "[监控]'mongo'操作通知"
    text = "#### WEB自动化测试'mongo'操作错误\n\n****操作方式：" + msg + "****\n\n****错误原因：" + str(e) + "****"
    send_DD(dd_group_id=cfg.DD_MONITOR_GROUP, title=title, text=text, at_phones=cfg.DD_AT_FXC, is_at_all=False)


def test_interface(pro_name):
    """
    【 测 试 接 口 】（根据项目名）
    :param pro_name:
    :return:

    【 测 试 主 流 程 】
    1.获取上线的接口列表
    （1）上线的'依赖接口列表'
    （2）上线的'测试接口列表'
    2.[ 获 取 依 赖 字 段 值 ]
      < 判断 > 是否需要依赖
    （1）若不需要，则 直接进入 [ 验 证 接 口  ]
    （2）若需要，则执行捕获操作，并获取'错误结果列表'
        1）若 错误列表为空 或者 'error:依赖接口不存在'不在错误列表中 -> 更新'依赖接口列表'结果记录
        2）若 错误列表不为空 -> 更新'测试接口列表'结果记录、并停止接口测试标记 -- STOP --
    3.[ 验 证 接 口 ]
    （1）根据返回的'待更新字典'，更新 '测试接口列表' 中的数据
    """

    # 1.获取上线的接口列表
    # （1）上线的'依赖接口列表'（按照依赖等级顺序排列）
    # （2）上线的'测试接口列表'
    with MongodbUtils(ip=cfg.MONGODB_ADDR, database=cfg.MONGODB_DATABASE, collection=pro_name) as pro_db:
        try:
            depend_interface_list = pro_db.find({"case_status": True, "is_depend": True})
            test_interface_list = pro_db.find({"case_status": True, "is_depend": False})
        except Exception as e:
            mongo_exception_send_DD(e=e, msg="获取'" + pro_name + "'项目上线接口列表")
            return "mongo error"

    depend_interface_list = list(depend_interface_list)
    test_interface_list = list(test_interface_list)
    host = get_host_by_pro(pro_name)

    if is_null(test_interface_list):
        return "no online case"

    # 2.[ 获 取 依 赖 字 段 值 ]
    verify_flag = True  # 接口测试标记 True：需要验证、False：不需要验证
    adf = AcquireDependField(host=host, depend_interface_list=depend_interface_list, test_interface_list=test_interface_list)
    if adf.is_need_depend():
        # 执行捕获操作，并获取'错误结果列表'
        depend_interface_result_list, test_interface_list = adf.acquire()
        fail_result_list = [result for result in depend_interface_result_list if "success" not in result]

        # 更新'依赖接口列表'结果记录
        if is_null(fail_result_list) or ("error:依赖接口不存在" not in fail_result_list):
            pass
        # 更新'测试接口列表'结果记录，并停止接口测试标记
        if fail_result_list:
            verify_flag = False



    # 3.[ 验 证 接 口 ]
    if verify_flag:
        print("进入 [ 验 证 接 口 ]")
        for test_interface in test_interface_list:
            result_dict = VerifyInterface(interface_name=test_interface.get("interface_name"),
                                          host=host, interface_url=test_interface.get("interface_url"),
                                          request_method=test_interface.get("request_method"),
                                          request_header=test_interface.get("request_header"),
                                          request_params=test_interface.get("request_params"),
                                          verify_mode=test_interface.get("verify_mode"),
                                          compare_core_field_name_list=test_interface.get("compare_core_field_name_list"),
                                          expect_core_field_value_list=test_interface.get("expect_core_field_value_list"),
                                          expect_field_name_list=test_interface.get("expect_field_name_list"),
                                          depend_interface_list=test_interface.get("depend_interface_list"),
                                          depend_field_name_list=test_interface.get("depend_field_name_list")).verify()
            # 更新用例测试结果
            result_dict["update_time"] = get_current_iso_date()
            pro_db.update({"_id": test_interface["_id"]}, {"$set": result_dict})

    return "done"

if __name__ == "__main__":
    test_interface("pro_demo_1")