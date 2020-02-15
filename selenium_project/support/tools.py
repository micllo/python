# coding=utf-8
from datetime import date, timedelta
import logging


def date_n(n):
    """
    返回n天后的日期
    :param n:
    :return:
    """
    return str((date.today() + timedelta(days=+int(n))).strftime("%Y-%m-%d"))


def log(show_content):
    """
    日志函数
    :param show_content:
    :return:
    """
    # 配置日志显示格式
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(filename)s %(levelname)s %(message)s",
                        datefmt="%Y-%d-%m %H:%M:%S",
                        filename="selenium_project/log/testLog.log")

    # 将相关日志打印到 log 文件中
    logging.info(show_content)

    # 在控制台显示相关日志内容
    # console = logging.StreamHandler()
    # console.setLevel(logging.INFO)
    # formatter = logging.Formatter('%(name)-6s: %(levelname)-8s %(message)s')
    # console.setFormatter(formatter)
    # logging.getLogger('').addHandler(console)


if __name__ == "__main__":
   pass
