import pandas as pd
import numpy as np

data = pd.read_excel("data/实验1数据.xls", usecols=[1])

train_data = np.array(data)
train_x_list = train_data.tolist()

print(train_x_list)

f = open("data/extracted.txt", "w+")
for line in train_x_list:
    f.write("\n")
    f.write(line[0])
