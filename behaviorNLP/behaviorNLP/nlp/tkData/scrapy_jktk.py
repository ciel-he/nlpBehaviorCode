#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-06-06 15:29:40
# @Author  : heye (heye1109@qq.com)
# @Blog    : https://blog.csdn.net/HYeeee
#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib.request as req
from urllib.parse import urlencode
 
#----------------------------------
# 驾照题库调用示例代码 － 聚合数据
# 在线接口文档：http://www.juhe.cn/docs/183
# 这里先获取所有的题库
#----------------------------------
 
def main():
 
    #配置您申请的APPKey
    appkey = "0f246553ab1506bce61dab2160e03658"
 
    #1.题库接口
    getAllSubject(appkey,"1","GET") #科目1
    getAllSubject(appkey,"4","GET") #科目4

 
#题库接口
def getAllSubject(appkey,km, m="GET"):
    url = "http://api2.juheapi.com/jztk/query"
    params = {
        "key" : appkey, #您申请的appKey
        "subject" : km, #选择考试科目类型，1：科目1；4：科目4
        "model" : "c1", #驾照类型，可选择参数为：c1,c2,a1,a2,b1,b2；当subject=4时可省略
        "testType" : "order", #测试类型，rand：随机测试（随机100个题目），order：顺序测试（所选科目全部题目）
 
    }
    params = urlencode(params)
    if m =="GET":
        f = req.urlopen("%s?%s" % (url, params))
    else:
        f = req.urlopen(url, params)
 
    content = f.read()
    
    # 把字符串转成对象
    res = json.loads(content.decode())
    # 全部题保存到json文件中=
    with open('k'+km+'.json','a',encoding='utf-8') as f:
        json.dump(res, f, indent=4, ensure_ascii=False)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            # print res["result"]
            pass
        else:
            print ("%s:%s" % (res["error_code"],res["reason"]))
    else:
        print( "request api error")
 
# def handleTK(res):
# 	for problem in res:
# 		if problem['url'] == '':


# 		else:
# 			'''图片题暂时不处理'''
# 			pass

#answer字段对应答案
# def request2(appkey, m="GET"):
#     url = "http://api2.juheapi.com/jztk/answers"
#     params = {
#         "key" : appkey, #您申请的appk
 
#     }
#     params = urlencode(params)
#     if m =="GET":
#         f = urllib.urlopen("%s?%s" % (url, params))
#     else:
#         f = urllib.urlopen(url, params)
 
#     content = f.read()
#     res = json.loads(content)
#     if res:
#         error_code = res["error_code"]
#         if error_code == 0:
#             #成功请求
#             print( res["result"])
           

#         else:
#             print("%s:%s" % (res["error_code"],res["reason"]))
#     else:
#         print ("request api error")
 
 
 
if __name__ == '__main__':
    main()