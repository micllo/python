import time,requests
from tomorrow import threads


# 使用装饰器，这个函数异步执行
@threads(10)
def download(url):
    return requests.get(url)


def main():
        start = time.time()
        urls = [
            'https://pypi.org/project/tomorrow/0.2.0/',
            'https://www.cnblogs.com/pyld/p/4716744.html',
            'http://www.xicidaili.com/nn/10',
            'http://baidu.com',
            'http://www.bubuko.com/infodetail-1028793.html?yyue=a21bo.50862.201879',
        ]
        responses = [download(i) for i in urls]
        end = time.time()
        print("Time: %f seconds" % (end - start))


if __name__ == "__main__":
        main()
