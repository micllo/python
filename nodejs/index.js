var server = require("./server");
var router = require("./router");

// router.route()
server.start(router.route);
