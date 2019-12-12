import re
str = '发现前方道路堵塞，正确的做法是按顺序停车等候'
searchRes = re.search('(?:正确的.*是)', str)
if searchRes:
    res = list(searchRes.span())
    print(res)