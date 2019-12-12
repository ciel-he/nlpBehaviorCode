# -*- coding: utf-8 -*-
from behaviorNLP.nlp.utils.getRegxFromText import loadFilterKeyWords
from behaviorNLP.nlp.utils.myLtpTool import myLtpTool
from behaviorNLP.nlp.utils.forceSegmentor import ForceSegmentor
from behaviorNLP.nlp.utils.filterRoleTag import handleRoleToOne,handleRoleToOneTwice,newHandleRoleTag
from behaviorNLP.nlp.utils.wordTagsAfterTreat import wordTagsAfterTreat
from behaviorNLP.nlp.utils.getConditionAndBehavior import getConAndBehBySafe,getConAndBehByTK
from behaviorNLP.nlp.utils.db_crud import insertConAndBeh
import os
import re


# 获得ltp工具
ltpTool = myLtpTool()


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# NLP_DIR = BASE_DIR+"/behaviorNLP/nlp"
# read_file：待处理的行为准则
# write_tag_file : 词性标注结果文件
# write_tag_parse_file ：语义角色标注结果文件

# 测试
userdict = './utils/userdict.txt'
# 0 是安全条例，1是驾考题库
flag = 1
# 处理安全条例
if flag == 0:
    read_file = './safeData/trafficRules.txt'
    write_tag_parse_file = './analyzeResult/safeResult/roleTagRules.txt'
    write_tag_error_file = './analyzeResult/safeResult/roleTagError.txt'
    write_error_file = './analyzeResult/safeResult/errorRules.txt'
    write_result_file = './analyzeResult/safeResult/resultRules.txt'
# 处理驾考题库
else:
    read_file = './tkData/k1_k4Data.txt'
    write_tag_parse_file = './analyzeResult/tkResult/roleTagRules.txt'
    write_tag_error_file = './analyzeResult/tkResult/roleTagError.txt'
    write_error_file = './analyzeResult/tkResult/errorRules.txt'
    write_result_file = './analyzeResult/tkResult/resultRules.txt'

try:
    # 下面两句没有文件会报错
    os.remove(write_tag_parse_file)
    os.remove(write_tag_error_file)
    os.remove(write_error_file)
    os.remove(write_result_file)
except IOError:
    print("Error: 删除文件失败")
try:
    tag_parse_file = open(write_tag_parse_file, 'a', encoding='utf-8')
    tag_error_file = open(write_tag_error_file, 'a', encoding='utf-8')
    error_file = open(write_error_file, 'a', encoding='utf-8')
    result_file = open(write_result_file, 'a', encoding='utf-8')
except IOError:
    print("Error: 没有找到文件或读取文件失败")

if flag == 0:
    # 驾驶条件正则
    conditonsRegx = loadFilterKeyWords('./utils/conditions.txt')
    patternCon = re.compile(conditonsRegx)
else :
    # 驾驶条件正则
    conditonsRegx = loadFilterKeyWords('./utils/conditionsTK.txt')
    patternCon = re.compile(conditonsRegx)
# 驾驶行为正则
regx1 = loadFilterKeyWords('./utils/behaviors.txt')
patternBeh = re.compile(regx1)
# 处理之后的无效词过滤
regx2 = loadFilterKeyWords('./utils/noUseWords.txt')
patternNoUse = re.compile(regx2)




# 读取文件内容
def getText(read_file):
    file = open(read_file, 'r', encoding='utf-8')
    line = file.readline()
    i = 1
    while line:
        line = line.strip()
        if line == '':
            # print('空行')
            pass
        else:
            print('写入第' + str(i) + '行')
            tag_parse_file.write('第' + str(i) + '条' + '\n')
            tag_error_file.write('第' + str(i) + '条' + '\n')
            words = wordsSplite(line)
            wordsTagAndWriteFile(words)
            i += 1
        line = file.readline()

        # if i > 20:
        #     break

    file.close()


##分词
def wordsSplite(s):
    # 调用默认的ltp分词得到的分词结果
    words = ltpTool.word_splitter(s)
    words = list(words)
    # 通过用户字典，将拆分的词又组合起来
    forceSegmentor = ForceSegmentor()
    forceSegmentor.load(userdict)
    # 强制分词以后的结果
    words = forceSegmentor.merge(s, words)
    return words



