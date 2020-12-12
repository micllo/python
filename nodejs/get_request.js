// https://www.runoob.com/nodejs/node-js-get-post.html

var http = require('http');
var url = require('url');
var util = require('util');

http.createServer(function(req, res){
    res.writeHead(200, {'Content-Type': 'text/plain'});

    // 解析 url 参数
    var params = url.parse(req.url, true).query;
    res.write("网站名：" + params.name);
    res.write("\n");
    res.write("网站 URL：" + params.url);
    res.end();

}).listen(3000);

// 控制台执行:
// node get_request.js

// 浏览器访问：
// http://127.0.0.1:3000?name=百度&url=www.baidu.com