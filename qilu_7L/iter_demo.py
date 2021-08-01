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

    文件读取方法：
    read()       读取整个文件
    readline()   每次读取一行，返回的是一个字符串，保持当前行的内容
    readlines()  一次性读取整个文件，返回 列表（包含每行的字符串） < 推荐 >

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

#
# a = Classes("1-1")
# a.add("张三", 6)
# a.add("李四", 7)
#
# for i in a: print(i)
# print("++++++++")
#
# # 无法进行第二次迭代
# for i in a: print(i)


""" ################################################################ """


"""
    【 生 成 器 】迭代器的一种
    生成器：一边循环, 一边计算，保存的是算法，而不是数据
    目的：为了不必创建完整的list，从而节省大量的空间
    注意：生成器也是一种迭代器，但是只能对其迭代一次，
          因为他们并没有把所有的值存在内存中，而是在运行时生产值
"""
# 列表生成式（占用内存空间）
a = [i for i in range(0, 10)]
# print(type(a))

# 生成器表达式（不占用内存空间）
b = (i for i in range(0, 10))
# print(type(b))


# 不推荐：执行效率低，占用空间大
# 返回：list
def get_odd1(lst):
    res = []
    for i in lst:
        if i % 2:  # 除以2后的余数
            res.append(i)  # 保存奇数
    return res


# print(get_odd1(a))


# 推荐：执行效率高，占用空间更小
# 返回：生成器（需要配合for循环来获取生成的元素）
def get_odd2(lst):
    for i in lst:
        if i % 2:
            yield i


# for i in get_odd2(a):
#     print(i)


# 在web自动化中的应用场景（ 代替 setup、teardown 方法 ）
def A():
    print("打开浏览器")
    yield 0
    print("关闭浏览器")


# for i in A():
#     print(i)


""" ################################################################ """


"""
    yield 两个方法： next()、send()
"""


def foo():
    print("starting...")
    num = 1
    while num <= 10:
        new_num = yield num
        print("new_num:", new_num)
        if new_num:
            num = new_num
        else:
            num += 1
    print("end...")

# g = foo()
# print(next(g))
# print("*"*20)
# print(g.send(7))
# print("*"*20)
# print(next(g))

# gg = foo()
# for i in gg:
#     if i == 5:
#         gg.send(9)
#     print(i)


""" ################################################################ """


"""  
   【 封装只需要生成一次的生成器 】 
    1.生成器 需要 生成 返回值
    2.生成器 需要 接受 外部参数
"""


def yield_demo():
    print("开始操作")
    out_value = yield "yield_demo 返回值"
    print("yield_demo 接收：" + str(out_value))
    print("结束操作")


# yield装饰
def yield_decorator(fun):
    def warp(*args, **kwargs):
        yield_func = yield_demo()
        try:
            for yield_return in yield_func:  # 循环中自动调用next()方法 -> yield_return = next(yield_func)
                yield_func.send(fun(yield_return=yield_return, *args, **kwargs))
        except StopIteration:
            pass
    return warp


# 普通装饰器
def general_decorator(func):
    def warp(*args, **kwargs):
        print("开始操作")
        func_return = func(yield_return="yield_demo返回值", *args, **kwargs)
        print("yield_demo接收值：" + str(func_return))
        print("结束操作")
    return warp


@yield_decorator
def action_1(args, yield_return=None):
    print("action_1 获取：" + yield_return)
    print("action_1 执行：" + args)
    return "action_1 返回值"


@yield_decorator
def action_2(args1, args2, yield_return=None):
    print("action_2 获取：" + yield_return)
    print("action_2 执行：" + args1 + "、" + args2)
    return "action_2 返回值"


@general_decorator
def action_3(args, yield_return=None):
    print("action_3 获取：" + yield_return)
    print("action_3 执行：" + args)
    return "action_3 返回值"


print()
action_1(args="操作 01")  # action_1 = yield_decorator(action_1)
print()
action_2(args1="操作 02_1", args2="操作 02_2")
print()
action_3(args="操作 03")







