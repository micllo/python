
"""
 【 利用列表实现数据结构 -- 栈（ 先进后出 ） 】
    有极限大小
    可以弹栈
    可以压栈
    栈满时压栈，提示已满
    栈空时弹栈，提示为空

    要求：
    0.不能直接访问栈
    1.初始化函数，传入栈的极限大小
    2.提供一个弾栈和一个压栈的方法
    3.提供一个获取栈极限大小的方法
    4.其他方法私有--判断栈是否到达极限，栈是否为空
"""


class stack:

    def __init__(self, size):
        self.size = size
        self.data = []

    def add(self, a):
        if not self.__is_full():
            self.data.append(a)
        else:
            print("栈已满")

    def delete(self):
        if not self.__is_empty():
            return self.data.pop()
        else:
            print("栈已空")

    def __is_full(self):
        return len(self.data) == self.size

    def __is_empty(self):
        return len(self.data) == 0

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)

    def __iter__(self):
        # 实现迭代
        pass


if __name__ == "__main__":

    s1 = stack(size=3)
    s1.add("hello")
    s1.add("world")
    print(len(s1))
    print(s1)