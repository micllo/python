import subprocess
import sys

"""
    通过 sys.path.append() 配置环境变量
"""
sys.path.append("/Users/micllo/Documents/tools/apache-maven-3.2.5")
subprocess.call("mvn -v", shell=True)


"""
   【 执行 cmd 命令 】
    Popen()、 call()、check_output() 区别：
    
    Popen(): 异步执行, 返回 subprocess.Popen 对象
    call():  同步执行(阻塞)，返回结果代码(0表示执行成功)，< 执行内容默认输出stdout >
    check_output(): 同步执行(阻塞)，返回执行结果（bytes类型）
"""

# subprocess.Popen("sleep 5", shell=True)
# res = subprocess.Popen("ls -la", shell=True)
# print("----")
# print(res)

# subprocess.call("sleep 5", shell=True)
# res_code = subprocess.call("pwd", shell=True)
# print(res_code)


# subprocess.check_output(["sleep", "5"])
# bytes_res = subprocess.check_output(["ls", "-la"])
# print(bytes_res)
# print(type(bytes_res))