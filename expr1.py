# encoding=utf-8
import numpy as np
from getChineseData import has_chinese
import jieba
import sys


def cosine_distance(matrix1, matrix2):
    matrix1_matrix2 = np.dot(matrix1, matrix2.transpose())
    matrix1_norm = np.sqrt(np.multiply(matrix1, matrix1).sum(axis=1))
    matrix1_norm = matrix1_norm[:, np.newaxis]
    matrix2_norm = np.sqrt(np.multiply(matrix2, matrix2).sum(axis=1))
    matrix2_norm = matrix2_norm[:, np.newaxis]
    cosine_distance = np.divide(matrix1_matrix2, np.dot(matrix1_norm, matrix2_norm.transpose()))
    return cosine_distance


VECTORS_POS = 'data/vectors.txt'
DOC_POS = 'data/3.txt'
IGNORED = ["和"]
THRESHOLD = 0.8

if __name__ == "__main__":
    dic = {}
    fr = open(VECTORS_POS, 'r', encoding='utf-8')
    for line in fr:
        v = line.strip().split(' ')
        if has_chinese(v[0]) and v[0] not in IGNORED:
            dic[v[0]] = v[1:]
    fr.close()

    fr = open(DOC_POS, 'r', encoding='utf-8')
    for line in fr:
        v = " ".join(jieba.cut(line, cut_all=False)).strip().split(' ')
        not_separate = []

        for i in range(v.count('')):
            v.remove('')
        for a in range(len(v) - 1):
            if v[a] in dic.keys() and v[a + 1] in dic.keys():
                matrix1 = np.array([list(map(float, dic[v[a]]))])
                matrix2 = np.array([list(map(float, dic[v[a + 1]]))])
                c = cosine_distance(matrix1, matrix2)
                if c >= THRESHOLD:
                    not_separate.append(a)

        st = ''
        for a in range(len(v)):
            st = st + v[a]
            if a not in not_separate:
                st = st + ' '

        print(st)
    fr.close()
