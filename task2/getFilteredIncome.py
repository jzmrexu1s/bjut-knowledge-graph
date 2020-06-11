import pandas as pd
import numpy as np

FROM_POS = "data/chinese_only.csv"

if __name__ == "__main__":
    df = pd.read_csv(FROM_POS)
    df_income = pd.DataFrame(columns=('Public company', 'Type', 'Income', 'Year'))

    for i in range(len(df)):
        ts = df.iloc[i, 1]
        sp_type = ts.find('半年收入') - 1
        sp_company = 0
        sp_income_end = ts.find('元')
        num_detected = False
        j = sp_income_end
        while j >= 0:
            if not ts[j].isnumeric() and ts[j] is not '.' and num_detected:
                break
            if ts[j].isnumeric():
                num_detected = True
            j -= 1
        sp_income = j + 1
        if sp_type != -2 and sp_income != -1:
            public_company = ts[sp_company: sp_type]
            typ = ts[sp_type: sp_type + 5]
            income = ts[sp_income: sp_income_end + 1]
            sp_year_end = df.iloc[i, 2].find('-')
            year = df.iloc[i, 2][:sp_year_end]
            if public_company.find('更正') != -1:
                public_company = public_company[public_company.find("更正") + 2:]
            if len(income) > 0:
                df_income = df_income.append({
                    'Public company': public_company.replace(' ', '').replace('∶', '').replace('*', '').replace('：', ''),
                    'Type': typ.replace(' ', ''),
                    'Income': income.replace(' ', ''),
                    'Year': year.replace(' ', '')}, ignore_index=True)

    df_income.to_csv("output/income_separated.csv")

