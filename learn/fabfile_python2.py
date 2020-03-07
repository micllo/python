# coding:UTF-8
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.utils import abort
from fabric.colors import *
import json
import time
import re


# ============================== 分组执行任务 ==============================

# env.hosts = [
#     "tomcat@192.168.23.60:22",
#     "centos@192.168.1.141:22",
#     "tomcat@192.168.23.141:22"
# ]
#
#
# # 服务器分组
# env.roledefs = {
#     'tomcat': ["tomcat@192.168.23.60:22", "tomcat@192.168.23.141:22"],
#     'centos': ["centos@192.168.1.141:22"]
# }
#
#
# env.passwords = {
#     # 'tomcat': "tomcatpshl2016",
#     # 'centos': "centosps2016"
#     "tomcat@192.168.23.60:22": "tomcatpshl2016",
#     "tomcat@192.168.23.141:22": "tomcatpshl2016",
#     "centos@192.168.1.141:22": "centosps2016"
# }
#
#
# @runs_once  # 遍历主机时，只有第一台触发该函数
# def local_task():
#     with settings(warn_only=True):  # 运行忽略失败的命令继续执行
#         res = local("cd /test123456")
#         print res
#         print res.return_code  # 返回码，0表示正确执行，1表示错误
#         print res.failed
#         print "++++++++++++++++++++++++"
#     local("ls")
#
#
# @serial  # 强制该任务串行执行（默认是串行执行）
# @parallel(pool_size=1)  # 强制该任务并发执行，并限制线程数为1
# @roles('tomcat')
# def remote_task1():
#     run("hostname")
#     time.sleep(3)
#
#
# @roles('centos')
# def remote_task2():
#     run('uname -r')
#
#
# # 分组执行任务
# def doworks():
#     # 针对 env.hosts
#     # local_task()
#     # remote_task1()
#     # remote_task2()
#     # 针对 env.roledefs
#     # execute(local_task)
#     execute(remote_task1)
#     execute(remote_task2)
#
#
# # 执行命令： fab tail:path=/etc/passwd,line=5
# def tail(path='/etc/passwd', line=10):
#     result = run('tail -n {0} {1}'.format(line, path))
#     print "==============="
#     print result
#     print result.return_code  # 返回码，0表示正确执行，1表示错误
#     print result.failed
#     print "+++++++++++++++"
#
#
# print json.dumps(env, indent=3)



# ============================== 终端命令执行: fab test_get ==============================

