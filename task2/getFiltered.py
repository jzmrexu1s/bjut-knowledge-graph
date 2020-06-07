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


def separate(rule_pre, rule_type, rule_assert, rule_from, rule_connect, s, d):
    sp_pre = s.find(rule_pre[0])
    sp_type = s.find(rule_type[0])
    sp_assert = None
    sp_assert_origin = None
    for rule in rule_assert:
        if s.find(rule) != -1:
            sp_assert = s.find(rule)
            sp_assert_origin = rule
            break
    sp_from = None
    sp_connect = None
    sp_connect_origin = None
    if not sp_assert:
        sp_from = s.find(rule_from[0])
        for rule in rule_connect:
            if s.find(rule) != -1:
                sp_connect = s.find(rule)
                sp_connect_origin = rule
                break
    finance_company = s[:sp_pre]
    public_company = s[sp_pre + len(rule_pre[0]): sp_type]
    operation = None
    if sp_connect:
        operation = sp_connect_origin[:-1]
    elif sp_assert:
        if '定为' in sp_assert_origin:
            operation = '定为'
        if '首次定为' in sp_assert_origin:
            operation = '首次定为'
        if '维持' in sp_assert_origin:
            operation = '维持在'
    if sp_assert or (sp_connect and sp_from):
        before_val = s[sp_assert + len(sp_assert_origin):] if sp_assert else s[sp_from + len(rule_from[0]): sp_connect]
        after_val = s[sp_assert + len(sp_assert_origin):] if sp_assert else s[sp_connect + len(sp_connect_origin):]
        date = str(d)
        return {'Finance company': finance_company,
                'Public company': public_company,
                'Before': before_val,
                'Operation': operation,
                'After': after_val,
                'Date': date}
    return {}


def separate_rate(s, d):
    sp0 = s.find('将')
    sp1 = s.find('评级')
    sp2 = s.find('维持在')
    sp3 = s.find('从')
    sp4 = s.find('上调至')
    sp5 = s.find('下调至')
    sp6 = s.find('首次评级定为')
    sp7 = s.find('初始评级定为')
    sp8 = s.find('评级定为')
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
    elif sp8 != -1:
        ar = s[sp8 + 4:]
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
    sp8 = s.find('目标价位')
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
    print(
        {'Finance company': fc,
         'Public company': pc,
         'Before price': br,
         'Operation': op,
         'After price': ar,
         'Date': str(d)}
    )
    return {'Finance company': fc,
            'Public company': pc,
            'Before price': br,
            'Operation': op,
            'After price': ar,
            'Date': str(d)}


if __name__ == "__main__":
    df = pd.read_csv(FROM_POS)
    df_rate = pd.DataFrame(columns=('Finance company', 'Public company', 'Before', 'Operation', 'After', 'Date'))
    df_price = pd.DataFrame(columns=('Finance company', 'Public company', 'Before', 'Operation', 'After', 'Date'))
    rule_connect = ['上升至', '上升到', '上调至', '上调到', '下调至', '下调到', '上调为', '下调为']

    for i in range(30000, 35000):
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
            df_rate = df_rate.append(separate(['将'], ['评级'], ['首次评级定为', '初始评级定为', '评级定为', '维持在'], ['从'],
                                              rule_connect, s, df.iloc[i, 2]), ignore_index=True)
        elif checkIn(["目标价", "将"], s) and checkNotIn(["评级"], s):
            df_price = df_price.append(separate(['将'], ['目标价'], ['首次目标价定为', '初始目标价定为', '目标价定为', '维持在'], ['从'],
                                              rule_connect, s, df.iloc[i, 2]), ignore_index=True)

    df_rate.to_csv("output/rate_separated.csv")
    df_price.to_csv("output/price_separated.csv")
