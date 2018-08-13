# /**
#  * 中文停用词表,全局变量，测试过
#  *
#  * @date Apr 29, 2016 17:53
#  */

import os
import codecs
from commons import log

#全局变量，在使用前，使用global声明下
global __global_stopKeywordsDict
__global_stopKeywordsDict = []


def getStopKeywords():
    global __global_stopKeywordsDict
    return __global_stopKeywordsDict

def addStopKeywords( pathList):
    """文本，参数是一个list []"""
    logger = log.get_logger("StopKeyword")

    global __global_stopKeywordsDict
    """添加换行，停用词，文本中不好配置，加在这里"""
    __global_stopKeywordsDict.append('\n')
    __global_stopKeywordsDict.append(' ')
    for path in pathList:
        if os.path.isfile(path):
            f = codecs.open(path, 'r', encoding='utf8')
            text = f.read()
            __global_stopKeywordsDict = __global_stopKeywordsDict +  list(text.split())
            # 去重
            __global_stopKeywordsDict = list(set(__global_stopKeywordsDict))
            f.close()
            logger.info("加载用户停用词：%s"%(path))
        else:
            logger.info("加载用户停用词失败：%s" % (path))
    logger.info("加载用户停用词完成：%s"%(pathList))


def isStopKeyword(word):
    global __global_stopKeywordsDict
    return word in __global_stopKeywordsDict



def _t1():
    print("初始化：",len(getStopKeywords()))
    addStopKeywords(['../resources/stoplists/cn.txt'])
    print("加载中文",len(getStopKeywords()))
    addStopKeywords(['../resources/stoplists/cn.txt'])
    print("重复加载加载中文，看是否去重",len(getStopKeywords()))

    t = isStopKeyword('“')
    print(t)

    addStopKeywords(['../resources/stoplists/en.txt'])
    print("加载英文，看是否添加新词",len(getStopKeywords()))

    print(getStopKeywords())

if __name__ == '__main__':
    _t1()

    print('+============================')
    a =['“二十八”','《地在要》']
    srcKey = a
    print(srcKey)
    for i in range(len(srcKey)).__reversed__():
        t  =  list(srcKey[i])
        for j in range(len(t)).__reversed__():
            if isStopKeyword(t[j]):
                del t[j]
        srcKey[i]=''.join(t)

    print(srcKey)