# env.hosts = ['192.168.23.60']
# env.port = 22
# env.user = 'centos'
# env.password = 'centospshl2016'
#
# env.warn_only = True  # 运行忽略失败的命令继续执行 ( 全局变量 )
# env.parallel = True   # 并行执行 ( 全局变量 )
#
#
# # 使用管理者权限
# def test_sudo():
#     sudo("mkdir -p /home/tomcat/fxc")
#     with cd("/home/tomcat"):
#         with settings(warn_only=True):  # 运行忽略失败的命令继续执行
#             run("pwd")  # 这里应该使用 sudo("pwd)
#             result = sudo("ls")
#             print result
#
#
# # 本地执行命令
# @task
# def test_local():
#     with lcd("/Users/micllo/Downloads"):
#         result = local("ls", capture=True)  # 捕获标准输出的内容
#         print result
#         print type(result)
#         print result.failed     # 如果执行失败那么 result.failed 为True
#         print result.succeeded  # 如果执行成功那么 result.succeeded 为True
#
#
# # 从远程服务器上获取文件
# @task
# def test_get():
#     with settings(warn_only=True):
#         result = get(remote_path="/etc/passwd123456", local_path="/Users/micllo/Downloads/passwd_fxc")
#         if result.failed:
#             # abort("退出任务")  # 后续任务不会执行
#             warn(yellow("发出警告，但不退出任务"))
#             puts(cyan("某台服务器的打印信息"))
#             print red("文件获取失败")
#         else:
#             print green("文件获取成功")
#
#
# # 本地上传文件至服务器
# def test_put():
#     # put(remote_path="/home/centos/passwd_test", local_path="/Users/micllo/Downloads/passwd")
#     put(remote_path="/home/java/", local_path="/Users/micllo/Downloads/passwd", use_sudo=True)
#     # 若远程目录需要超级用户权限，则使用 use_sudo=True
#
#
# # 重启服务器
# def test_reboot():
#     reboot(wait=10)  # 等待*秒
#
#
# # 与服务器交互
# @task  # 限定只有带 @task 的函数可以使用fab命令
# def test_prompt():
#     # input = prompt("please input cmd: ")
#     # run(input)
#     port = prompt("Please input port number: ", default=8080, validate=int)  # 给定默认值，限定输入类型
#     print port
#
#
# @task
# def test_cat_file():
#     with settings(warn_only=True):
#         with cd("/home/tomcat"):
#             sudo("pwd")
#             sudo("ls")
#             content = sudo("cat *.sh")
#             print content
#             print type(content)
#
#
# @task
# def test_hide():
#     with hide("running", "stdout", "stderr"):  # hide表示隐藏，下面的命令隐藏running，stdout，stderr输出
#         run("ls /1111")
#
#
# @task
# def test_show():
#     with show("debug"):  # 打开debug输出，默认只有这项是关闭的
#         run("uname -r")
#
#
# @task
# def test_confirm():
#     result = confirm("Continue Anyway?")
#     print result


# ============================== 程 序 执 行 ==============================

def test_setting():
    host_port = 22
    # machine_ip = "192.168.23.170"
    # host_user = "centos"
    # host_pwd = "centosps2016"

    machine_ip = "192.168.23.60"
    host_user = "tomcat"
    host_pwd = "tomcatpshl2016"

    with settings(host_string="%s@%s:%s" % (host_user, machine_ip, host_port), password=host_pwd):
        # cmd_res = run("pgrep uwsgi")
        # cmd_res = run("ps aux | grep uwsgi | grep -v 'grep' | awk '{print $2}' ")
        # print cmd_res
        # print type(cmd_res)
        # pids = cmd_res.split("\r\n")
        # print pids
        # print type(pids)

        # data = run('pwd && sleep 3', warn_only=True)
        # data = run("ps aux | grep java | grep -v 'grep' | cut -c 10-15", warn_only=True)
        # data = run("ps aux | grep java | grep -v 'grep' | cut -c 10-15 | xargs kill -9", warn_only=True)
        data = run("ps aux | grep java | grep -v 'grep' | awk '{print $2}' ", warn_only=True)
        print data


def test_local_put_get():
    host_port = 22
    machine_ip = "192.168.23.60"
    host_user = "tomcat"
    host_pwd = "tomcatpshl2016"
    # 将本地文件上传服务器
    # with lcd("/Users/micllo/Downloads"):
    #     local("ls")
    #     with settings(host_string="%s@%s:%s" % (host_user, machine_ip, host_port), password=host_pwd):
    #         put(remote_path="/home/tomcat/", local_path="channel")

    # 从服务器获取文件到本地
    with settings(host_string="%s@%s:%s" % (host_user, machine_ip, host_port), password=host_pwd):
        with cd("/home/tomcat"):
            get(remote_path="deploy_create_new_pro.sh", local_path="/Users/micllo/Downloads/download_file")


def test_local_ssh():
    host_port = 22
    machine_ip = "localhost"
    host_user = "micllo"
    host_pwd = "abc123"
    with settings(host_string="%s@%s:%s" % (host_user, machine_ip, host_port), password=host_pwd):
        run("ls", warn_only=True)
        run("pwd", warn_only=True)


if __name__ == '__main__':
    # test_setting()
    # test_local_put_get()
    test_local_ssh()
