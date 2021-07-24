import math


def maopao():
    """
    冒泡排序
       外层循环次数：数组长度少一次（因为本身不需要比较）
       内层循环次数：索引开始位置 保持第一位 不变
                   索引结束位置 最长为数组下标的倒数第二位（然后依次往前递减）
       内部逻辑：使用内循环下标 进行相邻的两数的比较
    :return:
    """
    maopao = [3, 5, 2, -2, 6, 9, 1]
    for i in range(len(maopao) - 1):
        for j in range(len(maopao) - 1 - i):
            if maopao[j] > maopao[j+1]:
                maopao[j], maopao[j+1] = maopao[j+1], maopao[j]
    print(maopao)


def two_num_add():
    """
    将列表中两数之和等于13的元素取出来

    方法一：两层循环
          外层循环：遍历整个列表（ 最后一位元素不需要遍历，因为没有后续的元素需要和它匹配了 ）
          内层循环：索引开始位置 从第二位起不断往后移  （依次往后递减）
                 索引结束位置 保持在列表最后一位不变
    方法二：一层循环
          遍历数组的同时，将当前元素值和下标存入字典中 key=元素值，value=下标
          同时调用字典的get()方法获取 该字典中已经存在且匹配的key，若能获取到则说明匹配成功了
    """
    test = [0, 2, 6, 7, 11, 15, 13]
    target = 13
    need = {}
    # 方法一：两层循环
    for index, value in enumerate(test):
        for i in range(index + 1, len(test)):  # 注：range(1,9) 最后一位是取不到的
            if value + test[i] == target:
                need[value] = test[i]
    print(need)

    # 方法二：一层循环
    tmp_dict = {}
    for index, value in enumerate(test):
        tmp_dict[value] = index
        if tmp_dict.get(target-value) is not None:
            need[value] = target-value
    print(need)


def find_with_two():
    """
    二分查找（通过给定的数字，找出对应的下标）
    :return:
    """
    find = 9
    test = [-2, 1, 2, 3, 5, 6, 9]
    start_i = 0
    end_i = len(test) - 1
    m_i = int((start_i + end_i) / 2)
    while start_i <= end_i:
        if find > test[m_i]:
            start_i = m_i + 1;
        elif find < test[m_i]:
            end_i = m_i - 1;
        else:
            find_i = m_i
            break;
        m_i = int((start_i + end_i) / 2)
    print(find_i)


def valid_word():
    """
    有效的字母异位词：给定两个字符串，若它们字母都相同但是顺序不同，则视为字母异位词
    网址：https://leetcode-cn.com/problems/valid-anagram/
    思路：判断 不同字母 和 其出现的次数 是否都一致
         将遍历的字符作为key保存入字典，将统计的数量作为value
    """
    a = "anagram"
    b = "nagaram"
    a_dict = {}
    b_dict = {}
    for i in a:
        a_dict[i] = a_dict.get(i, 0) + 1
    for i in b:
        b_dict[i] = b_dict.get(i, 0) + 1
    print(a_dict)
    print(b_dict)
    if a_dict == b_dict:
        print("相同")


def prime_number():
    """
     求100以内的质数：除了1和自身以外不能被其他自然数整除的大于1的自然数
        外层循环：遍历2~99的自然数
        内层循环：遍历从1~其自身之间的自然数
        判断 内层循环的自然数是否都不能被整除
    """
    prime_num_list = []
    for i in range(2, 100):
        for j in range(2, i):
            if i % j == 0:
                break
        else:  # 当正常循环完所有次数后，才会执行 else 语句
            prime_num_list.append(i)
    print(prime_num_list)


def nine_x_nine():
    """
    打印 9x9乘法表
        外层循环次数：1 ~ 9，共9次
        内层循环测试：索引开始位置：1 固定不变
       （每行的显示） 索引结束位置：从开始位置1不断增加，直到9
    :return:
    """

    for i in range(1, 10):
        for j in range(1, i+1):
            print(f"{j} x {i} = {j*i}  ", end="")
        print("")


def show_even_numbers():
    """
    显示 偶数
    :return:
    """
    # 方法一：
    show = []
    for i in range(0, 10):
        if i % 2 == 0:
            show.append(i)
    print(show)

    # 方法二：
    print([i for i in range(0, 10, 2)])


def show_sxhs():
    """
    求1000以内的水仙花数
        eg: 1^3 + 5^3 + 3^3 = 153
    :return:
    """
    for i in range(1, 1000):
        gw = i % 10             # 取模 - 返回除法的余数
        sw = i % 100 // 10    # 先取整除，再取整数
        bw = i // 100           # 取整除 - 返回商的整数部分
        if gw**3 + sw**3 + bw**3 == i:
            print(i)


def remove_duplication():
    """
    列表去重
    :return:
    """
    a = [1, 2, 3, 2, 5, 1, 6]

    # 1
    b = []
    for i in range(0, len(a)):
        if a[i] not in b:
            b.append(a[i])
    print(b)

    # 2
    print(list(set(a)))

    # 3
    print(list({}.fromkeys(a).keys()))


if __name__ == '__main__':
    # maopao()
    # two_num_add()
    # find_with_two()
    # valid_word()
    # prime_number()
    # nine_x_nine()
    # show_even_numbers()
    # show_sxhs()
    remove_duplication()


