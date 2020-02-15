# .-*- coding:utf-8 .-*-

import pika
import time

# 建立实例
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

# 声明管道
channel = connection.channel()

# durable=True 队列持久化
channel.queue_declare(queue='hello2', durable=True)


def callback(ch, method, properties, body):  # 四个参数为标准格式
    # print "ch : " + str(ch) + "\n"
    # print "method : " + str(method) + "\n"
    # print "properties : " + str(properties) + "\n"
    print(" [x] Received %r" % body)
    time.sleep(5)
    print "停留完毕"
    ch.basic_ack(delivery_tag=method.delivery_tag)  # 告诉生成者，消息处理完成


# 类似权重，按能力分发，如果有一个消息，就不在给你发
channel.basic_qos(prefetch_count=2)
channel.basic_consume(callback, queue='hello2', no_ack=False)

print(' [*] Waiting for messages. To exit press CTRL+C')

# 开始消费消息
channel.start_consuming()