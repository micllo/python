import os

file_name = "report_123.html"
path = "/Users/micllo/tmp/bbb/"
history_file = "/Users/micllo/tmp/bbb/history/"

res = os.system("cp " + history_file + file_name + " " + path + " && mv " + path + file_name + " " + path + "report.html")
if res != 0:
    print("测试报告替换操作有误！")


