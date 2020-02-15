from types import MethodType

"""
    动 态 给 类 -> 添加方法、修改方法
"""


class Student(object):

    def test(self):
        print("方法中原有的内容")


def new_test(self):
    print("新方法中的内容")


def set_name(self, name):
    self.name = name


def set_age(self, age):
    self.age = age


def set_sc(self, x, y):
    self.x = x
    self.y = y


if __name__ == "__main__":

    x1 = Student()
    x2 = Student()

    # 给 '实例对象' 添加 '实例方法'
    x1.set_age = MethodType(set_age, x1)
    x2.set_age = MethodType(set_age, x2)

    # 检查
    print("类Student是否存在'set_name'方法：" + str(hasattr(Student, "set_name")))
    print("类Student是否存在'set_age'方法：" + str(hasattr(Student, "set_age")))
    print("类Student是否存在'setsc'方法：" + str(hasattr(Student, "setsc")))
    print()

    print("实例对象x1是否存在'set_name'方法：" + str(hasattr(x1, "set_name")))
    print("实例对象x1是否存在'set_age'方法：" + str(hasattr(x1, "set_age")))
    print("实例对象x1是否存在'setsc'方法：" + str(hasattr(x1, "setsc")))
    print()

    print("实例对象x2是否存在'set_name'方法：" + str(hasattr(x2, "set_name")))
    print("实例对象x2是否存在'set_age'方法：" + str(hasattr(x2, "set_age")))
    print("实例对象x2是否存在'setsc'方法：" + str(hasattr(x2, "setsc")))
    print()

    print("==========================\n")

    # 给 '类' 添加 '方法'
    Student.setsc = MethodType(set_sc, Student)
    Student.set_name = MethodType(set_name, Student)

    # 检查
    print("类Student是否存在'set_name'方法：" + str(hasattr(Student, "set_name")))
    print("类Student是否存在'set_age'方法：" + str(hasattr(Student, "set_age")))
    print("类Student是否存在'setsc'方法：" + str(hasattr(Student, "setsc")))
    print()

    print("实例对象x1是否存在'set_name'方法：" + str(hasattr(x1, "set_name")))
    print("实例对象x1是否存在'set_age'方法：" + str(hasattr(x1, "set_age")))
    print("实例对象x1是否存在'setsc'方法：" + str(hasattr(x1, "setsc")))
    print()

    print("实例对象x2是否存在'set_name'方法：" + str(hasattr(x2, "set_name")))
    print("实例对象x2是否存在'set_age'方法：" + str(hasattr(x2, "set_age")))
    print("实例对象x2是否存在'setsc'方法：" + str(hasattr(x2, "setsc")))
    print()

    # 给 '类' 修改 '方法'
    Student.test = MethodType(new_test, Student)
    stu = Student()
    stu.test()

    x1.set_age(12)
    x2.set_age(13)

    x1.setsc("xmc", "xu")

    # 为类属性赋值
    Student.set_name("hhh")

    print(x1.age)
    print(x2.age)
    print(x1.x, x1.y)
    print(x1.name)
    print(x2.name)
