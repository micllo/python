
def subject_33():
    """
        33.统计列表中每个元素出现的个数
    :return:
    """
    a = [1, 3, 4, 1, 3, 5, 7, 4, 1]
    tmp = list(set(a))
    res = {}
    for i in tmp:
        res[i] = a.count(i)
    print(res)


def subject_34():
    """
      34.现有商品列表如下：
        products = [["iphone",6888],["MacPro",14800],["小米6",2499],["Coffee",31],["Book",60],["Nike",699]]

        需打印出以下格式：

        ------  商品列表 ------
        0  iphone     6888
        1  MacPro    14800
        2  小米6     2499
        3  Coffee      31
        4  Book       60
        5	 Nike       699

    """
    products = [["iphone", 6888], ["MacPro", 14800], ["小米6", 2499], ["Coffee", 31], ["Book", 60], ["Nike", 699]]
    print("------  商品列表 ------")
    for index, value in enumerate(products):
        print(f"{index} {value[0]} {value[1]}")


def subject_50():
    """
    50. 请将原始报文内容：
            [{"from": {"x": 39.123, "y": 40.234}, "to": {"x": 78.567, "y": 89.789}}]
        修改格式为：
            [{"from": "39.123,40.234", "to": "78.567,89.789"}]
    :return:
    """
    a = [{"from": {"x": 11.111, "y": 22.222}, "to": {"x": 33.333, "y": 44.444}},
         {"from": {"x": 55.555, "y": 66.666}, "to": {"x": 77.777, "y": 88.888}}]

    for i_dict in a:
        for key, value_dict in i_dict.items():
            i_dict[key] = ",".join([str(i) for i in value_dict.values()])
    print(a)


def subject_45():
    """
        45.算出平均分、再找出学霸（一行代码）、显示学霸姓名排行榜（一行代码）
    """
    data = {
            'ZhaoLiYing': 60,
            'FengShaoFeng': 75,
            'ZhangLaoShi': 99,
            'LiuLaoShi': 100,
            'TangYan': 88,
            'LuoJin': 35,
        }
    score_list = data.values()
    avg = sum(score_list) / len(score_list)
    print(f"平均分：{avg:.2f}")
    print(f"学霸：{sorted(data.items(), key=lambda x: x[1], reverse=True)[0][0]}")
    print(f"学霸排行榜：{list(map(lambda x: x[0], sorted(data.items(), key=lambda x: x[1], reverse=True)))}")


def subject_49():
    """
        49. 模拟一个bug查询接口功能：
            用户输入9，返回9月 bug共60个
    """
    data = {"business_Fans_J": [{"2016_08": 14}, {"2016_09": 15}, {"2016_10": 9}],
             "AX": [{"2016_08": 7}, {"2016_09": 32}, {"2016_10": 0}],
             "AX_admin": [{"2016_08": 5}, {"2016_09": 13}, {"2016_10": 2}]
            }
    month = input("请输入月份：")
    if month.isdigit():
        if len(month) == 1:
            month = "0" + month
        bug_num = 0
        for month_list in data.values():
            for month_dict in month_list:
                if month in list(month_dict.keys())[0]:
                    bug_num += list(month_dict.values())[0]
        print(bug_num)
    else:
        print("请输入数字！！！")


def senior_func_map():
    """
    map() 用法
        函数接收两个参数，一个是函数，一个是序列
        将传入的函数依次作用到序列的每个元素，并把结果作为新的list返回
    """
    a = [2, 1, 4, 3]
    # 求列表的平方数值
    print([i**2 for i in a])
    print(list(map(lambda i: i**2, a)))

    # 针对列表中每个元素长度，进行排序
    b = ['Python5', 'Java6', 'C2', 'PHP1', 'Ruby4', 'Go3', 'JavaScript7']
    print(list(map(len, b)))

    # 一行代码 实现 首字母大写、其余小写
    c = ["adam", "LISA", "barT"]
    print(list(map(lambda x: x.title(), c)))
    print(list(map(lambda x: x[0].upper() + x[1:].lower(), c)))


def senior_func_filter():
    """
    filter() 过滤函数
        接收一个布尔值返回值的函数和一个序列
        把传入的函数依次作用于每个元素，根据返回值是True还是False决定保留还是丢弃该元素
    """
    # 过滤列表中的小写字母
    a = ["aaa", "AAA", "bbb", "BBB"]
    print(list(filter(lambda x: x.islower(), a)))

    # 将爱好为“无”的数据剔除掉 ["姓名","年龄","爱好"]
    data = [["liulaoshi", "18", "学习"], ["tom", 25, "无"], ["hanmeimei", 26, "花钱"]]
    print(list(filter(lambda x: x[2] != "无", data)))


def senior_func_reduce():
    """
    reduce() 函数
        把一个函数作用在一个序列上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算
        reduce(f, [x1, x2, x3, x4]) = f(f(f(x1, x2), x3), x4)
    """
    # 把序列 [1, 3, 5, 7, 9] 转换成 13579
    a = [1, 3, 5, 7, 9]
    from functools import reduce
    print(reduce(lambda x, y: x*10+y, a))


class stack():

    def __init__(self):




if __name__ == "__main__":
    subject_34()
    # subject_33()
    # subject_50()
    # subject_45()
    # subject_49()

    # senior_func_map()
    # senior_func_filter()
    # senior_func_reduce()







