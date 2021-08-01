import subprocess
import sys
import jsonpath

"""
    通过 sys.path.append() 配置环境变量
"""
# sys.path.append("/Users/micllo/Documents/tools/apache-maven-3.2.5")
# subprocess.call("mvn -v", shell=True)


"""
   【 执行 cmd 命令 】
    Popen()、 call()、check_output() 区别：
    
    Popen(): 异步执行, 返回 subprocess.Popen 对象
    call():  同步执行(阻塞)，返回结果代码(0表示执行成功)，< 执行内容默认输出stdout >
    check_output(): 同步执行(阻塞)，返回执行结果（bytes类型）
"""

# subprocess.Popen("sleep 5", shell=True)
# res = subprocess.Popen("ls -la", shell=True)
# print("----")
# print(res)

# subprocess.call("sleep 5", shell=True)
# res_code = subprocess.call("pwd", shell=True)
# print(res_code)


# subprocess.check_output(["sleep", "5"])
# bytes_res = subprocess.check_output(["ls", "-la"])
# print(bytes_res)
# print(type(bytes_res))


"""
    将实例方法通过装饰器变成可以向调用属性的方式
    
   【 注 意 】
      def __init__(self, k_v=None): 
      坑：这里不能写成 k_v={} 默认空字典，否则每个实例对象都会使用同一个字典 
"""


# class Test(object):
#
#     def __init__(self, k_v=None):
#         self.k_v = k_v
#         self.__result = {}
#
#     @property
#     def result(self):
#         return self.__result
#
#
# t = Test()
# t.result["aa"] = 123
# print(t.result)


"""
    JSONPath 表达式
    https://www.cnblogs.com/jpfss/p/10973590.html
"""

data = {"error_code": 200,
        "event_list": [
            {"id": 1, "title": "标题1"},
            {"id": 2, "title": "标题2"},
            {"id": 3, "title": "标题3"},
            {"error_code": 502}
          ]
        }

print(jsonpath.jsonpath(data, '$.error_code'))
print(jsonpath.jsonpath(data, '$..error_code'))  # 递归查询所有key=error_code对应的值
print(jsonpath.jsonpath(data, '$.event_list[1].title'))
print(jsonpath.jsonpath(data, '$..title'))
print()


"""
    JSONPath 表达式 封装
"""


def json_path_value(data_dict, json_path, is_recur=False, index=None):
    """
      获取json字典中对应的值
    :param data_dict:  数据字典
    :param json_path:  json路径
    :param is_recur:   是否递归查找所有对应的值
    :param index:      指定返回多个value中的第几个

        【 举 例 】
            is_recur=False, index=None ：返回找到第一个值
            is_recur=True, index=None  ：返回递归查询到的值列表
            is_recur=True, index=2     ：返回递归查询到的第2个值
    :return:
    """
    json_path = is_recur and "$.." + json_path or "$." + json_path
    result = jsonpath.jsonpath(data_dict, json_path)
    if result:
        if not is_recur:
            return result[0]
        else:
            try:
                return index and result[index] or result
            except IndexError:
                return f"指定查询的索引'{index}'超出了范围"
    else:
        return 'json字段取值失败：{json_path}'.format(json_path=json_path)


# print(json_path_value(data, "error_code"))
# print(json_path_value(data, "error_code", is_recur=True))
# print(json_path_value(data, "error_code", is_recur=True, index=1))
# print(json_path_value(data, "error_code", is_recur=True, index=2))
# print(json_path_value(data, "event_list[1].title"))
# print(json_path_value(data, "title", is_recur=True))
#
