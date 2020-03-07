# coding:UTF-8
from flask import Flask, url_for, jsonify
from werkzeug.routing import BaseConverter

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/login")
def login():
    dict1 = {"name": "fxc"}
    return jsonify(dict1)


# 接受URL参数类型：unicode
@app.route('/<params>')
def one(params):
    print(type(params))
    return 'URL Parmas : ' + params


# 接受URL参数类型：int
@app.route('/<int:age>/')
def two(age):
    print(type(age))
    return 'int params'


# 只允许POST请求
@app.route('/<float:price>/', methods=['post'])
def get_request(price):
    print(type(price))
    return '只允许POST请求: ' + str(price)


# 通过别名反向生成url参数
@app.route('/<path:url>/', endpoint='baidu', methods=['get', 'post'])
def three(url):
    print(url_for('baidu', url=url))
    return '通过别名反向生成url参数'


class RegexConverter(BaseConverter):
    """
    自定义URL匹配正则表达式
    """

    def __init__(self, map, regex):
        super(RegexConverter, self).__init__(map)
        self.regex = regex

    def to_python(self, value):
        """
        路由匹配时，匹配成功后传递给视图函数中参数的值
        """
        return int(value)

    def to_url(self, value):
        """
        使用url_for反向生成URL时，传递的参数经过该方法处理，返回的值用于生成URL中的参数
        """
        val = super(RegexConverter, self).to_url(value)
        return val


# 添加到flask中
app.url_map.converters['regex'] = RegexConverter


@app.route('/index/<regex("\d+"):nid>')
def index(nid):
    print(url_for('index', nid='888'))
    return 'Index'


if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=6666)
    app.run()
