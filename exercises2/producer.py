# .-*- coding:utf-8 .-*-

import pika
import random

# 建立一个实例
credentials = pika.PlainCredentials('guest', 'guest')
param = pika.ConnectionParameters('localhost', 5672, '/', credentials)
conn = pika.BlockingConnection(param)

# 声明一个管道，在管道里发消息
channel = conn.channel()

# 在管道里声明queue （ durable=True 队列持久化 ）
channel.queue_declare(queue='hello2', durable=True)

number = random.randint(1, 1000)

# delivery_mode=2 消息持久化
for num in range(10):
    body = 'hello world:%s' % num
    channel.basic_publish(exchange='', routing_key='hello2', body=body, properties=pika.BasicProperties(delivery_mode=2))
    print " [x] Sent %s" % body

# 队列关闭
conn.close()