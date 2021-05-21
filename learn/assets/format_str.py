"""
    字符串拼接格式
"""
name = "测试开发"
money = 2000.1234

# 占位符
content1 = "姓名%s，工资%.2f" % (name, money)

# format
content2 = "姓名{name}，工资{money:.2f}".format(name=name, money=money)

# f-string
content3 = f"姓名{name}，工资{money:.2f}"
print(content1)
print(content2)
print(content3)

# https://pan.baidu.com/s/1Bt6S7ZnZGZfNYnaS3-Eobg&shfl=shareset

