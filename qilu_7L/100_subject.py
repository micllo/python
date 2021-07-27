import time, random

def subject_33():
    """
        33.统计列表中每个元素出现的个数

        {}.fromkeys(seq, val=None)
           -> 创建并返回一个新字典，
              参数1：已序列中的元素创建key（自动去重）
              参数2：创建value 默认赋值
    :return:
    """
    # 1
    a = [1, 3, 4, 1, 3, 5, 7, 4, 1]
    tmp = list(set(a))
    res = {}
    for i in tmp:
        res[i] = a.count(i)
    print(res)

    # 2
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
    a = [2, 1, 4, 3]
    # 求列表的平方数值
    print([i**2 for i in a])
    print(list(map(lambda i: i**2, a)))

    # 针对列表中每个元素长度值，进行排序
    b = ['Python5', 'Java6', 'C2', 'PHP1', 'Ruby4', 'Go3', 'JavaScript7']
    print(sorted(b, key=lambda x: len(x), reverse=True))
    print(list(map(lambda x: len(x), sorted(b, key=lambda x: len(x), reverse=True))))
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


def subject_79():
    """
        将 "2017-10-10 23:40:00" 改成 "2017/10/10 11:40:00 PM"
    """
    time_str = "2017-10-10 23:40:00"
    time_tuple = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    print(time_tuple)
    time_str2 = time.strftime("%Y/%m/%d %I:%M:%S %p", time_tuple)
    print(time_str2)


def subject_80():
    """
        打印出 三天前的时间，格式：年-月-日_小时:分钟:秒数
    """
    time_stamp = time.time() - 3*24*60*60
    time_tuple = time.localtime(time_stamp)
    print(time_tuple)
    time_str = time.strftime("%Y年%m月%d日_%H小时:%M分钟:%S秒数", time_tuple)
    print(time_str)


def subject_81():
    """
        编写一个方法，接受参数为一个列表：[2017, 01, 15] (不考虑1970.1.1之前的时间点)。
        随机输出2017.1.15日 00:00:00 之前的一个时间点，格式为：2017-01-01_13:59:06

        思路：1.将列表转换成时间字符串
             2.将时间字符串 转换成 时间戳（中间需要 元祖时间 过度）
             3.时间戳 随机减去 一个数字
             4.将时间戳 转换成 时间字符串（中间需要 元祖时间 过度）

        random.randint(a,b)	返回整数a和b范围内数字
    """
    time_list = [2017, 1, 15]
    time_str = f"{time_list[0]}-{time_list[1]}-{time_list[2]}_00:00:00"
    str_to_tuple = time.strptime(time_str, "%Y-%m-%d_%H:%M:%S")
    tuple_to_stamp = time.mktime(str_to_tuple)
    need_stamp = tuple_to_stamp - random.randint(1, tuple_to_stamp)
    stamp_to_tuple = time.localtime(need_stamp)
    tumple_to_str = time.strftime("%Y-%m-%d_%H:%M:%S", stamp_to_tuple)
    print(tumple_to_str)


def subject_82():
    """
        根据传入的美式时间字符串 13:28:06_12/21/2018
        生成标准时间字符串 2018-12-21_13:28:06
    """
    time_str = "13:28:06_12/21/2018"
    time_list = time_str.split("_")
    hms = time_list[0]
    ymd = time_list[1]
    ymd_list = ymd.split("/")
    ymd_list.insert(0, ymd_list.pop())  # 将列表最后一位 放入第一位
    ymd_str = "-".join(ymd_list)
    print(f"{ymd_str}_{hms}")


def subject_44():
    """
        将1-25的数字打乱顺序填入5*5个小方格的表里面（ 一次循环 ）
        random.shuffle(list)   给指定的列表进行原地随机移位
    """
    num_list = [i for i in range(1, 26)]
    random.shuffle(num_list)  # 给指定的列表进行原地随机移位
    for i in range(0, len(num_list)):
        if i % 5 == 0 and i > 0:
            print()
        print(num_list[i], end="\t")


def subject_40():
    """
        统计一篇英文文章每个单词的出现频率，并返回出现频率最高的前5个单词及其出现次数(字典形式)
    """
    content = "A small sample of texts from Project Gutenberg appears in the NLTK corpus collection. However, you may be interested in analyzing other texts from Project Gutenberg. You can browse the catalog of 25,000 free online books at http://www.gutenberg.org/catalog/, and obtain a URL to an ASCII text file. Although 90% of the texts in Project Gutenberg are in English, it includes material in over 50 other languages, including Catalan, Chinese, Dutch, Finnish, French, German, Italian"
    content_list = content.split(" ")
    word_list = []
    word_num_dict = {}
    for i in content_list:
        if i.isalpha() or (i[:-1].isalpha() and i[-1] in [".", ","]):
            i = i.replace(".", "")
            i = i.replace(",", "")
            word_list.append(i.lower())

    # 计数1：列表先去重
    # for i in list(set(word_list)):
    #     word_num_dict[i] = word_list.count(i)

    # 计数2：列表不用去重
    for i in word_list:
        word_num_dict[i] = word_num_dict.get(i, 0) + 1

    print(sorted(word_num_dict.items(), key=lambda x: x[1], reverse=True)[:5])


def subject_42():
    """
        要求：address=beijing&limit=200&title=XiaoMi_Test&time=2018-01-30&username=liulaoshi
        结果：token=123456title=XiaoMi_Test&time=2018-01-30&limit=200&address=beijing
            1.去除username参数
            2.剩余参数按照参数名的ASCII码降序排列
            3.最前面拼接字符串token=123456
    """
    params = "address=beijing&limit=200&title=XiaoMi_Test&time=2018-01-30&username=liulaoshi"
    params_list = params.split("&")

    for i in range(0, len(params_list)):
        if params_list[i].startswith("username"):
            params_list.pop(i)
    params_list.sort(reverse=True)
    params_list = "token=123456" + "&".join(params_list)
    print(params_list)



if __name__ == "__main__":

    # subject_33()
    # subject_34()
    # subject_50()
    # subject_45()
    # subject_49()

    # senior_func_map()
    # senior_func_filter()
    # senior_func_reduce()

    # subject_79()
    # subject_80()
    # subject_81()
    # subject_82()
    # subject_44()
    subject_40()
    # subject_42()



