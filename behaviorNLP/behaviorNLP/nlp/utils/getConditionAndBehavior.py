# 安全条例
# arr 为一个数组，从0-5依次为 : DIS, A0,ADV,V,A1,A2(C_A1)
def getConAndBehBySafe(words,roles,patternCon,patternBeh):
    phrase_list = []
    condition_list = []
    for role, i in zip(roles,range(len(roles))):
        if i == 0 :
            # 动词
            v_str = words[role['index']]
            arr = ['']*6
            arr[3] = v_str
            for arg,j in zip(role['arguments'],range(len(role['arguments']))):
                # 去掉法律相关条款等：通过关键字匹配
                startIndex = arg.range.start
                endIndex = arg.range.end
                # 去掉，
                if words[endIndex] == '，':
                    phrase = "".join(words[startIndex:endIndex])
                else:
                    phrase = "".join(words[startIndex:endIndex + 1])
                if arg.name == 'TMP' or arg.name == 'LOC':
                    if role['arguments'][j-1].name == 'A0':
                        condition_list.append(arr[1] + phrase)
                        arr[1] = ''
                    else:
                        condition_list.append(phrase)
                elif arg.name == 'DIS':
                    arr[0] = phrase
                elif arg.name == 'A0' or arg.name == 'MNR':
                    if arr[1] != '' :
                        condition_list.insert(0,arr[1])
                    arr[1] = phrase
                elif arg.name == 'ADV':
                    arr[2] = phrase
                elif arg.name == 'A1':
                    # 103 ,一个句子有两个A1
                    if arr[4] != '':
                        arr[0] = arr[4]
                    arr[4] = phrase
                elif arg.name == 'A2' or arg.name == 'C-A1':
                    arr[5] = phrase
            # 第一行肯定有条件，所以当没有tmp等时，整句作为条件
            if len(condition_list) == 0 :
                #  没有A0，有A1
                if arr[1]== '' and arr[4] != ''  :
                    # 146行的情况
                    if len(role['arguments'])>2 :
                        condition_list.append(arr[4])
                        arr[4] = ''
                        phrase_list.append("".join(arr))
                    # 84 行情况
                    else :
                        condition_list.append(arr[3]+arr[4])
                # 161 行的情况 有A0， 而且只有这一行，动词后面拆成行为
                elif arr[1] != ''  and len(roles) == 1:
                    condition_list.append(arr[1])
                    arr[1] = ''
                    phrase_list.append("".join(arr))
                else :
                    condition_list.append("".join(arr))
            else:
                if arr[1] == '' and arr[5] != '':
                    # A1 C-A1 情况
                    phrase_list.append(arr[4] + arr[3] + arr[5])
                else:
                    phrase_list.append("".join(arr))
        else :
            # 动词
            v_str = words[role['index']]
            arr = [''] * 6
            arr[3] = v_str
            for arg in role['arguments']:
                # 去掉法律相关条款等：通过关键字匹配
                startIndex = arg.range.start
                endIndex = arg.range.end
                phrase = "".join(words[startIndex:endIndex + 1])

                if arg.name == 'TMP' or arg.name == 'LOC':
                    phrase_list.append(phrase)
                elif arg.name == 'DIS':
                    arr[0] = phrase
                elif arg.name == 'A0' or arg.name == 'MNR':
                    # if pattern.search(phrase):
                    #     print(phrase + ': 有条件词1')
                    #     condition_list.append(phrase)
                    # else:
                    arr[1] = phrase
                elif arg.name == 'ADV':
                    arr[2] = phrase
                elif arg.name == 'A1':
                    # 103 ,一个句子有两个A1
                    if arr[4] != '':
                        arr[0] = arr[4]
                    arr[4] = phrase
                elif arg.name == 'A2' or arg.name == 'C-A1':
                    arr[5] = phrase

            if arr[1] == '' and arr[5] != '':
                # A1 C-A1 情况
                phrase_list.append(arr[4]+arr[3]+arr[5])
            else:
                phrase_list.append("".join(arr))





    print(condition_list, phrase_list)

    # 删除行为中重复部分
    plist = phrase_list.copy()
    for i in range(len(phrase_list)):
        for j in range(len(phrase_list)):
            if j != i and phrase_list[i] in phrase_list[j]:
                plist.remove(phrase_list[i])

    # 判断条件词，如果是条件，就放到condition_list里面
    plist_copy = plist.copy()
    for item in plist_copy:
        if patternCon.search(item):
            # 短语中间有条件词
            print(item+': 有条件词1')
            condition_list.append(item)
            plist.remove(item)

    # 行为词
    condition_list_copy = condition_list.copy()
    for item in condition_list_copy:
        if patternBeh.search(item):
            # 短语中间有条件词
            print(item + ': 有行为词1')
            plist.append(item)
            condition_list.remove(item)

    print(condition_list, plist)

    result = {
        "conditions": condition_list,
        "behavior": plist
    }
    return result

