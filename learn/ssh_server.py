# -*- coding: utf-8 -*-
import requests
import pymongo
import traceback
import re
import pandas as pd
import paramiko
import time


def ssh_server_exec_cmd(hostname, port, username, password, command):
    # 通过SSH链接服务器
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, port=port, username=username, password=password)
    std_in, std_out, std_err = ssh_client.exec_command(command)
    pid_list = [line.strip("\n") for line in std_out]
    ssh_client.close()
    return pid_list


def get_server_pid_list(hostname):
    port = 22
    username = "centos"
    command = "ps aux | grep uwsgi"
    cmd_res_list = []
    pid_list = []
    access_server = True
    # 登陆服务器获取相应信息
    try:
        password = "centosps2016"
        cmd_res_list = ssh_server_exec_cmd(hostname, port, username, password, command)
    except Exception, e:
        print e
        print traceback.format_exc()
        if "Authentication failed" in str(e):
            try:
                password = "centospshl2016"
                cmd_res_list = ssh_server_exec_cmd(hostname, port, username, password, command)
            except Exception, e:
                access_server = False
                print e
                print traceback.format_exc()
        else:
            access_server = False
    # 解析信息，获取pid列表
    if access_server:
        for line in cmd_res_list:
            if "bash -c ps aux | grep uwsgi" not in line and "grep uwsgi" not in line:
                # 过滤列表中的 空字符 和 None
                line_list = list(filter(None, line.split(" ")))
                pid_list.append(line_list[1])
    return access_server, pid_list


def kill_pid(hostname, pid_list):
    port = 22
    username = "centos"
    for pid in pid_list:
        try:
            password = "centosps2016"
            ssh_server_exec_cmd(hostname, port, username, password, "kill -9 " + pid)
        except Exception, e:
            if "Authentication failed" in str(e):
                password = "centospshl2016"
                ssh_server_exec_cmd(hostname, port, username, password, "kill -9 " + pid)


def test():
    """
    连接服务器，执行多个命令
    :return:
    """
    # 实例化一个transport对象
    trans = paramiko.Transport(('192.168.23.84', 22))
    # 建立连接
    trans.connect(username='centos', password='centosps2016')
    # 将sshclient的对象的transport指定为以上的trans
    ssh = paramiko.SSHClient()
    ssh._transport = trans
    # 执行多个命令
    stdin1, stdout1, stderr1 = ssh.exec_command('pwd')
    print(stdout1.read())
    print "_______________________________"
    stdin2, stdout2, stderr2 = ssh.exec_command('df -h')
    print(stdout2.read())
    print "_______________________________"

    # 关闭连接
    trans.close()


if __name__ == "__main__":
    # hostname = "192.168.23.84"
    # access_server, pid_list = get_server_pid_list(hostname)
    # print access_server
    test()










