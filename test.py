import re
import copy
import json

# a = 'A234567890'
# if re.match(r'[a-zA-Z\_][0-9a-zA-Z\_]{1,2}', a):
#     print('OK')
# else:
#     print('Failed')
#
# res = re.match(r'[a-zA-Z\_][0-9a-zA-Z\_]{1,2}', a)
# print(res)
# print(res.group(0))
# # print(res.group(1))

class abc(object):

    def abc_one(self):
        print("dddddd")


"""
冒泡排序
"""
def bubble_sort(nums):
    for i in range(len(nums) - 1):  # 这个循环负责设置冒泡排序进行的次数
        for j in range(len(nums) - i - 1):  # j为列表下标
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums


if __name__ == '__main__':
    test = "?name=messi&age=33"
    print(test.json())


