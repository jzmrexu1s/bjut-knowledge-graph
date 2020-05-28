from getChineseData import has_chinese

f = open("output/task1_result.txt", "r", encoding='utf-8')
maxLen = 0
for line in f:
    v = line.strip().split(' ')
    for word in v:
        t = word.replace('-', '')
        if has_chinese(t):
            maxLen = max(maxLen, len(t))
print(maxLen)
f.close()
f = open("output/task1_result.txt", "r", encoding='utf-8')
for line in f:
    v = line.strip().split(' ')
    for word in v:
        t = word.replace('-', '')
        if has_chinese(t) and len(t) == maxLen:
            print("word:", word)
f.close()
