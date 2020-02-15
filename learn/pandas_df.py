# coding:UTF-8
import pandas as pd
import numpy as np

if __name__ == '__main__':

    # res = np.random.randn(6, 4)
    # print type(res)
    # print res

    # df = pd.DataFrame(np.random.randn(6, 4), columns=["A", "B", "C", "D"])
    df = pd.DataFrame(columns=["B"])
    df.loc[0, "B"] = "0"
    df.loc[1, "B"] = "1"
    df.loc[2, "B"] = "2"
    df.loc[3, "B"] = "3"

    # 解决print换行问题
    # pd.set_option('display.height', 1000)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 500)

    # print df
    # print df.count()
    # print type(df.count())
    # print df.count().to_dict()

    # 统计"B"列数量
    cnt = df.count().to_dict().get("B")
    print cnt
    print "\n"
    print df
    print "\n"

    # 根据"B"列是否满足某些条件，来新增"A"列
    df["A"] = df["B"].map(lambda x: x in ["1", "2", "3", "4"])
    print df
    print "\n"

    # 转成字典
    df_list = df.to_dict()
    print df_list
    print "\n"

    # 筛选出满足条件的"B"列，并转成list
    # print df[df["B"].map(lambda x: x in ["1", "2", "3", "4"])]["B"].tolist()
    print "\n"

    # reset_index(drop=True)
    # drop=True：在原有的索引列重置索引，不再另外添加新列
    # drop=False：原有的索引不变添加列名index，同时在新列上重置索引
    select_df = df[df["B"].map(lambda x: x in ["1", "2", "3", "4"])].reset_index(drop=True)
    print select_df
    print "\n"

    error_info = str(select_df)
    print error_info
    print "\n"

    # abc = df["B"].map(lambda x: x in ["1", "2", "3", "4"])
    # print abc