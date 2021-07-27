
"""
 【 利用 列表 实现 -- 栈（ 先进后出 ） 】
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


"""
    【 利用 列表 实现 -- 队列（ 先进先出 ） 】
"""


class queue:

    def __init__(self, size):
        self.size = size
        self.data = []

    def __is_full(self):
        return len(self.data) == self.size

    def __is_empty(self):
        return len(self.data) == 0

    def add(self, a):
        if not self.__is_full():
            self.data.append(a)
        else:
            print("队列已满")

    def delete(self):
        if not self.__is_empty():
            return self.data.pop(0)
        else:
            print("队列已空")

    def __len__(self):
        return len(self.data)

    def __str__(self):
        return str(self.data)


"""
    【 利用 双栈 实现 -- 队列（ 先进先出 ） 】
    
      弹出栈的逻辑 - 目的 将最先进入的元素删除
    
        第一步：in_stack中添加元素
        in_stack = [1, 2, 3]
        out_stack = []
        
        第二步：in_stack依次弹出，out_stack依次放入
        in_stack = []
        out_stack = [3, 2, 1]
        
        第三步：out_stack 弹出最后一个元素
        in_stack = []
        out_stack = [3, 2]
        
        第四步：out_stack依次弹出，in_stack依次放入
        in_stack = [2, 3]
        out_stack = []
    
"""

class queue2:

    def __init__(self, size):
        self.size = size
        self.in_stack = stack(size=size)
        self.out_stack = stack(size=size)

    def __is_full(self):
        return len(self.in_stack) == self.size

    def __is_empty(self):
        return len(self.in_stack) == 0

    def __len__(self):
        return len(self.in_stack)

    def __str__(self):
        return str(self.in_stack)

    def add(self, a):
        if not self.__is_full():
            self.in_stack.add(a)
        else:
            print("队列已满")

    def delete(self):
        if not self.__is_empty():
            # 将 in_stack 中的元素 依次 弹入 out_stack 中
            while len(self.in_stack) > 0:
                self.out_stack.add(self.in_stack.delete())
            # out_stack 弹出最后一个
            self.out_stack.delete()
            # 将 out_stack 中的元素 依次 弹入 in_stack 中
            while len(self.out_stack) > 0:
                self.in_stack.add(self.out_stack.delete())
        else:
            print("空队列")


if __name__ == "__main__":

    s = stack(size=3)
    s.add("aaa")
    s.add("bbb")
    s.add("ccc")
    s.add("ddd")
    for i in range(4):
        print(s)
        print(len(s))
        s.delete()

    print("\n---------\n")

    q = queue(size=3)
    q.add("aaa")
    q.add("bbb")
    q.add("ccc")
    q.add("ddd")
    for i in range(4):
        print(q)
        print(len(q))
        q.delete()

    print("\n---------\n")

    q2 = queue2(size=3)
    q2.add("aaa")
    q2.add("bbb")
    q2.add("ccc")
    q2.add("ddd")
    for i in range(4):
        print(q2)
        print(len(q2))
        q2.delete()