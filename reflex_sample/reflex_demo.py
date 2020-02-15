class Person:
    country = "中国"

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show_info(self):
        print("我的姓名: %s, 年龄: %d" % (self.name, self.age))

    def show(self):
        print("++++++++++++")

    @classmethod
    def show_country(cls):
        print(cls.country)


if __name__ == "__main__":

    p1 = Person("xixi", 7)

    """
        getattr()
    　　　　功能：获取实例的属性值或者方法地址
    　　　　返回值：属性的值/方法的地址
    　　　　getattr(对象，属性名/方法名)
    　　　　getattr(类，属性名/方法名)
    """

    # 获取 实例对象'p1'的属性'name'
    name = getattr(p1, "name", "11111")
    print(name)

    # 获取 实例对象'p1'的方法'show_info'（ 该方法绑定了实例对象 p1 ）
    show_info = getattr(p1, "show_info")
    print(show_info)  # <bound method Person.show_info of <__main__.Person object at 0x000000000294AD68>>

    # 执行 实例对象'p1'的方法'show_info'
    show_info()

    demo = getattr(show_info, "__unittest_skip__", False)
    print(demo)

#     # 获取 类'Person'的类属性'country'
#     country = getattr(Person, "country")
#     print(country)
#
#     # 获取 类'Person'的类方法'show_contry'
#     show_country = getattr(Person, "show_country")
#     print(show_country)  # <bound method Person.show_country of <class '__main__.Person'>>
#
#     # 执行 类'Person'的类方法'show_contry'
#     show_country()
#
#     """
#         hasattr()
# 　　　　    功能：检测是否具有某个类方法，类属性，实例属性，实例方法
# 　　　　    返回值：bool值
# 　　　　    hasattr(对象，实例属性/实例方法)
# 　　　　    hasattr(类，类属性/类方法)
#     """
#
#     print(hasattr(p1, "name"))               # True
#     print(hasattr(p1, "show_info"))          # True
#     print(hasattr(p1, "get_num"))            # False
#     print(hasattr(Person, "country"))        # True
#     print(hasattr(Person, "show_country"))   # True
#
#     """
#       setattr()
# 　　　　    功能: 设置实例/类的属性值
# 　　　　    返回值: 无
# 　　　　    setattr(对象, 属性名, 属性值)
# 　　　　    setattr(类, 属性名, 属性值)
# 　　　 　   如果属性已存在, 重新赋值;
# 　　　　    如果属性不存在, 添加属性并赋值;
#     """
#
#     # 查看 方法 和 属性
#     print(dir(Person))
#     print(dir(p1))
#
#     # 修改实例对象'p1'的属性'age'值
#     setattr(p1, "age", 33)
#     print(p1.age)
#
#     # 添加实例对象'p1'的属性'friend'值为'haha'
#     setattr(p1, "friend", "haha")
#     print(p1.friend)
#
#     print(dir(Person))
#     print(dir(p1))
#
#     # 修改类'Person'的属性'country'值
#     setattr(Person, "country", "中华人民共和国")
#     print(Person.country)
#
#     # 添加类'Person'的属性'color'值为'黄'
#     setattr(Person, "color", "黄")
#     print(Person.color)
#     print(p1.color)
#
#     print(dir(Person))
#     print(dir(p1))
#
#     """
#        delattr()
# 　　　　    功能: 删除对象/类的 属性、方法　　
# 　　　      返回值: 无
# 　　　　    delattr(对象, 属性名)
# 　　　　    delattr(类, 属性名)
# 　　　　    要删除的属性不存在, 报错AttributeError: color
#
#     """
#
#     # 删除实例对象'p1'的属性'age'
#     delattr(p1, "age")
#     print(hasattr(p1, 'age'))
#     # print(p1.age)  # AttributeError: 'Person' object has no attribute 'age'
#
#     # 删除实例对象'p1'的属性'age'
#     delattr(p1, "age")
#     print(hasattr(p1, 'age'))
#
#     # 删除类'Person'的属性'country'
#     delattr(Person, "country")
#     print(hasattr(Person, 'country'))
#
#     # 删除类'Person'的实例方法'show_info'
#     delattr(Person, 'show_info')
#     print(hasattr(p1, 'show_info'))
#
#     # 删除类'Person'的类方法'show_country'
#     delattr(Person, "show_country")
#     print(hasattr(Person, "show_country"))
#
