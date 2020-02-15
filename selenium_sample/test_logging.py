# coding=utf-8
import logging

# # 自定义 日志显示格式
# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# DATE_FORMAT = "%Y-%d-%m %H:%M:%S"
#
# # 设置日志的基本配置（将error级别及大于该级别的日志打印到test.log文件中）
# logging.basicConfig(filename="log/test.log", level=logging.ERROR, format=LOG_FORMAT, datefmt=DATE_FORMAT)
#
# logging.debug("I am a debug level log.")
# logging.info("I am a info level log.")
# logging.warning("I am a warning level log.")
# logging.error("I am a error level log.")
# logging.critical("I am a critical level log.")
#
# logging.log(logging.DEBUG, "===== I am a debug level log.")
# logging.log(logging.INFO, "===== I am a info level log.")
# logging.log(logging.WARNING, "===== I am a warning level log.")
# logging.log(logging.ERROR, "===== I am a error level log.")
# logging.log(logging.CRITICAL, "===== I am a critical level log.")


# 提供一个日志函数
def log(str):

    # 将相关日志打印到 log-selenium.log 文件中
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(filename)s %(levelname)s %(message)s",
                        filemode='a',  # 模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                                       # a是追加模式，默认如果不写的话，就是追加模式
                        datefmt="%Y-%d-%m %H:%M:%S",
                        filename="log/log-selenium.log")
    logging.info(str)

    # 在控制台显示相关日志内容
    # console = logging.StreamHandler()
    # console.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(name)-6s: %(levelname)-8s %(message)s')
    # console.setFormatter(formatter)
    # logging.getLogger('').addHandler(console)
    # logging.info(str)


if __name__ == '__main__':
    log("显示需要日志打印的内容")

