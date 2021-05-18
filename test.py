import re

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

    # 可变类型：List
    # 解释：变动时只在原地址上的对内容进行修改，变动后仍然引用的是同一个内存地址
    a = [1, 2, 3]
    b = a
    print(a, b)
    print(id(a), id(b))
    a[2] = 4
    print(a, b)
    print(id(a), id(b))

    print("\n===================\n")

    # 不可变类型：元祖、字符串、数字、布尔值
    # 解释：变动时会生成新的内存地址，变动后会变成不同的内存地址
    c = (1, 2, 3)
    d = c
    print(c, d)
    print(id(c), id(d))
    print()
    c = c[:2]
    print(c, d)
    print(id(c), id(d))




