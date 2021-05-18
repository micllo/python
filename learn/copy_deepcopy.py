import copy

# 可变类型：List
# 解释：变动时只在原地址上的对内容进行修改，变动后仍然引用的是同一个内存地址
aa = [1, 2, 3]
bb = aa
print(aa, bb)
print(id(aa), id(bb))
aa[2] = 4
print(aa, bb)
print(id(aa), id(bb))

print("\n-----------------\n")

# 不可变类型：元祖、字符串、数字、布尔值
# 解释：变动时会生成新的内存地址，变动后会变成不同的内存地址
cc = (1, 2, 3)
dd = cc
print(cc, dd)
print(id(cc), id(dd))
print()
cc = cc[:2]
print(cc, dd)
print(id(cc), id(dd))

print("\n======== 深拷贝、浅拷贝 ===========\n")

"""
浅拷贝 对一个复杂对象的子对象并不会完全进行复制
深拷贝 会将一个复杂对象的每一层复制一个单独的个体出来
"""

a = [1, 2, 3]
b = a
a = [4, 5, 6]
print(a)
print(b)
print("")

a = [1, 2, 3]
b = a
a[0], a[1], a[2] = 4, 5, 6
print(a)
print(b)
print("")

a = [1, 2, 3]
b = copy.copy(a)
a[0], a[1], a[2] = 4, 5, 6
print(a)
print(b)
print("")

a = [1, 2, [4, 5]]
b = copy.copy(a)
a[2][0] = 0
print(a)
print(b)
print("")

a = [1, 2, [4, 5]]
b = copy.deepcopy(a)
a[2][0] = 0
print(a)
print(b)
print("")

