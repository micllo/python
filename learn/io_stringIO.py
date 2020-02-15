import datetime
import io, sys


class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()


stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)


if __name__ == "__main__":

    # 【 用 法 一 】
    # 实例化一个'IO流对象'
    outputBuffer = io.StringIO()
    # 'IO流对象'调用'write'方法 写入一些字符串 作为缓存
    outputBuffer.write('Hello World\n')
    # 打印一些内容并保存入'IO流对象'
    print('this is a test\n', file=outputBuffer)
    # 取出'IO流对象'中写入的值
    print(outputBuffer.getvalue())

    # 【 用 法 二 】
    outputBuffer = io.StringIO('Hello\nWorld\n')
    # 先取出前4个字符
    print(outputBuffer.read(4))
    # 再取出剩余的字符
    print(outputBuffer.read())

    # 【 用 法 三 】
    temp = sys.stdout
    stdout_redirector.fp = io.StringIO()
    sys.stdout = stdout_redirector
    print("\n要输出的字符串被保存在了StringIO内存中")
    print("====================")
    sys.stdout = temp
    print("++++++ 标准输出 指向了原来的sys.stdout ++++++++")
    print(stdout_redirector.fp.getvalue())
