// 引入 events 模块
var events = require('events');

// 创建 eventEmitter 对象
var eventEmitter = new events.EventEmitter();

// 创建 事件处理程序
var connectHandler = function con(arg) {
   console.log('连接成功。' + arg);

   // 触发 data_received 事件
   eventEmitter.emit('data_received');
}


// 绑定(监听) connection 事件 (使用'con'回调函数) -> 处理程序
eventEmitter.on('connection', connectHandler);

// 绑定(监听) data_received 事件 (使用匿名回调函数) -> 处理程序
eventEmitter.on('data_received', function(){
   console.log('数据接收成功。');
});

// 触发 connection 事件
eventEmitter.emit('connection', '参数1');

console.log("程序执行完毕。");

// 提供方法 供其他模块调用
exports.world = function () {
    console.log("Hello World!")
}