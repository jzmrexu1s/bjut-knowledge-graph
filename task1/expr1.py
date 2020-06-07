# encoding=utf-8
import numpy as np
import jieba.posseg as peg

VECTORS_POS = 'data/vectors_task2.txt'
DOC_POS = 'data/test.txt'
OUTPUT_POS = 'output/task2_result.txt'
IGNORED = ["和", "的", "月份", "亿美元", "部分", "预计"]
THRESHOLD = 0.55
EXTENDED_NOUN = ["n", "nr", "nz", "PER", "f", "ns", "LOC", "s", "nt", "ORG", "nw", "TIME"]
NOT_ALLOWED = ["v", "d"]


def checkProp(wordList):
    if wordList[-1][1] not in EXTENDED_NOUN:
        return False
    for word in wordList:
        if word[1] in NOT_ALLOWED:
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
        if v[0] not in IGNORED:
            dic[v[0]] = v[1:]
    fr.close()

    fr = open(DOC_POS, 'r', encoding='utf-8')
    f = open(OUTPUT_POS, 'w+', encoding='utf-8')
    result = ''
    count = 0

    for line in fr:
        if count > 99999:
            break
        groups = peg.cut(line)

        processed = []
        for word, flag in groups:
            if word != ' ':
                processed.append([word, flag])

        not_separate = []

        i = 0
        tmpIdxs = []

        finish_step = False
        while i < len(processed) - 1:
            if processed[i][0] in dic.keys() and processed[i + 1][0] in dic.keys() and len(processed[i][0]) > 1 and len(
                    processed[i + 1][0]) > 1:
                matrix1 = np.array([list(map(float, dic[processed[i][0]]))])
                matrix2 = np.array([list(map(float, dic[processed[i + 1][0]]))])
                c = cosine_distance(matrix1, matrix2)
                if c >= THRESHOLD:
                    tmpIdxs.append(i)
                else:
                    finish_step = True
            else:
                finish_step = True

            if finish_step and len(tmpIdxs):
                tmpIdxs.append(tmpIdxs[-1] + 1)
                tmpLen = len(tmpIdxs)
                while tmpLen >= 2:
                    j = 0
                    while j <= len(tmpIdxs) - tmpLen:
                        if checkProp(list(map(lambda x: processed[x], tmpIdxs[j:j + tmpLen]))):
                            not_separate.extend(tmpIdxs[j:j + tmpLen - 1])
                        j += 1
                    tmpLen -= 1
                tmpIdxs = []
            i += 1

        for a in range(len(processed)):
            result = result + processed[a][0]
            if a not in not_separate:
                result = result + ' '
                # result = result + '(' + processed[a][1] + ") "
            else:
                result = result + '-'
                # print('(' + processed[a][1] + '/' + processed[a+1][1] + ')-')
                # result = result + '(' + processed[a][1] + '/' + processed[a + 1][1] + ')-'
        count += 1

    f.write(result)
    fr.close()
    f.close()
