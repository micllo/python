import random, time
from functools import reduce


def maopao():
    """
    冒泡排序
    """
    maopao = [3, 5, 2, -2, 6, 9, 1]


def two_num_add():
    """
    将列表中两数之和等于13的元素取出来
    方法一：两层循环
    方法二：一层循环
    """
    test = [0, 2, 6, 7, 11, 15, 13]
    target = 13


def find_with_two():
    """
    二分查找（通过给定的数字，找出对应的下标）
    """
    find = 9
    test = [-2, 1, 2, 3, 5, 6, 9]


def valid_word():
    """
    有效的字母异位词：给定两个字符串，若它们字母都相同但是顺序不同，则视为字母异位词
    网址：https://leetcode-cn.com/problems/valid-anagram/
    """
    a = "anagram"
    b = "nagaram"


def prime_number():
    """
     求100以内的质数：除了1和自身以外不能被其他自然数整除的大于1的自然数
    """



def nine_x_nine():
    """
    打印 9x9乘法表
    """


def show_even_numbers():
    """
    显示 偶数（一行代码）
    :return:
    """


def show_sxhs():
    """
    求1000以内的水仙花数
        eg: 1^3 + 5^3 + 3^3 = 153
    """



def remove_duplication():
    """
    列表去重（三种方式）
    """
    a = [1, 2, 3, 2, 5, 1, 6]



