import os


def mkdir(path):

    path = path.strip()  # 去除首位空格
    path = path.rstrip("//")  # 去除尾部 / 符号

    # 判断路径是否存在(True存在，False不存在)
    is_exists = os.path.exists(path)

    # 判断结果
    if not is_exists:
        os.makedirs(path)
        print(path + '创建成功')
        return True
    else:
        print(path + '目录已存在')
        return False


if __name__ == "__main__":
    path = "/Users/micllo/tmp/bbb/history/"
    mkdir(path)

