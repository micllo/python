import requests

"""
    接 口 示 例
    https://docs.python-requests.org/zh_CN/latest/
    http://ws.webxml.com.cn/WebServices/WeatherWS.asmx?op=getSupportCityString
    
    【 requests 参考文档 】
    https://docs.python-requests.org/zh_CN/latest
    https://docs.python-requests.org/zh_CN/latest/user/quickstart.html#id5
    
    1.常见的请求正文格式（Body）
    （1）url-encoded：文本格式（网页表单提交数据的默认格式）
    （2）multipart/form-data：表单格式（上传文件接口）
    （3）raw：自由格式（JSON、TEXT、JavaScript、HTML、XML）
    （4）binary：二进制格式
    
    2.请求头信息中的重要字段：Content-Type
    （1）application/json
    （2）www-xxxx-url-encode
    （3）text/xml
    （4）application/xml
    （5）空着（上传文件）
        
    3.接口 入参、出参 格式种类
    （1）入参：form、出参：json
    （2）入参：json、出参：json
    （3）入参：form、出参：html
    （4）入参：xml、出参：xml

"""

# 1.HTTP协议：GET 请求
host = "http://ws.webxml.com.cn"
params = {"theRegionCode": 311101}
get_r = requests.get(url=host+"/WebServices/WeatherWS.asmx/getSupportCityString", params=params)
print(get_r.text)


# 2.HTTP协议：POST 请求（ 入参 form 格式 ）
host = "http://ws.webxml.com.cn"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {"theRegionCode": 311101}
form_r = requests.post(url=host+"/WebServices/WeatherWS.asmx/getSupportCityString", headers=headers, data=data)
print(form_r.text)


# 3.HTTP协议：POST 请求（ 入参 json 格式 ）（API自动化框架）
host = "http://127.0.0.1:7060/api_local"
headers = {"Content-Type": "application/json"}
# 方式1：json 对应 字典
json = {"name": "messi", "passwd": "messi"}
json_r = requests.post(url=host+"/test/login", headers=headers, json=json)
print(json_r.text)

# 方式2：data 对应 字符串
data = '{"name": "messi", "passwd": "messi"}'
data_r = requests.post(url=host+"/test/login", headers=headers, data=data)
print(data_r.text)


# 4.WebService: SOAP协议 （ 入参 xml 格式 ）
host = "http://ws.webxml.com.cn"
headers = {"Content-Type": "text/xml;charset=utf-8", "SOAPAction": "http://WebXml.com.cn/getSupportCityString"}
xml = '''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <getSupportCityString xmlns="http://WebXml.com.cn/">
      <theRegionCode>311101</theRegionCode>
    </getSupportCityString>
  </soap:Body>
</soap:Envelope>'''
soap_r = requests.post(url=host+"/WebServices/WeatherWS.asmx", headers=headers, data=xml)
print(soap_r.text)


# 5.上传接口（API自动化框架 - 批量导入接口）
host = "http://127.0.0.1:7060/api_local"
file_name = "测试用例模板.xlsx"
file_path = "/Users/micllo/Downloads/测试用例模板.xlsx"
files = {"file": open(file_path, "rb")}
res = requests.post(url=host + "/API/import_action/pro_demo_1/batch_insert_and_replace", files=files)
print(res.text)


# 6.下载接口（API自动化框架 - 下载用例模板接口）
download_path = "/Users/micllo/Downloads/用例模板下载.csv"
res = requests.get(url="http://localhost:7060/api_case_tmpl")
with open(download_path, "wb") as fd:
    for text in res.iter_content(1024):
        fd.write(text)


# 7.使用 session 会话保持（ 前提：上游接口是通过在浏览器中保存 cookie 的方式来实现的 ）
# 调用方式1：模拟浏览器 保持同一个session 解决关联问题
session = requests.session()
r1 = session.get(url="登录接口")  # 会将cookie保存在session中（保证下游接口的登录状态）
r2 = session.get(url="查询接口")  # 会直接带上session中的cookie < 调用成功 >
# 调用方式2：使用不同的session
rr1 = requests.session().get(url="登录接口")
rr2 = requests.session().get(url="查询接口")  # < 调用失败 >


# 8.关联下游接口1
res = requests.get(url="接口1", allow_redirects=False)  # 禁止重定向
print(res.status_code)
print(res.history)  # 显示历史重定向
# 获取cookies
token = res.cookies["token"]
uid = res.cookies["uid"]
r = requests.post(url="接口2", headers={"Content-Type": "application/json", "Cookie": "token=" + token + ';uid=' + uid},
                  json={"city": "1000", "month": "2"})


# 9.关联下游接口2
host = "http://127.0.0.1:7060/api_local"
headers = {"Content-Type": "application/json"}
json = {"name": "messi", "passwd": 33}
res1 = requests.post(url=host+"/test/login", json=json, headers=headers)
print(res1.text)
token = res1.json()["data"]["token"]
print(token)
# 传递token方式1：
res2 = requests.get(url=host+"/test/get_image" + "?token="+token)
print(res2.text)
# 传递token方式2：
rr = requests.get(url="接口", headers={"Authorization": "Bearer " + token})


# 10.接口超时，失败重试三次
for i in range(0, 3):
    try:
        r = requests.get(url="http://192.168.31.111:1180/api_local", timeout=3)
        break
    except:
        print("失败重试" + str(i))
else:
    raise Exception("失败三次，接口异常！！！")


