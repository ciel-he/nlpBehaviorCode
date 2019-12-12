# -*- coding: utf-8 -*-
import sys
import os
import re
from pyltp import *
# import nltk
# from nltk.tree import Tree
# from nltk.grammar import DependencyGrammar
# from nltk.parse import *

class myLtpTool():

    def __init__(self):
        base = "F:\\NLP-relative\\myLibs\\ltp_data_v3.4.0\\"
        # 初始化分词
        self.segmentor = Segmentor()
        user_dict = base+'userdict.txt'
        self.segmentor.load_with_lexicon(base + 'cws.model', user_dict)
        # 初始化词性标注
        self.postagger = Postagger()
        user_tag = base+"usertag.txt"
        self.postagger.load_with_lexicon(base + 'pos.model',user_tag)  # 加载模型

        # 初始化命名实体识别
        self.recognizer = NamedEntityRecognizer()  # 初始化实例
        self.recognizer.load(base + 'ner.model')  # 加载模型

        # 初始化句法分析
        self.parser = Parser()  # 初始化实例
        self.parser.load(base + 'parser.model')  # 加载模型

        # 初始化语义角色
        self.labeller = SementicRoleLabeller()  # 初始化实例
        self.labeller.load(base + 'pisrl_win.model')  # 加载模型

    # 在销毁里面释放模型,程序结束自动执行
    def __del__(self):
        self.releaseAllModel()
        class_name = self.__class__.__name__
        print(class_name, "销毁")

    def releaseAllModel(self):
        self.segmentor.release()
        self.postagger.release()
        self.recognizer.release()
        self.parser.release()  # 释放模型
        self.labeller.release()

    def sentence_splitter(sentence):
        """
        分句，也就是将一片文本分割为独立的句子
        :param sentence:几句话
        :return: 单个单个句子
        """
        single_sentence = SentenceSplitter.split(sentence)  # 分句
        return single_sentence


    def word_splitter(self,sentence):
        """
        分词：加上用户词典
        """
        words2 = self.segmentor.segment(sentence)
        return words2


    def word_tag(self,words):
        """
        词性标注
        :param words: 已切分好的词
        :return:
        """
        postags = self.postagger.postag(words)  # 词性标注

        return postags


    def name_recognition(self,words, postags):
        """
        命名实体识别
        :param words:分词
        :param postags:标注
        :return:
        """

        netags = self.recognizer.recognize(words, postags)  # 命名实体识别

        return netags


    def parse(self,words, postags):
        """
        依存句法分析
        :param words:
        :param postags:
        :return:
        """

        arcs = self.parser.parse(words, postags)  # 句法分析
        return arcs


    def sementic_role(self,words, postags, arcs):

        # # 语义角色标注
        # arcs 是使用依存句法分析的结果
        roles = self.labeller.label(words, postags, arcs)
        return roles


# 测试
# myltp = myLtpTool()
# sentence = '驶近没有人行横道的交叉路口时，发现有人横穿道路，应减速或停车让行 '
# words = list(myltp.word_splitter(sentence))
# print([(word,i) for word,i in zip(words,range(len(words)))])
#
# tags = list(myltp.word_tag(words))
# arcs = myltp.parse(words, tags)
# roles = myltp.sementic_role(words, tags,arcs)
# for role in roles:
#     print(role.index, "".join(["%s:(%d,%d)  " % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
#




