# 词性标注后处理一：将u词性的词，与前一个词以及后面的n一起合并成一个名词
# 不能这么处理，处理之后，有些变好了10，有些变差了，如1
# 有些不变，如6，这个没有用
def wordTagsAfterTreat(words, tags):
    # 词性标注+写入文件

    tags = list(tags)

    # 词性标注后处理一：将u词性的词，与前一个词以及后面的n一起合并成一个名词
    while True:
        indexU = indexStart = indexEnd = -1
        if 'u' in tags:
            indexU = tags.index('u')
            # 这个是p+v+u+。。。+n的结构，之后肯定要改 ，或者d、、、用正则吧
            if tags[indexU - 2] == 'p':
                indexStart = indexU - 2
            else:
                indexStart = indexU - 1

            if 'n' in tags[indexU:]:
                indexEnd = tags[indexU:].index('n') + indexU
            else:
                indexEnd = indexU

        # print(words, '\n', tags, '\n', tags[indexU:], '\n', indexU, indexEnd)
        if indexU == -1 or indexEnd == -1:
            break
        concat_words = ''.join(words[indexStart:indexEnd + 1])
        tags = tags[:indexStart] + tags[indexEnd + 1:]
        words = words[:indexStart] + words[indexEnd + 1:]
        tags.insert(indexStart, 'n')
        words.insert(indexStart, concat_words)
        # print(words, '\n', tags, '\n', concat_words)

    return [words, tags]

# txtForTag中用
# 合并某些词性之后的效果
# ATreat = wordTagsAfterTreat(words, tags)
# words = ATreat[0]
# tags = ATreat[1]
# # 词性标注结果存入文件
# for word, tag, i in zip(words, tags, range(len(words))):
#     tag_file.write(word + '/' + tag + '  ')
#     tag_parse_file.write('(' + str(i) + ')' + word + '/' + tag + '  ')
# tag_file.write('\n')
# tag_parse_file.write('\n')
#
#
# # 句法依存
# arcs = ltpTool.parse(words, tags)
# # 角色标注结果
# roles = ltpTool.sementic_role(words, tags, arcs)
#
# for role in roles:
#     tag_parse_file.write(str(role.index) + ' ' +
#                          "".join(["%s:(%d,%d)  " % (arg.name, arg.range.start, arg.range.end) for arg in
#                                   role.arguments]) + '\n')
# tag_parse_file.write('\n')