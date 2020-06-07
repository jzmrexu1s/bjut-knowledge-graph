import jieba
import numpy as np
import pandas as pd
import sys

# sys.stdout = open('recode.log', mode='w', encoding='utf-8')


jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持
strs = ["我来到北京清华大学","乒乓球拍卖完了","中国科学技术大学"]
# for str in strs:
#     seg_list = jieba.cut(str,use_paddle=True) # 使用paddle模式
#     print("Paddle Mode: " + '/'.join(list(seg_list)))
#

#
seg_list = jieba.cut("巴克莱集团和法国巴黎银行打算收购雷曼兄弟印度资产－报导", cut_all=False)
print("Default Mode: " + " ".join(seg_list))  # 精确模式
#
# seg_list = jieba.cut("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 默认是精确模式
# print(", ".join(seg_list))
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print(", ".join(seg_list))

# data = pd.read_excel("数据.xls", usecols=[1])
#
# train_data = np.array(data)
# train_x_list=train_data.tolist()
#
# for a in train_x_list:
#     b=str(a)
#     seg_list = jieba.cut(b, cut_all=False)
#     c=" ".join(seg_list)
#     print(c[6:-4])