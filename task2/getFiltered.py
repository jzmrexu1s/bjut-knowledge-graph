import pandas as pd
import numpy as np
import jieba

FROM_POS = "data/chinese_only.csv"
SYM = "~!@#$%^&*()_+-*/<>,[]\/"


def check_in(words, sentence):
    for word in words:
        if word not in sentence:
            return False
    return True


def check_not_in(words, sentence):
    for word in words:
        if word in sentence:
            return False
    return True


def cast_sp_assert(sp_assert_origin):
    operation = 'UNDEFINED'
    if '定为' in sp_assert_origin:
        operation = '定为'
    if '首次定为' in sp_assert_origin:
        operation = '首次定为'
    if '维持' in sp_assert_origin:
        operation = '维持在'
    return operation


def separate(rule_pre, rule_type, rule_assert, rule_from, rule_connect, s, d):
    sp_pre = s.find(rule_pre[0])
    sp_type = None
    for rule in rule_type:
        if s.find(rule) != -1:
            sp_type = s.find(rule)
            break
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
        operation = cast_sp_assert(sp_assert_origin)
    if sp_assert or (sp_connect and sp_from):
        before_val = s[sp_assert + len(sp_assert_origin):] if sp_assert else s[sp_from + len(rule_from[0]): sp_connect]
        if before_val:
            if not before_val[0].isnumeric() and '目标价' in rule_type:
                before_val = ''
        after_val = s[sp_assert + len(sp_assert_origin):] if sp_assert else s[sp_connect + len(sp_connect_origin):]
        for c in after_val:
            if c in SYM:
                after_val = after_val[:after_val.find(c)]
                break
        date = str(d)
        return {'Finance company': finance_company.replace(' ', ''),
                'Public company': public_company.replace(' ', ''),
                'Before': before_val.replace(' ', ''),
                'Operation': operation.replace(' ', ''),
                'After': after_val.replace(' ', ''),
                'Date': date.replace(' ', '')}
    return None


if __name__ == "__main__":
    df = pd.read_csv(FROM_POS)
    df_rate = pd.DataFrame(columns=('Finance company', 'Public company', 'Before', 'Operation', 'After', 'Date'))
    df_price = pd.DataFrame(columns=('Finance company', 'Public company', 'Before', 'Operation', 'After', 'Date'))
    rule_connect = ['上升至', '上升到', '上调至', '上调到', '下调至', '下调到', '上调为', '下调为']
    rule_pre = ['将']
    rule_from = ['从', '由']

    for i in range(len(df)):
        ts = df.iloc[i, 1]
        s = ts
        p0 = s.find('* ')
        if p0 != -1:
            s = s[p0 + 2:]
        p1 = s.find('>')
        if p1 != -1:
            s = s[:p1]
        if check_in(["评级", "将"], s) and check_not_in(["目标价"], s):
            df_rate = df_rate.append(separate(rule_pre, ['的评级', '评级'],
                                              ['首次评级定为', '初始评级定为', '评级定为', '维持在'],
                                              rule_from,
                                              rule_connect, s, df.iloc[i, 2]), ignore_index=True)
        elif check_in(["目标价", "将"], s) and check_not_in(["评级"], s):
            df_price = df_price.append(separate(rule_pre, ['的目标价', '目标价'],
                                                ['首次目标价定为', '初始目标价定为', '目标价定为', '维持在'],
                                                rule_from,
                                              rule_connect, s, df.iloc[i, 2]), ignore_index=True)

    df_rate.to_csv("output/rate_separated.csv")
    df_price.to_csv("output/price_separated.csv")
