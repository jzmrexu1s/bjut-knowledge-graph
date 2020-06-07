import pandas as pd
import numpy as np
import jieba

FROM_POS = "data/chinese_only.csv"
TO_POS = "output/price_only.csv"
WORDS = ["目标价", "将"]


def checkIn(words, sentence):
    for word in words:
        if word not in sentence:
            return False
    return True


if __name__ == "__main__":
    df = pd.read_csv(FROM_POS)
    df_filtered = pd.DataFrame(columns=('content', 'date'))

    for i in range(len(df)):
        ts = df.iloc[i, 1]
        if checkIn(WORDS, ts):
            df_filtered = df_filtered.append([{'content': ts, 'date': df.iloc[i, 2]}], ignore_index=True)

    df_filtered.to_csv(TO_POS)
