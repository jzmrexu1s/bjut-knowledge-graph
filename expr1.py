# encoding=utf-8
import numpy as np
from getChineseData import has_chinese
import jieba.posseg as peg
import sys

VECTORS_POS = 'data/vectors.txt'
DOC_POS = 'data/extracted.txt'
IGNORED = ["和", "的"]
THRESHOLD = 0.70


def checkType(s1, s2):
    # if s1 == 'n' and s2 == 'n':
    #     return True
    # if s1 == 'v' and s2 == 'n':
    #     return True
    return True


def checkContent(s1, s2):
    if len(s1) == 1 or len(s2) == 1:
        return False
    return True


def cosine_distance(matrix1, matrix2):
    matrix1_matrix2 = np.dot(matrix1, matrix2.transpose())
    matrix1_norm = np.sqrt(np.multiply(matrix1, matrix1).sum(axis=1))
    matrix1_norm = matrix1_norm[:, np.newaxis]
    matrix2_norm = np.sqrt(np.multiply(matrix2, matrix2).sum(axis=1))
    matrix2_norm = matrix2_norm[:, np.newaxis]
    cosine_distance = np.divide(matrix1_matrix2, np.dot(matrix1_norm, matrix2_norm.transpose()))
    return cosine_distance

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

        groups = peg.cut(line)

        processed = []
        for word, flag in groups:
            if word != ' ':
                processed.append([word, flag])

        not_separate = []

        for a in range(len(processed) - 1):
            if processed[a][0] in dic.keys() and processed[a + 1][0] in dic.keys() and len(processed[a][0]) > 1:
                if checkContent(processed[a][0], processed[a + 1][0]) and checkType(processed[a][1], processed[a + 1][1]):
                    matrix1 = np.array([list(map(float, dic[processed[a][0]]))])
                    matrix2 = np.array([list(map(float, dic[processed[a + 1][0]]))])
                    c = cosine_distance(matrix1, matrix2)
                    if c >= THRESHOLD:
                        not_separate.append(a)

        st = ''

        for a in range(len(processed)):
            st = st + processed[a][0]
            if a not in not_separate:
                st = st + ' '
            else:
                # st = st + '-'
                st = st + '(' + processed[a][1] + '/' + processed[a+1][1] + ')-'
        print(st)
    fr.close()
