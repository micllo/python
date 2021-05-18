# coding: utf-8
import requests, json

url = "http://127.0.0.1:7060/api_local/API/import_action/pro_demo_1/batch_insert_and_replace"
file_path = "/Users/micllo/Downloads/测试用例模板.xlsx"
file_name = "测试用例模板.xlsx"


data = {'filesize': 1}
print(type(data))
files = {'file': (file_name, open(file_path, 'rb'))}
print(files)
res = requests.post(url=url, data=data, files=files)
print(res.request.body)
print(res.text)

test = {}
test = test and json.dumps(test) or ""
print(test)