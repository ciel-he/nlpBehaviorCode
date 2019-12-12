# 从用户词典，构建正则匹配表达式
def loadFilterKeyWords(filepath):
    filter_words = []
    # 输入是文件时
    if isinstance(filepath, str):
        with open(filepath, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
            while line:
                if not len(line) or line.startswith('#'):
                    print('过滤用户定义词典：',line)
                    line = file.readline().strip()
                    continue
                filter_words.append(line)
                line = file.readline().strip()

    # 输入是list数组时
    if isinstance(filepath, list):
        filter_words = filepath.copy()

    comstr = '(?:'
    for word in filter_words:
        comstr += word + '|'
        # comstr += '|'
    # 去掉最后一个|
    comstr = comstr[:-1]
    comstr += ')'
    return  comstr