# 词性标注-》 句法依存-》语义角色标注。words类型list
def wordsTagAndWriteFile(words):
    # 词性标注+写入文件
    tags = ltpTool.word_tag(words)
    tags = list(tags)

    # 词性标注结果存入文件
    # for word, tag, i in zip(words, tags, range(len(words))):
    #     tag_file.write(word + '/' + tag + '  ')
        # tag_parse_file.write('(' + str(i) + ')' + word + '/' + tag + '  ')
    # tag_file.write('\n')
    # tag_parse_file.write('\n')

    # 句法依存
    arcs = ltpTool.parse(words, tags)
    # 角色标注结果
    roles = ltpTool.sementic_role(words, tags, arcs)
    # for role in roles:
    #     tag_parse_file.write(str(role.index) + ' ' +
    #                      "".join(["%s:(%d,%d)  " % (arg.name, arg.range.start, arg.range.end) for arg in
    #                               role.arguments]) + '\n')
    # tag_parse_file.write('\n')

    # 安全条例处理
    if flag == 0:

        # 看一下筛选去重处理之后的
        new_roles = handleRoleToOne(words,roles)
        # for role in new_roles:
        #     tag_parse_file.write(str(role["index"]) + ' ' +
        #                      "".join(["%s:(%d,%d)  " % (arg.name, arg.range.start, arg.range.end) for arg in
        #                               role["arguments"]]) + '\n')
        # tag_parse_file.write('\n')

        # 角色标注有问题，记录下来
        if new_roles[len(new_roles) - 1]['index'] == -1:

            for word, tag, i in zip(words, tags, range(len(words))):
                error_file.write(word)
                tag_error_file.write('(' + str(i) + ')' + word + '/' + tag + '  ')
            error_file.write('\n')
            tag_error_file.write('\n')

            # 未处理之前的
            for role in roles:
                tag_error_file.write(str(role.index) + ' ' +
                                     "".join(["%s:(%d,%d)  " % (arg.name, arg.range.start, arg.range.end) for arg in
                                              role.arguments]) + '\n')
            tag_error_file.write('\n')
            # 去重之后的
            for role in new_roles:
                tag_error_file.write(str(role["index"]) + ' ' +
                                 "".join(["%s:(%d,%d)  " % (arg.name, arg.range.start, arg.range.end) for arg in
                                          role["arguments"]]) + '\n')
            tag_error_file.write('\n')
            return

        # 再一次筛选去重
        for word, tag, i in zip(words, tags, range(len(words))):
            tag_parse_file.write('(' + str(i) + ')' + word + '/' + tag + '  ')
        tag_parse_file.write('\n')

        new_roles2 = handleRoleToOneTwice(words, new_roles)
        for role in new_roles2:
            tag_parse_file.write(str(role["index"]) + ' ' +
                                 "".join(["%s:(%d,%d)  " % (arg.name, arg.range.start, arg.range.end) for arg in
                                          role["arguments"]]) + '\n')
        tag_parse_file.write('\n')

        # 获得结果
        con_beh_res = getConAndBehBySafe(words,new_roles2,patternCon,patternBeh)
        condition_list = con_beh_res["conditions"]
        behavior_list = con_beh_res["behavior"]
        for item in condition_list:
            result_file.write(item+'  ')
        result_file.write('-->')
        for item in behavior_list:
            result_file.write(item+' ')
        result_file.write('\n')

        # 软著到这里就结束了，写进文档供下载
        return
        # 识别条件，写入数据库  —— 实验需要的
        # insertConAndBeh(condition_list,behavior_list)

    # 题库处理
    else :

        new_roles = newHandleRoleTag(words, roles)

        # 角色标注有问题，跳过
        if new_roles[len(new_roles) - 1]['index'] == -1:
            for word, tag, i in zip(words, tags, range(len(words))):
                error_file.write(word)
                tag_error_file.write('(' + str(i) + ')' + word + '/' + tag + '  ')
            error_file.write('\n')
            tag_error_file.write('\n')
            # 未处理之前的 --------------------------- 可注释
            for role in roles:
                tag_error_file.write(str(role.index) + ' ' +
                                     "".join(["%s:(%d,%d)  " % (arg.name, arg.range.start, arg.range.end) for arg in
                                              role.arguments]) + '\n')
            tag_error_file.write('\n')
            # 去重之后的
            for role in new_roles:
                tag_error_file.write(str(role["index"]) + ' ' +
                                 "".join(["%s:(%d,%d)  " % (arg.name, arg.range.start, arg.range.end) for arg in
                                          role["arguments"]]) + '\n')
            tag_error_file.write('\n')
            return

        # 角色标注没问题，接着进行处理
        # 原例句
        for word, tag, i in zip(words, tags, range(len(words))):
            tag_parse_file.write('(' + str(i) + ')' + word + '/' + tag + '  ')
        tag_parse_file.write('\n')
        # 原
        for role in roles:
            tag_parse_file.write(str(role.index) + ' ' +
                                 "".join(["%s:(%d,%d)  " % (arg.name, arg.range.start, arg.range.end) for arg in
                                          role.arguments]) + '\n')
        tag_parse_file.write('\n')
        # 新角色标注
        for role in new_roles:
            tag_parse_file.write(str(role["index"]) + ' ' +
                             "".join(["%s:(%d,%d)  " % (arg.name, arg.range.start, arg.range.end) for arg in
                                      role["arguments"]]) + '\n')
        tag_parse_file.write('\n')

        # 获得结果
        con_beh_res = getConAndBehByTK(words, new_roles, patternCon,patternBeh,patternNoUse)
        condition_list = con_beh_res["conditions"]
        behavior_list = con_beh_res["behavior"]
        for item in condition_list:
            result_file.write(item + '  ')
        result_file.write('-->')
        for item in behavior_list:
            result_file.write(item + ' ')
        result_file.write('\n')


def testSingleSentence(line):
    words = wordsSplite(line)
    tags = ltpTool.word_tag(words)
    tags = list(tags)
    # 句法依存
    arcs = ltpTool.parse(words, tags)
    # 角色标注结果
    roles = ltpTool.sementic_role(words, tags, arcs)
    for word, tag, i in zip(words, tags, range(len(words))):
        print('(' + str(i) + ')' + word + '/' + tag + '  ')
    print('\n')
    for role in roles:
        print(str(role.index) + ' ' +
                         "".join(["%s:(%d,%d)  " % (arg.name, arg.range.start, arg.range.end) for arg in
                                  role.arguments]) + '\n')
    print('\n')


if __name__ == '__main__':

    getText(read_file)

    # ques = '在路口右转弯遇同车道前车等候放行信号时如何行驶？'
    # testSingleSentence(ques)
