"""
    获取 字符串中的 中文

    str.encode("utf-8")：将 string类型 转换成  byte数组
    str.decode("utf-8")：将 byte数组 转换成 string类型
"""
a = "not 404 found 张三 99 深圳"
a_list = a.split(" ")
res = []
for i in a_list:
    # 判断 string类型 是否为纯字母（包含：字母、中文）
    if i.isalpha():
        # 将 string类型 转换 byte数组 -> b'not'、b'\xe5\xbc\xa0\xe4\xb8\x89'
        i = i.encode("utf-8")
        print(i)
        print(type(i))
        # 判断 byte数组 是否为纯字母（仅包含：字母）
        if not i.isalpha():
            res.append(i.decode("utf-8"))
print(res)







