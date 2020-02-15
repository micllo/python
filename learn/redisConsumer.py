# -*- coding:utf-8 -*-
from redisHelper import RedisHelper

# 订阅
obj = RedisHelper()
redis_sub = obj.subscribe()

while True:
    msg = redis_sub.parse_response()
    print (msg)
