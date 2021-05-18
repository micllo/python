"""
求两数之和等于13的下标
"""
test = [2, 6, 7, 11, 15]
target = 13
# 方法一：两层循环
# for index, value in enumerate(test):
#     for i in range(index+1, len(test)):
#         if value + test[i] == target:
#             print(index, i)

# 方法二：一层循环, 使用字典
test_dict = {}  # key=数字，value=下标
for index, value in enumerate(test):
    test_dict[value] = index
    if test_dict.get(target-value) is not None:
        print(test_dict.get(target-value), index)


"""
有效的字母异位词
https://leetcode-cn.com/problems/valid-anagram/
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


