# coding:UTF-8

""" yield 的 next()  send() 函数 """


def fun():
    for i in range(20):
        x = yield i
        print('good', x)


# # 程序开始执行以后，因为fun函数中有yield关键字，所以fun函数并不会真的执行，而是先得到一个生成器a(相当于一个对象)
# a = fun()
# # next()表示 第一次迭代到yield位置，并返回yield后面参数的值，此时程序停止了不再往下执行 (注意：并不会将i的值赋值给x)
# re = a.next()
# print(re)
# # send(30)表示 从上次yield位置介入，并将参数30作为'yield i'表达式的值，第二次迭代到yield位置，并返回yield后面参数的值
# x = a.send(30)
# print(x)
# print(" ")


""" 为什么要使用yield """
# 因为如下生成器中使用list，会占用大量的空间，所以可以使用yield组合生成器来实现
# for n in range(1000):
#     a = n


def foo(num):
    print("starting...")
    while num < 10:
        num = num + 1
        yield num


# for循环会触发next()方法
for n in foo(0):
    print(n)



