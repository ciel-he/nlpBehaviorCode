
def takeArguLen(elem):
    return len(elem.arguments)


def handleRoleToOne(words,roles):

    # 按照argument的长度排序，解析最长的放最上面——放弃该方式
    # sort_roles = []
    # for role in roles:
    #     sort_roles.append(role)
    # sort_roles.sort(key=takeArguLen, reverse=True)
    #
    # roles = sort_roles

    strlen = len(words)
    new_roles = []
    maxLastIndex = -1
    minLastIndex = strlen
    maxlen_list = [] #主要用于计算是否标注就有问题，没有全标注出来
    for role , i in zip(roles,range(len(roles))):
        # 只有一个标注的情况不要
        # if len(role.arguments) < 2:
        #     continue
        v_index = role.index
        # 记录每一行的最大index，用于之后是否除去这一行
        maxIndex = -1
        minIndex = strlen
        maxlen = 0
        new_arguments = []
        for arg in role.arguments:
            startIndex = arg.range.start
            endIndex = arg.range.end
            # 不排序的话用这个

            if startIndex < minLastIndex and minLastIndex <= maxLastIndex and maxLastIndex < endIndex:
                if len(new_roles) > 0:
                    # print('删除上一个role')
                    new_roles.pop()
                    maxlen_list.pop() #把上一轮的长度也减掉
            if maxLastIndex >= endIndex :
                # print('跳过此次的',startIndex,' ', endIndex)
                continue
            # if minLastIndex < endIndex :
            #     continue
            new_arguments.append(arg)
            difflen = endIndex - startIndex+1
            maxlen += difflen
            maxIndex = max(maxIndex, endIndex)
            minIndex = min(minIndex, startIndex)
            # print(minIndex, maxIndex ,'----',minLastIndex, maxLastIndex,'==>',endIndex , startIndex ,maxlen)

        maxlen_list.append(maxlen)
        if maxIndex != -1 :
            maxLastIndex = maxIndex
        if minIndex != strlen:
            minLastIndex = minIndex
        # print(minIndex,maxIndex,minLastIndex,maxLastIndex,'下一轮role')
        if len(new_arguments) != 0:
            new_roles.append({"index":role.index,"arguments":new_arguments})

        if maxlen > strlen -4 :
            # 4 只是一个阈值，去掉标点符号和一些东西
            break

    count = 0
    for item in maxlen_list :
        count += item
    if count < strlen / 2 or  count < strlen - 6:
        new_roles.append({"index": "角色标注有问题，另外处理！！" + str(count) + '--' + str(strlen), "arguments": []})
        new_roles.append({"index": -1, "arguments": []})

    return new_roles

# 这个代码和handleRoleToOne一样，重点处理删除重复部分，
# 主要是handleRoleToOne处理后的roles访问index和argument的方式变了
def handleRoleToOneTwice(words,roles):
    strlen = len(words)
    new_roles = []
    maxLastIndex = -1
    minLastIndex = strlen
    for role , i in zip(roles,range(len(roles))):
        maxIndex = -1
        minIndex = strlen
        new_arguments = []
        for arg in role['arguments']:
            startIndex = arg.range.start
            endIndex = arg.range.end
            if startIndex <= minLastIndex and minLastIndex <= maxLastIndex and maxLastIndex <= endIndex:
                if len(new_roles) > 0:
                    print('2删除上一个role')
                    new_roles.pop()
            if maxLastIndex >= endIndex :
                print('2跳过此次的',startIndex,' ', endIndex)
                continue
            new_arguments.append(arg)
            maxIndex = max(maxIndex, endIndex)
            minIndex = min(minIndex, startIndex)

        if maxIndex != -1 :
            maxLastIndex = maxIndex
        if minIndex != strlen:
            minLastIndex = minIndex
        if len(new_arguments) != 0:
            new_roles.append({"index":role['index'],"arguments":new_arguments})

    return new_roles

#  科目一和科目四处理，换一种方法：针对数据一个个来，放到一个字典里，多行输出
def newHandleRoleTag(words,roles):
    strlen = len(words)
    dist_role = {}
    for role, i in zip(roles, range(len(roles))):
        v_index = role.index
        for arg in role.arguments:
            startIndex = arg.range.start
            endIndex = arg.range.end
            key = str(v_index) + '-' + str(startIndex) + '-' + str(endIndex)
            #  这个区间 不在已有的区间中
            if not keyInDist(startIndex,endIndex,dist_role):
                dist_role[key] = arg


    # 是否是个大区间，包括了前面的区间，要删除有交集的区间
    filter_dist_role = {}
    for key1 in dist_role:
        arr1 = key1.split('-')
        start1 = arr1[1]
        end1 = arr1[2]
        flag = 0
        for key2 in dist_role:
            if key1 == key2:
                # 不与自身对比
                continue
            else:
                arr2 = key2.split('-')
                if int(arr2[1]) <= int(start1) and int(end1) <= int(arr2[2]):
                    flag = 1
                    break
        if flag == 0:
            filter_dist_role[key1] =  dist_role[key1]

    res =  getAllVType(strlen,filter_dist_role)
    return  res


# 这个区间是否已经存在了
def keyInDist(start,end,dist):
    for key in dist:
        arr = key.split('-')
        if int(arr[1]) <= start and end <= int(arr[2]):
            # 已经包括这个区间
            return True
    return  False

# 把字典中的数据合并成多个role :[{'1-2-3': arguments中的一项arg},{...}]
def getAllVType(strlen,dists):
    # 注意键值都是字符串
    max_len = 0
    new_roles = []
    v_keys = set()
    arguments = []
    for key in dists:
        role = {"index": '', "arguments": []}
        arr = key.split('-')
        max_len += int(arr[2]) - int(arr[1]) + 1
        now_key = arr[0]
        if now_key not in v_keys:
            max_len += 1
            v_keys.add(now_key)
            role['index'] = int(now_key)
            role['arguments'].append(dists[key])
            new_roles.append(role)
        else :
            for item in new_roles:
                if item['index'] == int(now_key) :
                     item['arguments'].append(dists[key])

    # arguments 按从小到大排序
    for item in new_roles:
        item['arguments'].sort(key=argIncrease,reverse=False)

    # 按照index的大小排序
    new_roles.sort(key=indexIncrease, reverse=False)

    # 去除一些角色标注有问题的
    if max_len <= strlen / 2 + 1 or max_len <= strlen - 5:
        new_roles.append({"index": "角色标注有问题，另外处理！！" + str(max_len) + '--' + str(strlen), "arguments": []})
        new_roles.append({"index": -1, "arguments": []})

    return new_roles

def indexIncrease(elem):
    return elem['index']

def argIncrease(elem):
    return elem.range.start