# 题库处理
def getConAndBehByTK(words,roles,patternCon,patternBeh,patternNoUse):
    phrase_list = []
    condition_list = []

    if len(roles)==1:
        role = roles[0]
        # 动词
        v_str = words[role['index']]
        arr = [''] * 6
        arr[3] = v_str
        for arg, j in zip(role['arguments'], range(len(role['arguments']))):
            startIndex = arg.range.start
            endIndex = arg.range.end
            # 去掉，
            if words[endIndex] == '，' or words[endIndex] == ',':
                phrase = "".join(words[startIndex:endIndex])
            else:
                phrase = "".join(words[startIndex:endIndex + 1])
            if arg.name == 'TMP' or arg.name == 'LOC':
                if j != 0 and role['arguments'][j - 1].name == 'A0':
                    condition_list.append(arr[1] + phrase)
                    arr[1] = ''
                # TMP 和 LOC都有的情况，LOC作为行为
                elif len(condition_list)!=0 and '时' in condition_list[-1]:
                    phrase_list.append(phrase)
                else:
                    condition_list.append(phrase)
            elif arg.name == 'DIS':
                arr[0] = phrase
            elif arg.name == 'A0' or arg.name == 'MNR':
                if arr[1] != '':
                    condition_list.insert(0, arr[1])
                arr[1] = phrase
            elif arg.name == 'ADV':
                # 第4条，两个ADV，后一个ADV当做名词用
                if role['arguments'][j - 1].name == 'ADV':
                    arr[5] = phrase
                else:
                    arr[2] = phrase
            elif arg.name == 'A1':
                # 100 ,一个句子有两个A1
                if arr[4] != '':
                    arr[5] = phrase
                else :
                    arr[4] = phrase
            elif arg.name == 'A2' or arg.name == 'C-A1':
                arr[5] = phrase

        # 第一行肯定有条件，所以当没有tmp等时，整句作为条件
        if len(condition_list) == 0 :
            #  没有A0，有A1
            if arr[1]== '' and arr[4] != ''  :
                print('没有A0，有A1')
                # 138行的情况
                condition_list.append(arr[2] + arr[3])
                phrase_list.append(arr[4])
            # 276 行的情况 有A0， 而且只有这一行，动词后面拆成行为
            elif arr[1] != '':
                condition_list.append(arr[1])
                arr[1] = ''
                phrase_list.append("".join(arr))
            else :
                condition_list.append("".join(arr))
        else:
            phrase_list.append("".join(arr))
    else :
        for role, i in zip(roles, range(len(roles))):
            # 动词
            v_index = role['index']
            v_str = words[v_index]
            arr = []
            arg_len = len(role['arguments'])
            for arg,j in zip(role['arguments'],range(arg_len)):
                startIndex = arg.range.start
                endIndex = arg.range.end
                phrase = "".join(words[startIndex:endIndex + 1])
                # 动词的摆放位置
                if startIndex > v_index:
                    arr.append(v_str)
                    v_str = ''
                    v_index = len(words)
                if arg.name == 'TMP' or arg.name == 'LOC':
                    if patternBeh.search(phrase) :
                        # 有行为词 或者 LOC是最后一个（9条） or j == arg_len-1
                        arr.append(phrase)
                    else:
                        # arg.name == 'LOC' and kan 79 TMP 也可以
                        if j == arg_len-1:
                            # 73 条：['在没有道路中心线的狭窄山路，靠']
                            if not phrase.endswith('，'):
                                phrase += v_str
                            v_str = ''
                        condition_list.append(phrase)
                else:
                    arr.append(phrase)
            if v_str != '':
                arr.append(v_str)
            if len(arr) == 0:
                # arr 里面没东西
                continue
            temp_str = "".join(arr)
            temp_arr = temp_str.split('，')
            if i == 0 and len(condition_list) == 0:
                # 多行情况下，第一句如果没有TMP和LOC，那么整句是条件
                # condition_list.append("".join(arr))
                condition_list.extend(temp_arr)
            else:
                # phrase_list.append("".join(arr))
                phrase_list.extend(temp_arr)

    # print(condition_list, phrase_list)

    # 后续处理

    # 删除条件中重复部分
    clist = condition_list.copy()
    for i in range(len(condition_list)):
        for j in range(len(condition_list)):
            if j != i and condition_list[i] != '' and condition_list[i] in condition_list[j]:
                clist.remove(condition_list[i])

    # 删除行为中重复部分
    plist = phrase_list.copy()
    for i in range(len(phrase_list)):
        for j in range(len(phrase_list)):
            if j != i and phrase_list[i] != '' and phrase_list[i] in phrase_list[j]:
                plist.remove(phrase_list[i])

    # 判断条件词，如果是条件，就放到condition_list里面
    plist_copy = plist.copy()
    for item in plist_copy:
        if patternCon.search(item):
            # 短语中间有条件词
            print(item + ': 有条件词2')
            clist.append(item)
            plist.remove(item)

    # 行为词
    clist_copy = clist.copy()
    for item in clist_copy:
        if patternBeh.search(item):
            # 短语中间有条件词
            print(item + ': 有行为词2')
            plist.append(item)
            clist.remove(item)

    print(clist, plist)

    # 删除一些无效词
    res_clist = clist.copy()
    for item in clist:
        if len(item) == 1 or patternNoUse.search(item):
            res_clist.remove(item)

    res_plist = plist.copy()
    for item in plist:
        if len(item) == 1 or patternNoUse.search(item):
            res_plist.remove(item)

    print(res_clist, res_plist)

    result = {
        "conditions": res_clist,
        "behavior": res_plist
    }
    return result
