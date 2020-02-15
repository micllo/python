
"""
 【 功 能 】
  1.通过字符串的反射，实现动态的函数调用
  2.通过__import__()函数，实现动态导入同名的模块

  【 操 作 】
  运行后输入：common/home  （ 模块名/方法名 ）
"""


def get_page_url_by_str():
    inp = input("请输入您想访问页面的url：  ").strip()
    modules, func = inp.split("/")
    obj = __import__("lib." + modules, fromlist=True)  # 基于字符串的动态模块导入
    print(obj)
    if hasattr(obj, func):
        func = getattr(obj, func)  # 获取common.py模块文件中的'func'函数
        func()  # 执行相应的函数
    else:
        print("404")

    # 取代如下操作
    # if inp == "login":
    #     common.login()
    # elif inp == "logout":
    #     common.logout()
    # elif inp == "home":
    #     common.home()
    # else:
    #     print("404")


if __name__ == '__main__':

    get_page_url_by_str()
