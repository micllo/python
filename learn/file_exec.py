# coding:UTF-8
import os

if __name__ == '__main__':

    file_path = "/Users/micllo/Downloads/requirement.txt"
    fo = open(file_path, "r+")
    content = fo.read()
    print content
    print type(content)
    fo.close()