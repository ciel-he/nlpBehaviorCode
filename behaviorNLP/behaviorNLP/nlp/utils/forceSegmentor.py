# -*- coding: utf-8 -*-
import re
class ForceSegmentor(object):
    def __init__(self):
        self.forcelist = []

    def load(self, filepath):

        # 输入是文件时
        if isinstance(filepath, str):
            with open(filepath, 'r',encoding='utf-8') as file:
                line = file.readline()
                while line:
                    if ('#' in line):
                        line = file.readline().strip()
                        continue
                    self.forcelist.append(ForceSegmentorItem(line))
                    line = file.readline()
        # 输入是list数组时
        if isinstance(filepath, list):
            for item in filepath:
                self.forcelist.append(ForceSegmentorItem(item))

        self.compileStr = ''
        # print(len(self.forcelist),'用户字典')
        xlen = len(self.forcelist)
        comstr = '(?:'
        for x in range(xlen):
            comstr += self.forcelist[x].get_text()
            comstr += '|'
        # 去掉最后一个|
        comstr = comstr[:-1]
        comstr += ')'
        self.compileStr = re.compile(comstr)


    def find_in_dict(self,sentence):
        arr = []
        result=self.compileStr.findall(sentence)
        if result:
            #找到句子中包含的字典中的词,返回一个列表,这里会有个空字符串
            for s in set(result):
                if s != '' :
                    arr.append(s)
            return arr
        return None
    
    def merge(self, sentence, words):
        # 有些词无法通过自定义分词词典直接正确划分，用该方法将属于强制词典的多个词合并

        result = words
        midd_res = words
        wordList = self.find_in_dict(sentence)
        # print('需合并词包括：', wordList)
        if not wordList :
            return result
        for found_word in wordList:
            # 可能同一个词在这句话里出现多次
            indexs_start = []
            # 合并的词首尾距离
            index_distance = 0
            index_start = -1
            strm = ''
            for i, word in enumerate(midd_res):
                wl = len(word)
                if (index_start == -1 and word == found_word[0:wl]):
                    index_start = i
                    strm += word
                elif (index_start != -1):
                    strm += word
                    if (strm == found_word):
                        # 已经完全匹配

                        index_distance = i - index_start + 1
                        indexs_start.append(index_start)

                        index_start = -1
                        strm = ''
                    elif (strm not in found_word):
                        # 现在连接得到的多个词是错误的，重新开始匹配
                        index_start = -1
                        strm = ''
            result = []
            i = 0
            # print(indexs_start, index_distance)
            while (i < len(midd_res)):

                if (i in indexs_start):
                    result.append(found_word)
                    i += index_distance
                else:
                    result.append(midd_res[i])
                    i += 1
            # 保存此次合并的结果，用于接下来的合并
            midd_res = result

        return result

class ForceSegmentorItem(object):
    def __init__(self, line):
        self.text = line.replace('\n', '')

    def get_text(self):
        return self.text
