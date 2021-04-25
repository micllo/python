var fs = require("fs");

// 不使用回调函数 -> 阻塞（同步）
var data = fs.readFileSync('input.txt');
console.log(data.toString());
console.log("阻塞：等待以上程序执行完毕后，才执行该语句!");

// 使用回调函数返回结果 -> 非阻塞（异步）
fs.readFile('input1.txt', function (err, data) {
    if (err) {
        console.log(err.stack);
        return;
    }
    console.log(data.toString());
});
console.log("非阻塞：同步执行该语句!");


