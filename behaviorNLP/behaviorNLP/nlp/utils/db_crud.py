import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "behaviorNLP.settings")# project_name 项目名称
django.setup()
# 上面这部分是让数据库可以在单独运行py文件时可调用setting
# 数据库
from behaviorNLP import models
"""
插入测试数据
"""
def insertConAndBeh(condition_list,behavior_list):
    # 从models文件中获取condition对象
    if len(behavior_list) == 0:
        return
    con_id_list = ''
    for item in condition_list:
        queryRes = models.Condition.objects.filter(con_name=item)
        # 如果已经有这个条件了，就获取他的id
        if len(queryRes) > 0:
            print(queryRes,queryRes[0].id)
            con_id_list += str(queryRes[0].id) + '/'
            continue
        # 否则，向数据库里面添加
        else:
            add_con = models.Condition.objects.create(con_name=item)
            con_id_list += str(add_con.id) + '/'
        print(con_id_list)

    # 写入行为表
    add_beh = models.Behavior.objects.create(con_id_list=con_id_list, detail_behavior=' '.join(behavior_list))


def startSearchBehavior(keyWords):
    # 查找到keywords相对应的con_id
    res = []
    for item in keyWords:
        queryRes = models.Condition.objects.filter(con_name__icontains=item)

    # 根据 id 查找 行为
    for re in queryRes:
        id = str(re.id) + '/'
        qr = models.Behavior.objects.filter(con_id_list=id)
        for item in qr:
            res.append(re.con_name + item.detail_behavior)
    return res