import pandas as pd
import numpy as np


def has_chinese(s):
    if type(s) != str:
        print(s)
        return False
    for ch in s:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False


def to_chinese_only():
    # 读取csv
    df = pd.read_csv('../task1/data/data.csv', header=None)
    print(df.head())

    # 提取中文条目
    english_only = []
    for index, row in df.iterrows():
        if not has_chinese(row[1]):
            english_only.append(index)

    df = df.drop(labels=english_only)
    df[[1, 2]].to_csv('data/chinese_only.csv')


if __name__ == '__main__':
    to_chinese_only()
