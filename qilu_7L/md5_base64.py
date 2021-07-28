import random, base64, hashlib


def set_password(pwd):
    """
       在 密码 前面加上三位随机数字后，进行 base64 转码
    """
    if pwd not in ["", None]:
        random_num = str(random.randint(100, 999))  # 随机生成三位数字符串
        pwd_bytes = base64.b64encode((random_num + pwd).encode("utf-8"))
        return str(pwd_bytes, encoding="utf-8")
    else:
        return pwd


def md5_key(uid, rstr, token):
    """
        key = MD5(uid+rstr+token) 32位小写
    :param uid:
    :param rstr:  任意3位字符
    :param token:
    :return: 返回 生成的 key
    """
    md5 = hashlib.md5()
    md5.update((str(uid) + str(rstr) + str(token)).encode("utf-8"))
    return md5.hexdigest()


if __name__ == "__main__":

    pwd_base64 = set_password("123456")
    print(pwd_base64)

    uid = "a2344567gfg45776t"
    rstr = "lgb"
    token = "he343545ddf4564tgbdh34565ergfdg3"
    key = md5_key(uid, rstr, token)
    print(key)
