# .-*- coding:utf-8 .-*-
import redis

# 创建连接池
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)  # 默认使用 db=0
# pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1)
# 连接
r = redis.Redis(connection_pool=pool)

# 使用管道
pipe = r.pipeline(transaction=True)

# 添加
r.set('name', 'fxc')
r.set('age', '18')
r.set('sex', 'nan')

# pipline 一次请求处理多个命令
pipe.execute()

# 获取
print (r.get('name'))


