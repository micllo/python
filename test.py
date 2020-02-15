import datetime
import io, sys

if __name__ == "__main__":

    STATUS = {0: '通过', 1: '失败', 2: '错误'}
    n = 0
    tid = (n == 0 and "p" or (n == 1 and "f" or "e")) + "t1_1"
    print(tid)

