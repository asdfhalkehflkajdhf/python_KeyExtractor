


from commons.xml2dict import XML2Dict
import os
import jieba
import commons.SegmentFactory as SegmentFactory

import numpy


class WordStatisticalInfo():
    def __init__(self):
        # {word: [占比，分布]}
        # 分布有三个分段，6种情况
        self._wordDict={}

        # {'q': 318, 'z': 195, 'h': 327, 'qz': 772, 'zh': 532, 'qzh': 3245}
        self._wordLocal = {'q': 1.06, 'z': 1.04, 'h': 1.06, 'qz': 1.15, 'zh': 1.10, 'qzh': 1.60}

    def _get分布(self, len, s, e):
        L = numpy.array([0, len / 3, len / 3 * 2, len])
        Lt = abs(numpy.array(L) - s)
        L1 = list(Lt).index(Lt.min())
        Lt = abs(numpy.array(L) - e)
        L2 = list(Lt).index(Lt.min())
        # print(L1,'\t', L2,'\t', t)

        if L1 == 0:
            if L2 == 1:
                res = self._wordLocal['q']
            elif L2 == 2:
                res = self._wordLocal['qz']
            else:
                res = self._wordLocal['qzh']
        elif L1 == 1:
            if L2 == 2:
                res = self._wordLocal['z']
            else:
                res = self._wordLocal['zh']
        elif L1 == 2:
            res = self._wordLocal['h']
        else:
            res = 1
        return res

    def 分析(self, content):
        """"""
        contentLen = len(content)
        '''分词'''
        resList = SegmentFactory.getSegmentTag(content)
        '''去停用词'''
        SegmentFactory.get停用词(resList)
        '''合并'''
        SegmentFactory.get合并词(resList,isDelWord=False)
        '''去单字'''
        SegmentFactory.get去单字(resList)
        '''计算词距'''

        t = len(content)

        for it in resList:
            if it[0] not in  list(self._wordDict.keys()):
                s = content.find(it[0])
                e = content.rfind(it[0])
                self._wordDict[it[0]]=[(e -s)/t, self._get分布(t, s, e), (e -s)/t*self._get分布(t, s, e), it[1]]

        '''排序'''
        t = sorted(self._wordDict.items(), key=lambda x:x[1][2], reverse=True)
        self._wordDict.clear()
        for i,(key, value) in enumerate(t):
            self._wordDict[key]=value+[i]
        '''输出结果'''

    def getWord(self,word):
        """[word,词距，词分布，排名]"""
        try:
            b = list(self._wordDict.keys()).index(word)
        except:
            # print(word, "不在字典中")
            b = None
        try:
            res = self._wordDict[word]
        except:
            res = [None, None]
        return [word]+res+[b]

    def showAll(self):
        print(self._wordDict)

if __name__ == "__main__":
    # filePath = input("input file:")
    filePath = '../data/articles.xml'
    # filePath = 'data/test.txt'
    if not os.path.exists(filePath):
        print("文件[%s]不存在，重新输入" % (filePath))

    xml = XML2Dict()
    r = xml.parse(filePath)

    stat = WordStatisticalInfo()

    from  pprint import pprint
    data = r.articles.article
    # pprint(data)
    stat.分析(data[2].content)

    print("输出合并词后，按词在文本中位置权重{word: [占比，分布，权重，序]}")
    stat.showAll()

    print()
    print("输出关键词信息")
    for key in list(data[2].tags.split(',')):
        print(stat.getWord(key))


