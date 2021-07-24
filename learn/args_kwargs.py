# coding=utf-8


def test(*info, **data):
    """
        *info ： 接收不定长 元祖
        **data： 接收不定长 字典
    """
    print(info)
    print(type(info))
    print(data)
    print(type(data))


#  *args 用来将参数打包成tuple给函数体调用，输出结果以元组的形式展示
def print_msg(*args):
    print(args)
    print('args的类型是{0}'.format(type(args)))
    print('args的长度是{0}'.format(len(args)))


#  **kwargs 打包关键字参数成dict给函数体调用,输出结果以字段形式
def print_msg2(**kwargs):
    print(kwargs)
    print('args的类型是{0}'.format(type(kwargs)))
    print('args的长度是{0}'.format(len(kwargs)))


if __name__ == '__main__':

    test("aa", "bb", a=11, b="22")
    print('---------------------\n')

    # *args 用来将参数打包成tuple给函数体调用，输出结果以元组的形式展示 实例
    print_msg('tigger', 'mouse', 'Elephant', 'Lion')
    print('---------------------\n')

    a = ['tigger', 'mouse', 'Elephant', 'Lion']
    print_msg(a)
    print('---------------------\n')

    # *脱去一层外套
    print_msg(*a)
    print('---------------------\n')

    a = [['tigger', 'mouse'], ['Elephant', 'Lion']]
    print_msg(a)
    print('---------------------\n')

    # *脱去一层外套
    print_msg(*a)
    print('---------------------\n')

    print_msg2(x=1, y=2)
    print('---------------------\n')

    a = {'x': 1, 'y': 2}
    print_msg2(**a)