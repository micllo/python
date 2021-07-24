# 格式化 输出
a = 2.34567
print(f"总金额：{a:.2f}")
print("\n")


# 整合多个列表中的第一列，形成二维列表
a = [1, 2, 3]
b = ["小明", "小红", "小黄"]
c = [79, 50, 66]
print(list(zip(a, b, c)))
# [(1, '小明', 79), (2, '小红', 50), (3, '小黄', 66)]
print("\n")


# 将 int 数组 转换成 字符串
a = [1, 2, 3, 4]
print(','.join([str(i) for i in a]))
print("\n")


# 更新字典中的 key
a = {"aa": 1, "bb": 2}
# 1
a["cc"] = a.pop("aa")
# 2
# tmp = a["aa"]
# del a["aa"]
# a["cc"] = tmp
print(a)
print("\n")


# 将 列表 元素作为 keys 创建 字典，value赋默认值 0 或 []
a = ["aa", "bb", "cc"]
# 1
b = {}.fromkeys(a, 0)
b = {}.fromkeys(a, [])  # 注意：这里赋值 [] 会有坑（ 该空列表是所有字典元素共用的 ）
b["aa"].append("1")     # 坑 实例
# 2
# b = {key: [] for key in a}  # 解决上述的坑
print(b)
print("\n")


# 按照字典的 key / value 进行排序
d = {"c": "4", "a": "2", "d": "1", "b": "3"}
d_sorted_0 = sorted(d.items(), key=lambda x: x[0])
d_sorted_1 = sorted(d.items(), key=lambda x: x[1])
print(d_sorted_0)
print(d_sorted_1)


# 按照列表中 每个字典元素的'age'进行排序
test = [{"name": "d", "age": "10"}, {"name": "a", "age": "30"}, {"name": "c", "age": "20"}, {"name": "b", "age": "90"}]
test_age_1 = sorted(test, key=lambda key: key["age"])
test_age_2 = sorted(test, key=lambda key: key["age"], reverse=True)
print(test_age_1)
print(test_age_2)


# 去重、并集、交集、差集、对称差
list1 = [2, 1, 2, 3]
list2 = [3, 4, 5]
set1 = set(list1)  # list去重
set2 = set(list2)
print(set1 | set2)  # 并集
print(set1 & set2)  # 交集
print(set1 ^ set2)  # 对称差（两集合汇总不同元素集）
print(set1 - set2)  # 差集（另一集合中没有的部分）


# 删除列表中重复的元素，并保持原来的排序
test11 = ["b", "c", "d", "b", "c", "a", "a"]
# 方式一
tmp = sorted(set(test11), key=test11.index)
print(tmp)
# 方式二
tmp_list = []
for i in test11:
    if i not in tmp_list:
        tmp_list.append(i)
print(tmp)












