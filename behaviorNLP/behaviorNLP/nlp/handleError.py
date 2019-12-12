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




def handleError(flag,patternCon,patternBeh):
    if flag == 0:
        error_file = './analyzeResult/safeResult/errorRules.txt'
        write_result = './analyzeResult/safeResult/errorToRight.txt'
    else:
        error_file = './analyzeResult/tkResult/errorRules.txt'
        write_result = './analyzeResult/tkResult/errorToRight.txt'
    try:
        os.remove(write_result)
    except IOError:
        print("Error: 删除标注后处理文件失败")
    try:
        errorText = open(error_file, 'r', encoding='utf-8')
        errorToRight = open(write_result, 'a', encoding='utf-8')
    except IOError:
        print("Error: 没有找到角色标注失败的文件")

    line = errorText.readline()
    while line:
        con_list = []
        beh_list = []
        line = line.strip()
        if line == '':
            pass
        else:
            ind = line.find('应')
            if ind != -1 and line[ind-1] != '，':
                line = line[0:ind] + '，' + line[ind:]
            sentence_list = line.split('，')

            # 简单划分，最后一个是行为
            con_list += sentence_list[0:-1]
            beh_list.append(sentence_list[-1])

            con_list_copy = con_list.copy()
            for item in con_list_copy:
                if patternBeh.search(item):
                    # 短语中间有条件词
                    print(item + ': 有行为词')
                    beh_list.insert(0,item)
                    con_list.remove(item)


            # 题库处理—— 这个效果还没有上面的好
            # else :
            #     # 有“时，”的情况
            #     index = line.rfind('时，')
            #     if index != -1 :
            #         print('====',line)
            #         # 以最后一个“时，”为分割点
            #         sentence_list = line.split('时，',1)
            #         for i in range(len(sentence_list)):
            #             item = sentence_list[i]
            #             if i == 0 :
            #                 con_list.append(item)
            #             else:
            #                 ind = item.find('，应')
            #                 if ind != -1:
            #                     item = item[0:ind] + '|' + item[ind:]
            #                     item_list = item.split('|')
            #                     con_list.append(item_list[0])
            #                     beh_list.append(item_list[1])
            #                 else:
            #                     sentence_list = item.split('，')
            #                     beh_list = sentence_list
            #     else :
            #         print('++++', line)
            #         ind = line.find('，应')
            #         if ind != -1 :
            #             line = line[0:ind] + '|' + line[ind:]
            #             sentence_list = line.split('|')
            #             con_list.append(sentence_list[0])
            #             beh_list.append(sentence_list[1])
            #         else :
            #             sentence_list = line.split('，')
            #             con_list = sentence_list[0:-1]
            #             beh_list.append(sentence_list[-1])
            #
            #     con_list_copy = con_list.copy()
            #     for item in con_list_copy:
            #         if patternBeh.search(item):
            #             # 短语中间有条件词
            #             print(item + ': 有行为词')
            #             beh_list.insert(0, item)
            #             con_list.remove(item)


            # print(con_list,beh_list)
            # 写入txt
            for item in con_list :
                errorToRight.write(item+' ')
            errorToRight.write('-->')
            for item in beh_list:
                errorToRight.write(item + ' ')
            errorToRight.write('\n')
        line = errorText.readline()


# 0 是安全条例，1是驾考题库
if __name__ == '__main__':
    flag = 1

    if flag == 0:
        conditonsRegx = loadFilterKeyWords('./utils/error_conditions.txt')
        patternCon = re.compile(conditonsRegx)
    else:
        conditonsRegx = loadFilterKeyWords('./utils/error_conditions.txt')
        patternCon = re.compile(conditonsRegx)

    # 驾驶行为正则
    regx1 = loadFilterKeyWords('./utils/error_behaviors.txt')
    patternBeh = re.compile(regx1)
    print(patternBeh)
    handleError(flag,patternCon,patternBeh)