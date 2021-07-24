import time

# 获取当前时间戳
time_stamp = time.time()
print(time_stamp)

# 时间戳 --> 时间元祖
time_tuple = time.localtime(time_stamp)
print(time_tuple)

# 时间元祖 --> 时间戳
time_stamp2 = time.mktime(time_tuple)
print(time_stamp2)

# 时间元祖 --> 时间字符串
time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
print(time_str)

# 时间字符串 --> 时间元祖
time_tuple2 = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
print(time_tuple2)