import pandas as pd
import numpy as np

FROM_POS0 = "output/rate_separated.csv"
FROM_POS1 = "output/price_separated.csv"
TO_POS0 = "output/financial_companies_no_repeat.csv"
TO_POS1 = "output/public_companies_no_repeat.csv"
TO_POS2 = "output/rate_replaced.csv"
TO_POS3 = "output/price_replaced.csv"

if __name__ == '__main__':
    df_rate = pd.read_csv(FROM_POS0)
    df_price = pd.read_csv(FROM_POS1)
    dic_fin_comp = dict()
    dic_pub_comp = dict()
    i_fin = 0
    i_pub = 0

    for i in range(len(df_rate)):
        k = df_rate.iloc[i, 1]
        if k not in dic_fin_comp.keys():
            dic_fin_comp[k] = i_fin
            i_fin += 1
        k = df_rate.iloc[i, 2]
        if k not in dic_pub_comp.keys():
            dic_pub_comp[k] = i_pub
            i_pub += 1

    for i in range(len(df_price)):
        k = df_price.iloc[i, 1]
        if k not in dic_fin_comp.keys():
            dic_fin_comp[k] = i_fin
            i_fin += 1
        k = df_price.iloc[i, 2]
        if k not in dic_pub_comp.keys():
            dic_pub_comp[k] = i_pub
            i_pub += 1

    fin_comp = list(dic_fin_comp.keys())
    df_fin_comp = pd.DataFrame(np.array(fin_comp).reshape(len(fin_comp), 1), columns=['Finance company'])
    df_fin_comp.to_csv(TO_POS0)

    pub_comp = list(dic_pub_comp.keys())
    df_pub_comp = pd.DataFrame(np.array(pub_comp).reshape(len(pub_comp), 1), columns=['Public company'])
    df_pub_comp.to_csv(TO_POS1)

    for i in range(len(df_rate)):
        df_rate.iloc[i, 1] = dic_fin_comp[df_rate.iloc[i, 1]]
        df_rate.iloc[i, 2] = dic_pub_comp[df_rate.iloc[i, 2]]

    for i in range(len(df_price)):
        df_price.iloc[i, 1] = dic_fin_comp[df_price.iloc[i, 1]]
        df_price.iloc[i, 2] = dic_pub_comp[df_price.iloc[i, 2]]

    df_rate.to_csv(TO_POS2, index=False)
    df_price.to_csv(TO_POS3, index=False)
