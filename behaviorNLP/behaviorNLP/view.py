import os

from django.http import HttpResponse, FileResponse
from django.shortcuts import render
#导入,可以使此次请求忽略csrf校验
from django.views.decorators.csrf import csrf_exempt
import random
import string
import json
from behaviorNLP.nlp.txtForTag import initByType
from behaviorNLP.nlp.tkData.dataFilter import startK1K4Filter
from behaviorNLP.nlp.utils.db_crud import startSearchBehavior
# 数据库
from behaviorNLP import models


def index(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'index.html', context)

def hello(request):
    a = models.Condition.objects.create(con_name='绿灯亮')
    print(a.id, a.__str__())
    return HttpResponse("Hello world hehe! ")


def search(request):
    request.encoding='utf-8'
    print(request.GET)
    if 'q' in request.GET and request.GET['q']:
        message = '你搜索的内容为: ' + request.GET['q']
    else:
        message = '你提交了空表单'
    return HttpResponse(message)

# 接收请求数据
@csrf_exempt
def startSafe(request):
    request.encoding = 'utf-8'
    json_result = json.loads(request.body.decode('utf-8'))
    # 读取数据
    textType = json_result['data']['textType']
    userWords = json_result['data']['userWords']

    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    print(textType, type(userWords),salt)

    # 开始生成标注
    filePath = initByType(0,userWords,salt)
    data = {'code':200,'type':textType,'msg':"成功生成",'url':filePath}
    data = json.dumps(data)
    return HttpResponse(data)

@csrf_exempt
def startTK(request):
    request.encoding = 'utf-8'
    json_result = json.loads(request.body.decode('utf-8'))
    # 读取数据
    textType = json_result['data']['textType']
    k1Words = json_result['data']['k1Words']
    k4Words = json_result['data']['k4Words']

    # 生成8位随机字符
    salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    # 题库过滤
    isFilterSuccess = startK1K4Filter(k1Words,k4Words,salt)
    # 开始生成标注
    if isFilterSuccess == 1 :
        filePath = initByType(0, 0,salt)
        print(textType, k1Words,k4Words)
        data = {'code':200,'type': textType, 'msg':"成功生成",'url':filePath}
        data = json.dumps(data)
    else :
        data = {'code': 400, 'type': textType, 'msg': "题库过滤失败"}
        data = json.dumps(data)
    return HttpResponse(data)

# 下载文件 post方式
@csrf_exempt
def downloadTxt(request):
    request.encoding = 'utf-8'
    json_result = json.loads(request.body.decode('utf-8'))
    url = json_result['data']['url']
    # url = 'behaviorNLP/static/safeData/Lcpixd5EroleTagRules.txt'
    file = open(url, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="roleRules.txt"'
    # 下载之后就删除
    try:
        os.remove(url)
    except IOError:
        print("Error: 删除下载文件失败")
    return response

# 下载 get方式
@csrf_exempt
def downloadTxtGet(request):
    request.encoding = 'utf-8'
    if 'q' in request.GET and request.GET['q']:
        url =  request.GET['q']
    # url = 'behaviorNLP/static/safeData/Lcpixd5EroleTagRules.txt'
    file = open(url, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="roleRules.txt"'
    # 下载之后就删除 --这里写入的时间很慢，会出现下载之后还没写完的情况
    try:
        os.remove(url)
    except IOError:
        print("Error: 删除下载文件失败")
    return response



@csrf_exempt
def startSearch(request):
    request.encoding='utf-8'
    json_result = json.loads(request.body.decode('utf-8'))
    keyWords = json_result['data']['keyWords']
    result = startSearchBehavior(keyWords)
    data = {'code': 200,  'data': result}
    return HttpResponse(data)
