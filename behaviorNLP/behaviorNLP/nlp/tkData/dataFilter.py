#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-06-06 16:36:08
# @Author  : heye (heye1109@qq.com)
# @Blog    : https://blog.csdn.net/HYeeee


from behaviorNLP.nlp.utils.getRegxFromText import loadFilterKeyWords
from behaviorNLP.nlp.utils.concatTxt import concatTxt
import re
import json
import os

# 答案对照
result_tk = {
    "1": "A",  # 或者正确
    "2": "B",  # 或者错误
    "3": "C",
    "4": "D",
    "7": "AB",
    "8": "AC",
    "9": "AD",
    "10": "BC",
    "11": "BD",
    "12": "CD",
    "13": "ABC",
    "14": "ABD",
    "15": "ACD",
    "16": "BCD",
    "17": "ABCD"
}


# 加载题库
def load(fileName):
    with open("./"+fileName + '.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


# 科目一选择题处理
def handleSelectK1Question(sentence):
    slen = len(sentence)
    # 答案插入需拼接
    searchRes = re.search('(?:怎样|如何)', sentence)
    if searchRes:
        res = list(searchRes.span())
        start = sentence.find('(', res[1])  # 找括号的位置
        if re.search('应', sentence[0:res[0]]):
            split_flag = ''
        else:
            split_flag = '，' # 这里，不要加“应”处理看看
        sentence = sentence[0:res[0]] + split_flag + sentence[start + 1:slen - 1]
        return sentence

    # 答案直接替换文字
    searchRes = re.search('(?:什么|多少|怎么办|怎么做|多远|哪条|以下哪种情况下)', sentence)
    if searchRes:
        res = list(searchRes.span())
        start = sentence.find('(', res[1])
        sentence = sentence[0:res[0]] + sentence[start + 1:slen - 1]
        return sentence

    # 处理这种情况 —— 写论文时可以通过print修改前后举例。
    # 行经下列哪种路段时不得超车？(交叉路口)
    # 行经交叉路口时不得超车
    searchRes = re.search(r'(有)?下列.*?[时|辆|段]', sentence)
    if searchRes:
        # print(sentence)
        res = list(searchRes.span())
        start = sentence.find('(', res[1])
        if sentence[res[1]] == '时':
            split_flag = ''
        else:
            split_flag = '时，'
        sentence = sentence[0:res[0]] + sentence[start + 1:slen - 1] + split_flag +sentence[res[1] :start-1]
        # print(sentence)
        return sentence

    return sentence

# 科目四选择题处理
def handleSelectK4Question(sentence):
    slen = len(sentence)
    # 答案插入需拼接
    # 以下关于驶离高速公路的做法正确的是什么？(提前开启右转向灯 驶入减速车道 按减速车道规定的时速行驶 ) --这句被过滤掉了前提：驶离高速公路
    # 但是下面还会有相关的问题，这里可以考虑忽略
    searchRes = re.search('(?:怎么办|怎么做|怎样|如何|(?:以下|下列).*?正确)', sentence)
    if searchRes:
        res = list(searchRes.span())
        start = sentence.find('(', res[1])  # 找括号的位置
        if re.search('(?:应|要|，)', sentence[res[0]-3:res[0]]):
            split_flag = ''
        else:
            split_flag = '，'  # 这里，不要加“应”处理看看
        sentence = sentence[0:res[0]] + split_flag + sentence[start + 1:slen - 1]
        return sentence

    # 错误答案处理 -在句子前面加不能，只有6条，先不考虑
    # searchRes = re.search(r'(以)?下.*?错误的是什么', sentence)
    # if searchRes:
    #     res = list(searchRes.span())
    #     start = sentence.find('(', res[1])
    #     sentence = sentence[0:res[0]] + '不能' + sentence[start + 1:slen - 1]
    #     return sentence

    # 处理：要采取的措施是（什么）？这一类问题
    searchRes = re.search(r'采取的.*?是', sentence)
    if searchRes:
        res = list(searchRes.span())
        start = sentence.find('(', res[1])
        sentence = sentence[0:res[0]]  + sentence[start + 1:slen - 1]
        return sentence

    # 答案直接替换文字
    searchRes = re.search('(?:什么地方|以下什么|什么灯|什么|多少|多远|哪条|哪些方面)', sentence)
    if searchRes:
        res = list(searchRes.span())
        start = sentence.find('(', res[1])
        sentence = sentence[0:res[0]]+sentence[start + 1:slen - 1] + sentence[res[1]:start-1]
        return sentence



    return sentence


def dataFilter(fileName, regStr, salt):
    # 加载题库
    data = load(fileName)
    res_list = data['result']
    new_file_Name = './'+salt+fileName+"Data.txt"
    # 先删除文件
    try:
        os.remove(new_file_Name)
    except IOError:
        print("Error: 删除文件失败")
    try:
        file = open(new_file_Name, "a", encoding='utf-8')  # a 方式，seek是无效的
    except IOError:
        print("Error: 没有找到文件或读取文件失败")

    judgment_question_true_list = []  # 判断题
    judgment_question_false_list = []  # 判断题

    for res in res_list:
        if res['url'] != '':
            # 去掉图片题
            pass
        else:
            # 答案匹配
            answer = ''
            for key in result_tk:
                if res['answer'] == key:
                    res_arr = result_tk[key]
                    break
            for index, item in enumerate(res_arr):
                if index == len(res_arr) - 1:
                    delimiter  = ''
                else:
                    delimiter = '，'
                if item == 'A':
                    answer += res['item1'] + delimiter if res['item1'] != '' else '正确'  # 注意这里的,必须要
                if item == 'B':
                    answer += res['item2'] + delimiter if res['item2'] != '' else '错误'
                if item == 'C':
                    answer += res['item3'] + delimiter
                if item == 'D':
                    answer += res['item4'] + delimiter

            question = res['question']
            explains = res['explains']

            # 去掉-交通法扣分题
            if re.search('\d分', answer) or re.search('\d分', question):
                continue

            # 写入数据拼接 ，注意这里后面的空格必须要
            if answer == "正确"  or answer == "对":
                write_data = question
            elif answer == "错误"  or answer == "错":
                write_data = question + '(错误)'
                # write_data = question + '(错误,' + explains + ')'
            else:
                write_data = question + '(' + answer + ')'

            # 去掉法律相关条款等：通过关键字匹配
            pattern = re.compile(regStr)
            if not pattern.search(write_data):
                # 把驾驶机动车5个字去掉，语句意思不变，但对角色标注有好处
                # 这个放在最前面，是因为选择题和判断题中都去掉
                searchRes = re.search('驾驶机动车', write_data)
                if searchRes:
                    res = list(searchRes.span())
                    write_data = write_data[0:res[0]] + write_data[res[1]:]
                if '是因为' in write_data:
                    continue
                if re.search('(?:\?|？)', write_data):
                    # 选择题的处理
                    if fileName == 'k1' :
                        handleTxt = handleSelectK1Question(write_data)
                    else:
                        handleTxt = handleSelectK4Question(write_data)
                        if handleTxt.startswith('，'):
                            print('这句处理错误，舍弃：',write_data)
                            continue
                    # file.write(write_data + '\n') #原句-对照看处理结果
                    # 去掉依然含有？的句子
                    searchRes = re.search('[?|？]', handleTxt)
                    if searchRes:
                        continue
                    # 去掉 ‘主路车流量大、速度快’ 这一句，没有意义
                    if '主路车流量大、速度快' in handleTxt:
                        continue
                    # 去掉“应当，开启转向灯观察主路情况确保安全汇入车流”
                    if handleTxt.startswith('应当'):
                        continue

                    if '路面无障碍物，道路宽直' in handleTxt :
                        continue
                    # 去掉”正确的.*是“
                    searchRes = re.search('(?:正确的.*是)', handleTxt)
                    if searchRes:
                        res = list(searchRes.span())
                        handleTxt = handleTxt[0:res[0]] +  handleTxt[res[1]:]
                    # 在“ 时” 后面加“，”
                    searchRes = re.search('(?:[^必要|随|小|临|及]时)', handleTxt)
                    if searchRes:
                        res = list(searchRes.span())
                        print(handleTxt)
                        if res[1] < len(handleTxt) and handleTxt[res[1]] != '，' and handleTxt[res[1]] != ',' and \
                                handleTxt[res[1]] != '候' and handleTxt[res[1]] != '速' and handleTxt[res[1]] != '间' :
                            handleTxt = handleTxt[0:res[1]] + '，'+handleTxt[res[1]:]
                    file.write(handleTxt + '\n')
                else:
                    # 加‘，’
                    searchRes = re.search('(?:[^必要|随|小|临|及]时)', write_data)
                    if searchRes:
                        res = list(searchRes.span())
                        if res[1] < len(write_data) and write_data[res[1]] != '，' and write_data[res[1]] != ',' and \
                                write_data[res[1]] != '候' and write_data[res[1]] != '速'  and write_data[res[1]] != '间':
                            write_data = write_data[0:res[1]] + '，' + write_data[res[1]:]
                    # 判断题处理
                    if re.search('错误', write_data):
                        judgment_question_false_list.append(write_data)
                    else:
                        # 正确的判断题当做陈述句处理
                        judgment_question_true_list.append(write_data)

    # 判断题写入
    file.write('\n')
    for item in judgment_question_true_list:
        file.write(item + '\n')
    file.write('\n')
    # 答案为错误的判断题 —— 暂时不考虑
    # for item in judgment_question_false_list:
    #     file.write(item + '\n')

    file.close()
    return new_file_Name

# =========================================================================================================
#=========================================== 选择题分别对题干和答案处理，题干（条件），答案（行为）==============


# 科目一选择题处理
def handleK1Question(sentence):
    slen = len(sentence)
    # 答案插入需拼接
    searchRes = re.search('(?:怎样|如何)', sentence)
    if searchRes:
        res = list(searchRes.span())
        start = sentence.find('(', res[1])  # 找括号的位置
        if re.search('应', sentence[0:res[0]]):
            split_flag = '=>'
        else:
            split_flag = '=>' # 这里，不要加“应”处理看看
        sentence = sentence[0:res[0]] + split_flag + sentence[start + 1:slen - 1]
        return sentence

    # 答案直接替换文字
    searchRes = re.search('(?:什么|多少|怎么办|怎么做|多远|哪条|以下哪种情况下)', sentence)
    if searchRes:
        res = list(searchRes.span())
        start = sentence.find('(', res[1])
        split_flag = '=>'
        sentence = sentence[0:res[0]] + split_flag+ sentence[start + 1:slen - 1]
        return sentence

    # 处理这种情况 —— 写论文时可以通过print修改前后举例。
    # 行经下列哪种路段时不得超车？(交叉路口)
    # 行经交叉路口时不得超车
    searchRes = re.search(r'(有)?下列.*?[时|辆|段]', sentence)
    if searchRes:
        # print(sentence)
        res = list(searchRes.span())
        start = sentence.find('(', res[1])
        if sentence[res[1]] == '时':
            split_flag = '=>'
        else:
            split_flag = '时，=>'
        sentence = sentence[0:res[0]] + sentence[start + 1:slen - 1] + split_flag +sentence[res[1] :start-1]
        # print(sentence)
        return sentence

    return sentence

# 科目四选择题处理
def handleK4Question(sentence):
    slen = len(sentence)
    # 答案插入需拼接
    # 以下关于驶离高速公路的做法正确的是什么？(提前开启右转向灯 驶入减速车道 按减速车道规定的时速行驶 ) --这句被过滤掉了前提：驶离高速公路
    # 但是下面还会有相关的问题，这里可以考虑忽略
    searchRes = re.search('(?:怎么办|怎么做|怎样|如何|(?:以下|下列).*?正确)', sentence)
    if searchRes:
        res = list(searchRes.span())
        start = sentence.find('(', res[1])  # 找括号的位置
        if re.search('(?:应|要|，)', sentence[res[0]-3:res[0]]):
            split_flag = '=>'
        else:
            split_flag = '=>'  # 这里，不要加“应”处理看看
        sentence = sentence[0:res[0]] + split_flag + sentence[start + 1:slen - 1]
        return sentence

    # 错误答案处理 -在句子前面加不能，只有6条，先不考虑
    # searchRes = re.search(r'(以)?下.*?错误的是什么', sentence)
    # if searchRes:
    #     res = list(searchRes.span())
    #     start = sentence.find('(', res[1])
    #     sentence = sentence[0:res[0]] + '不能' + sentence[start + 1:slen - 1]
    #     return sentence

    # 处理：要采取的措施是（什么）？这一类问题
    searchRes = re.search(r'采取的.*?是', sentence)
    if searchRes:
        res = list(searchRes.span())
        start = sentence.find('(', res[1])
        split_flag = '=>'
        sentence = sentence[0:res[0]]  + split_flag + sentence[start + 1:slen - 1]
        return sentence

    # 答案直接替换文字
    searchRes = re.search('(?:什么地方|以下什么|什么灯|什么|多少|多远|哪条|哪些方面)', sentence)
    if searchRes:
        res = list(searchRes.span())
        start = sentence.find('(', res[1])
        sentence = sentence[0:res[0]]+sentence[start + 1:slen - 1] + sentence[res[1]:start-1]
        return sentence


    return sentence


def dataFilterNew(fileName, regStr, salt):
    # 加载题库
    data = load(fileName)
    res_list = data['result']
    new_file_Name = './'+salt+fileName+"Data.txt"
    # 先删除文件
    try:
        os.remove(new_file_Name)
    except IOError:
        print("Error: 删除文件失败")
    try:
        file = open(new_file_Name, "a", encoding='utf-8')  # a 方式，seek是无效的
    except IOError:
        print("Error: 没有找到文件或读取文件失败")

    judgment_question_true_list = []  # 判断题
    judgment_question_false_list = []  # 判断题

    for res in res_list:
        if res['url'] != '':
            # 去掉图片题
            pass
        else:
            # 答案匹配 ABCD
            answer = ''
            for key in result_tk:
                if res['answer'] == key:
                    res_arr = result_tk[key]
                    break
            for index, item in enumerate(res_arr):
                if index == len(res_arr) - 1:
                    delimiter  = ''
                else:
                    delimiter = '，'
                if item == 'A':
                    answer += res['item1'] + delimiter if res['item1'] != '' else '正确'  # 注意这里的,必须要
                if item == 'B':
                    answer += res['item2'] + delimiter if res['item2'] != '' else '错误'
                if item == 'C':
                    answer += res['item3'] + delimiter
                if item == 'D':
                    answer += res['item4'] + delimiter

            question = res['question']
            explains = res['explains']

            # 去掉-交通法扣分题
            if re.search('\d分', answer) or re.search('\d分', question):
                continue

            # 写入数据拼接 ，注意这里后面的空格必须要
            if answer == "正确"  or answer == "对":
                write_data = question
            elif answer == "错误"  or answer == "错":
                write_data = question + '(错误)'
            else:
                write_data = question + '(' + answer + ')'

            # 去掉法律相关条款等：通过关键字匹配
            pattern = re.compile(regStr)
            if not pattern.search(write_data):
                # 把驾驶机动车5个字去掉，语句意思不变，但对角色标注有好处
                # 这个放在最前面，是因为选择题和判断题中都去掉
                # searchRes = re.search('驾驶机动车', write_data)
                # if searchRes:
                #     res = list(searchRes.span())
                #     write_data = write_data[0:res[0]] + write_data[res[1]:]
                # if '是因为' in write_data:
                #     continue
                # 处理选择题
                if re.search('(?:\?|？)', write_data):
                    # 选择题的处理
                    if fileName == 'k1' :
                        handleTxt = handleK1Question(write_data)
                    else:
                        handleTxt = handleK4Question(write_data)
                        # if handleTxt.startswith('，'):
                        #     print('这句处理错误，舍弃：',write_data)
                        #     continue
                    # file.write(write_data + '\n') #原句-对照看处理结果
                    # 去掉依然含有？的句子
                    # searchRes = re.search('[?|？]', handleTxt)
                    # if searchRes:
                    #     continue
                    # # 去掉 ‘主路车流量大、速度快’ 这一句，没有意义
                    # if '主路车流量大、速度快' in handleTxt:
                    #     continue
                    # # 去掉“应当，开启转向灯观察主路情况确保安全汇入车流”
                    # if handleTxt.startswith('应当'):
                    #     continue
                    #
                    # if '路面无障碍物，道路宽直' in handleTxt :
                    #     continue
                    # # 去掉”正确的.*是“
                    # searchRes = re.search('(?:正确的.*是)', handleTxt)
                    # if searchRes:
                    #     res = list(searchRes.span())
                    #     handleTxt = handleTxt[0:res[0]] +  handleTxt[res[1]:]
                    # # 在“ 时” 后面加“，”
                    # searchRes = re.search('(?:[^必要|随|小|临|及]时)', handleTxt)
                    # if searchRes:
                    #     res = list(searchRes.span())
                    #     print(handleTxt)
                    #     if res[1] < len(handleTxt) and handleTxt[res[1]] != '，' and handleTxt[res[1]] != ',' and \
                    #             handleTxt[res[1]] != '候' and handleTxt[res[1]] != '速' and handleTxt[res[1]] != '间' :
                    #         handleTxt = handleTxt[0:res[1]] + '，'+handleTxt[res[1]:]
                    file.write(handleTxt + '\n')
                else:
                    # 加‘，’
                    searchRes = re.search('(?:[^必要|随|小|临|及]时)', write_data)
                    if searchRes:
                        res = list(searchRes.span())
                        if res[1] < len(write_data) and write_data[res[1]] != '，' and write_data[res[1]] != ',' and \
                                write_data[res[1]] != '候' and write_data[res[1]] != '速'  and write_data[res[1]] != '间':
                            write_data = write_data[0:res[1]] + '，' + write_data[res[1]:]
                    # 判断题处理
                    if re.search('错误', write_data):
                        judgment_question_false_list.append(write_data)
                    else:
                        # 正确的判断题当做陈述句处理
                        judgment_question_true_list.append(write_data)

    # 判断题写入
    file.write('\n')
    for item in judgment_question_true_list:
        file.write(item + '\n')
    file.write('\n')
    # 答案为错误的判断题 —— 暂时不考虑
    # for item in judgment_question_false_list:
    #     file.write(item + '\n')

    file.close()
    return new_file_Name


def startK1K4Filter(filter1,filter4,salt):
    reg1Str = loadFilterKeyWords(filter1)
    reg4Str = loadFilterKeyWords(filter4)

    # 文件名前缀，正则匹配过滤文本
    try:
        file_Name1 = dataFilter('k1', reg1Str,salt)
        file_Name4 = dataFilter('k4', reg4Str,salt)
    except IOError:
        print("Error: 驾考题过滤出错")
        return 0
    else:
        # 想放在一个文件下，文件合并
        concatTxt(file_Name1,file_Name4,'k1_k4Data.txt',salt)
        return 1


if __name__ == '__main__':
    # reg1Str = loadFilterKeyWords('filter_key_words_1')
    # reg4Str = loadFilterKeyWords('filter_key_words_4')
    # # 想放在一个文件夹，文件名写一样即可，现在是分开处理的
    # dataFilter('k1', reg1Str)  # 文件名前缀，正则匹配过滤文本
    # dataFilter('k4', reg4Str)

    # 自己的过滤词，类型：文件
    startK1K4Filter('filter_key_words_1','filter_key_words_4','')

    # 用户自定义过滤词，类型：数组

# 17行，手动处理