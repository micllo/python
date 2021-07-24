"""
  【 迭 代 器 】

   迭代器：
        是一个可以记住遍历位置的对象，迭代器只能往前不会退后。
   优势：
    （1）节省内存空间（它没有数据，你需要下一个元素，它就按照算法给你计算出下一个元素返回）
    （2）执行效率高
   应用场景：
    （1）range(1000)：不是生成一个1000个元素的集合，而是内置了next函数，逐个生成
    （2）使用 for line in file: 调用文件，则是迭代器中逐行前进，也是内置了next行数
         而使用 file.readlines() 调用文件，返回的是一个列表
"""


class Classes(object):

    def __init__(self, number):
        self.number = number
        self.student = []
        self.n = 0  # 类似与指针的作用

    def add(self, name, age):
        self.student.append((name, age))

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < len(self.student):
            n = self.n
            self.n += 1
            return self.student[n]
        else:
            raise StopIteration


a = Classes("1-1")
a.add("张三", 6)
a.add("李四", 7)

for i in a: print(i)
print("++++++++")

# 无法进行第二次迭代
for i in a: print(i)


"""
    【 生 成 器 】迭代器的一种
    生成器：一边循环, 一边计算，保存的是算法，而不是数据
    目的：为了不必创建完整的list，从而节省大量的空间
    注意：生成器也是一种迭代器，但是只能对其迭代一次，
          因为他们并没有把所有的值存在内存中，而是在运行时生产值
"""
# 列表生成式（占用内存空间）
a = [i for i in range(0, 10)]
print(type(a))

# 生成器表达式（不占用内存空间）
b = (i for i in range(0, 10))
print(type(b))


# 不推荐：执行效率低，占用空间大
# 返回：list
def get_odd1(lst):
    res = []
    for i in lst:
        if i % 2:  # 除以2后的余数
            res.append(i)  # 保存奇数
    return res


print(get_odd1(a))


# 推荐：执行效率高，占用空间更小
# 返回：生成器（需要配合for循环来获取生成的元素）
def get_odd2(lst):
    for i in lst:
        if i % 2:
            yield i


for i in get_odd2(a):
    print(i)


# 在web自动化中的应用场景（ 代替 setup、teardown 方法 ）
def A():
    print("打开浏览器")
    yield 0
    print("关闭浏览器")


for i in A():
    print(i)
