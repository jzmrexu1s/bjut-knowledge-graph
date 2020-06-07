import pandas as pd
import numpy as np
import jieba

FROM_POS = "data/chinese_only.csv"


def checkIn(words, sentence):
    for word in words:
        if word not in sentence:
            return False
    return True


def checkNotIn(words, sentence):
    for word in words:
        if word in sentence:
            return False
    return True


def separate_rate(s, d):
    sp0 = s.find('将')
    sp1 = s.find('评级')
    sp2 = s.find('维持在')
    sp3 = s.find('从')
    sp4 = s.find('上调至')
    sp5 = s.find('下调至')
    sp6 = s.find('首次评级定为')
    sp7 = s.find('初始评级定为')
    fc = s[0:sp0]
    pc = ''
    if sp6 != -1:
        pc = s[sp0 + 1:sp6]
    elif sp7 != -1:
        pc = s[sp0 + 1:sp7]
    else:
        pc = s[sp0 + 1:sp1]
    br = ''
    ar = ''
    op = ''
    if sp2 != -1:
        br = s[sp2 + 3:]
        ar = br
        op = '维持'
    elif sp4 != -1:
        br = s[sp3 + 1: sp4]
        ar = s[sp4 + 3:]
        op = '上调'
    elif sp5 != -1:
        br = s[sp3 + 1: sp5]
        ar = s[sp5 + 3:]
        op = '下调'
    elif sp6 != -1:
        ar = s[sp6 + 6:]
        op = '评级'
    elif sp7 != -1:
        ar = s[sp7 + 6:]
        op = '评级'

    return {'Finance company': fc,
            'Public company': pc,
            'Before rate': br,
            'Operation': op,
            'After rate': ar,
            'Date': str(d)}


def separate_price(s, d):
    sp0 = s.find('将')
    sp1 = s.find('目标价')
    sp2 = s.find('维持在')
    sp3 = s.find('从')
    sp4 = s.find('上调至')
    sp5 = s.find('下调至')
    sp6 = s.find('首次目标价定为')
    sp7 = s.find('目标价定为')
    fc = s[0:sp0]
    pc = ''
    if sp6 != -1:
        pc = s[sp0 + 1:sp6]
    elif sp7 != -1:
        pc = s[sp0 + 1:sp7]
    else:
        pc = s[sp0 + 1:sp1]
    br = ''
    ar = ''
    op = ''
    if sp2 != -1:
        br = s[sp2 + 3:]
        ar = br
        op = '维持'
    elif sp4 != -1:
        br = s[sp3 + 1: sp4]
        ar = s[sp4 + 3:]
        op = '上调'
    elif sp5 != -1:
        br = s[sp3 + 1: sp5]
        ar = s[sp5 + 3:]
        op = '下调'
    elif sp6 != -1:
        ar = s[sp6 + 6:]
        op = '定为'
    elif sp7 != -1:
        ar = s[sp7 + 6:]
        op = '定为'

    return {'Finance company': fc,
            'Public company': pc,
            'Before price': br,
            'Operation': op,
            'After price': ar,
            'Date': str(d)}


if __name__ == "__main__":
    df = pd.read_csv(FROM_POS)
    df_rate = pd.DataFrame(columns=('Finance company', 'Public company', 'Before rate', 'Operation', 'After rate', 'Date'))
    df_price = pd.DataFrame(columns=('Finance company', 'Public company', 'Before price', 'Operation', 'After price', 'Date'))

    for i in range(len(df)):
    # for i in range(1000):
        ts = df.iloc[i, 1]
        s = ts
        p0 = s.find('* ')
        if p0 != -1:
            s = s[p0 + 2:]
        p1 = s.find('>')
        if p1 != -1:
            s = s[:p1]
        if checkIn(["评级", "将"], s) and checkNotIn(["目标价"], s):
            df_rate = df_rate.append([separate_rate(s, df.iloc[i, 2])], ignore_index=True)
        elif checkIn(["目标价", "将"], s) and checkNotIn(["评级"], s):
            df_price = df_price.append([separate_price(s, df.iloc[i, 2])], ignore_index=True)

    df_rate.to_csv("output/rate_separated.csv")
    df_price.to_csv("output/price_separated.csv")
