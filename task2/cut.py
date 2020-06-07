import pandas as pd
import numpy as np
import jieba

FROM_POS = "data/chinese_only.csv"
TO_POS = "output/task2_cut.txt"

if __name__ == "__main__":
    data = pd.read_csv(FROM_POS, usecols=[1])

    train_data = np.array(data)
    train_x_list = train_data.tolist()

    f = open(TO_POS, 'w+', encoding="utf-8")

    s = ""

    for a in train_x_list:
        b = str(a)
        seg_list = jieba.cut(b, cut_all=False)
        s += " ".join(seg_list)[4:-4]
        s += "\n"

    f.write(s)
    f.close()