def subject_33():
    """
        33.统计列表中每个元素出现的个数
    :return:
    """
    a = [1, 3, 4, 1, 3, 5, 7, 4, 1]
    a_dict = {}.fromkeys(a, 0)
    for i in a_dict.keys():
        a_dict[i] = a.count(i)
    print(a_dict)



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
        5  Nike       699

    """
    products = [["iphone", 6888], ["MacPro", 14800], ["小米6", 2499], ["Coffee", 31], ["Book", 60], ["Nike", 699]]
    print("------  商品列表 ------")
    for i in range(0, len(products)):
        print(f"{i}\t{products[i][0]}\t{str(products[i][1])}")



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
        for key, value in i_dict.items():
            i_dict[key] = ",".join(map(lambda x: str(x), list(value.values())))
    print(a)


def subject_45():
    """
        45.算出平均分（一行代码）、再找出学霸（一行代码）、显示学霸姓名排行榜（一行代码）
    """
    data = {
            'ZhaoLiYing': 60,
            'FengShaoFeng': 75,
            'ZhangLaoShi': 99,
            'LiuLaoShi': 100,
            'TangYan': 88,
            'LuoJin': 35,
        }
    print(f"平均分：{sum(data.values())/len(data.values()):.2f}")

    print(f"学霸：{sorted(data.items(), key=lambda x: x[1], reverse=True)[0][0]}")
    print(f"学霸排行：{list(map(lambda x: x[0], sorted(data.items(), key=lambda x: x[1], reverse=True)))}")

    print(f"学霸：{[key for key,value in data.items() if value == max(data.values())][0]}")
    print(f"学霸排行：{[i[0] for i in sorted(data.items(), key=lambda x:x[1], reverse=True)]}")

    print(f"学霸：{list(map(lambda k,v: v==max(data.values()), data.items()))}")


def subject_49():
    """
        49. 模拟一个bug查询接口功能：
            用户输入9，返回9月 bug共60个
    """
    data = {"business_Fans_J": [{"2016_08": 14}, {"2016_09": 15}, {"2016_10": 9}],
             "AX": [{"2016_08": 7}, {"2016_09": 32}, {"2016_10": 0}],
             "AX_admin": [{"2016_08": 5}, {"2016_09": 13}, {"2016_10": 2}]
            }

    m = input("请输入月份: ")
    if m.isdigit():
        if int(m) in range(1, 13):
            bug = 0
            m_str = len(m) == 1 and "2016_0" + str(m) or "2016_" + str(m)
            for value_list in data.values():
                for m_dict in value_list:
                    bug += m_dict.get(m_str, 0)
            print(bug)
        else:
            print("无效月份！！！")
    else:
        print("请输入数字！！！")


def senior_func_map():
    """
    map() 用法
        函数接收两个参数，一个是函数，一个是序列
        将传入的函数依次作用到序列的每个元素，并把结果作为新的list返回
    """
    # 求列表的平方数值
    a = [2, 1, 4, 3]
    print(list(map(lambda x: x**2, a)))

    # 针对列表中每个元素长度值，进行排序
    b = ['Python5', 'Java6', 'C2', 'PHP1', 'Ruby4', 'Go3', 'JavaScript7']
    print(sorted(b, key=lambda x: len(x), reverse=True))
    print(list(map(lambda x: len(x), sorted(b, key=lambda x: len(x), reverse=True))))
    print(list(map(len, b)))

    # 一行代码 实现 首字母大写、其余小写
    c = ["adam", "LISA", "barT"]
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
    test = [1, 3, 5, 7, 9]
    print(reduce(lambda x, y: x * 10 + y, test))


def subject_79():
    """
        将 "2017-10-10 23:40:00" 改成 "2017/10/10 11:40:00 PM"
    """
    time_str = "2017-10-10 23:40:00"
    time_tuple = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    time_str2 = time.strftime("%Y/%m/%d %I:%M:%S %p", time_tuple)
    print(time_str2)


def subject_80():
    """
        打印出 三天前的时间，格式：年-月-日_小时:分钟:秒数
    """
    time_stamp = time.time() - 3*24*60*60
    time_tuple = time.localtime(time_stamp)
    time_str = time.strftime("%Y年-%m月-%d日_%H小时:%M分钟:%S秒数", time_tuple)
    print(time_str)


def subject_81():
    """
        编写一个方法，接受参数为一个列表：[2017, 01, 15] (不考虑1970.1.1之前的时间点)。
        随机输出2017.1.15日 00:00:00 之前的一个时间点，格式为：2017-01-01_13:59:06
         random.randint(a,b)	返回整数a和b范围内数字
    """
    time_list = [2017, 1, 15]
    time_str = "-".join(map(lambda x: str(x), time_list)) + "_00:00:00"
    time_tuple1 = time.strptime(time_str, "%Y-%m-%d_%H:%M:%S")
    time_stamp = time.mktime(time_tuple1)
    need_stamp = time_stamp - random.randint(1, int(time_stamp))
    time_tuple2 = time.localtime(need_stamp)
    time_str2 = time.strftime("%Y-%m-%d_%H:%M:%S", time_tuple2)
    print(time_str2)


def subject_82():
    """
        根据传入的美式时间字符串 13:28:06_12/21/2018
        生成标准时间字符串 2018-12-21_13:28:06
    """
    time = "13:28:06_12/21/2018"
    time_list = time.split("_")
    hms_str = time_list[0]
    ymd_list = time_list[1].split("/")
    ymd_list.insert(0, ymd_list.pop())
    ymd_str = "-".join(ymd_list)
    print(ymd_str + "_" + hms_str)


def subject_44():
    """
        将1-25的数字打乱顺序填入5*5个小方格的表里面（ 一次循环 ）
        random.shuffle(list)   给指定的列表进行原地随机移位
    """
    num_list = list(range(1, 26))
    random.shuffle(num_list)
    for i in range(0, len(num_list)):
        if i % 5 == 0 and i > 0:
            print()
        print(num_list[i], end="\t")



if __name__ == '__main__':
    # maopao()
    # two_num_add()
    # find_with_two()
    # valid_word()
    # prime_number()
    # nine_x_nine()
    # show_even_numbers()
    # show_sxhs()
    # remove_duplication()

    # subject_33()
    # subject_34()
    # subject_50()
    subject_45()
    # subject_49()

    # senior_func_map()
    # senior_func_filter()
    # senior_func_reduce()

    # subject_79()
    # subject_80()
    # subject_81()
    # subject_82()
    # subject_44()


