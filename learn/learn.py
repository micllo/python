# coding:UTF-8
import time
import sys


if __name__ == '__main__':

    # list = sys.path
    # for i in list:
    #     print i


    """
     【 多维list排序 】
      lambda：匿名函数，可快速创建简单的临时方法
    """

    # reverse=True 降序排列
    list = ["2018.10.01 19:53:37", "2018.10.02 10:50:30", "2018.10.02 09:00:00"]
    list.sort(reverse=True)
    print(list)

    # 按照第二维list的 第二个字段进行排序
    list2 = [["aaa", "2018.10.01 19:53:37"], ["bbb", "2018.10.02 10:50:30"], ["ccc", "2018.10.02 09:00:00"]]
    list2.sort(key=lambda x: x[1], reverse=True)
    print(list2)

    # 按照第二维list的 第二个list中的第二个字段进行排序
    list3 = [[["aaa", "2018.10.01 19:53:37"], ["aaa", "2018.10.01 18:53:37"]], [["bbb", "2018.10.02 10:50:30"], ["bbb", "2018.10.02 10:40:00"]], [["ccc", "2018.10.02 09:00:00"], ["ccc", "2018.10.02 08:00:00"]]]
    list3.sort(key=lambda x: x[1][1], reverse=True)
    print(list3)

    # 按照第二维list的 第一个list中的第二个字段进行排序
    list4 = [[["aaa", "2018.10.01 19:53:37"], ["aaa", "2018.10.01 18:53:37"]], [["bbb", "2018.10.02 10:50:30"], ["bbb", "2018.10.02 07:40:00"]], [["ccc", "2018.10.02 09:00:00"], ["ccc", "2018.10.02 08:00:00"]]]
    list4.sort(key=lambda x: x[0][1], reverse=True)
    print(list4)


    """
     【 将时间格式转换成时间戳 】
    """
    str1 = "2018.10.01 19:53:37"
    timeArray = time.strptime(str1, "%Y.%m.%d %H:%M:%S")
    print(timeArray)
    timeStamp = int(time.mktime(timeArray))
    print(timeStamp)
