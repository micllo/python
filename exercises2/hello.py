# coding:UTF-8

from flask import Flask
app = Flask(__name__)

# http://192.168.23.250:1234
@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)