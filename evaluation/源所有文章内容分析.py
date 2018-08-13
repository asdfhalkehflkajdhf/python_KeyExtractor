

from commons.xml2dict import XML2Dict
import os
import jieba
import commons.SegmentFactory as SegmentFactory

import numpy
''''''

class WordStatisticalInfo():
    def __init__(self):
        # {'word':{
        #           {base:{len:, 分词个数:， 分词:， 词性:
        #                   }
        #             statList:[ [id:N, titleCount:N, contextCount:N] ....]
        #             }
        #
        self._totalWrodCount=0
        self._wordDict={}

        # 关键词，词组词性统计
        self._wordPosCount={}

        # {pos:count}
        self._wordPosList={}

        # 统计关键词在文章中出现的位置,前中后,
        self._wordLocal={'q':0, 'z':0, 'h':0, 'qz':0, 'zh':0, 'qzh':0}

    def addWord(self, word, articlesId, titleCount, contextCount):
        # 关键词计数
        self._totalWrodCount+=1
        if word in self._wordDict.keys():
            self._wordDict[word]['statList'].append([articlesId,titleCount, contextCount])
        else:
            word = SegmentFactory.get去中文标点符号(word)
            fenchi = SegmentFactory.getSegmentTag(word)
            t =''
            p =''
            for a,b,_,_ in fenchi:
                t = t+a+' '
                p = p+b+' '
            self._wordDict[word]={'len':len(word), 'num':len(fenchi), 'words':t, 'poss':p, 'statList':[[articlesId,titleCount, contextCount]]}

        # 词性统计
        t = self._wordDict[word]['words']
        p = self._wordDict[word]['poss']
        if  p not in list(self._wordPosCount.keys()):
            self._wordPosCount[p]=0
            self._wordPosList[p]=[]
        self._wordPosCount[p]+=1
        self._wordPosList[p].append(t+" "+str(articlesId))


    def getAvgLen(self):
        count = self._wordDict.__len__()
        lenCount = 0
        for key,value in self._wordDict.items():
            lenCount += value['len']

        print("平均长度：",lenCount/count)
        print("================================")

        return lenCount / count

    def getPosCount(self):
        """词性统计，看那个比较多"""
        # totNum = sum(list(self._wordPosCount.values()))
        res = sorted(self._wordPosCount.items(), key=lambda x:x[1], reverse=True)
        print("词性统计: ",res)
        print("前30%：")
        for i in range(int(res.__len__()*0.3)):
            print(res[i],'占比：',res[i][1]/self._totalWrodCount,'关键词+文本号(可以去 commons/xml2dict.py运行查看)：',  self._wordPosList[res[i][0]])
        print("================================")

        print()
        nr = 0
        ns = 0
        nz = 0
        j = 0
        n = 0
        v = 0
        for i in range(int(res.__len__() )):
            if res[i][0].startswith('n '):
                n+=res[i][1]
            if res[i][0].startswith('nr'):
                nr+=res[i][1]
            if res[i][0].startswith('ns'):
                ns += res[i][1]
            if res[i][0].startswith('nz'):
                nz += res[i][1]
            if res[i][0].startswith('j'):
                j += res[i][1]
            if res[i][0].startswith('v ') or res[i][0].startswith('vn '):
                v += res[i][1]
        print('n占比：', n / self._totalWrodCount,'v占比：', v / self._totalWrodCount,'nr占比：', nr / self._totalWrodCount, ' ns占比：', ns/self._totalWrodCount, ' nz占比：', nz/self._totalWrodCount, ' j占比：',j/self._totalWrodCount)

    def getLangWord(self):
        count = self._wordDict.__len__()
        len2Count = 0
        len3Count = 0
        len4Count = 0
        len5Count = 0
        len6Count = 0
        len_Count=0
        for key,value in self._wordDict.items():
            if value['len']==2:
                len2Count += 1
            if value['len']==3:
                len3Count += 1
            if value['len']==4:
                len4Count += 1
            if value['len']==5:
                len5Count+=1
            if value['len']==6:
                len6Count+=1
            if value['len']>6:
                len_Count+=1
        print("长词(2)：",len2Count, " 占比：",len2Count/count)
        print("长词(3)：",len3Count, " 占比：",len3Count/count)
        print("长词(4)：",len4Count, " 占比：",len4Count/count)
        print("长词(5)：",len_Count, " 占比：",len5Count/count)
        print("长词(6)：",len_Count, " 占比：",len6Count/count)
        print("长词(>6)：",len_Count, " 占比：",len_Count/count)

        print("================================ 总个数",count)
    def getNotContext(self):
        """没在文章中出现过的个数"""
        tCount = 0
        cCount = 0
        aCoutn = 0
        count=0
        for key,value in self._wordDict.items():
            for l in value['statList']:
                if l[1]==0:
                    tCount+=1
                if l[2]==0:
                    cCount+=1
                if l[1] == 0 and l[2]==0:
                    aCoutn +=1
                count+=1
        print("没在标题中出现的个数：",tCount, " 没在内容中出现的个数：",cCount, " 都没出现过：",aCoutn)
        print("词数出现总次数：",count)
        print("没在标题中出现的占比：", tCount/count, " 没在内容中出现的占比：", cCount/count, " 都没出现过占比：", aCoutn/count)
        print("================================")

    def getWordLocal(self):
        print("词出现位置统计：", self._wordLocal)
        print("权重：",end='')
        totCount = sum(list(self._wordLocal.values()))
        for key,value in self._wordLocal.items():
            print(key, ':',1+value/totCount, ' ',end='')
        print()
        print("================================")
    def setWordLocal(self, word, content):
        # 词位置统计
        t = len(content)
        L = numpy.array([0, t / 3, t / 3 * 2, t])

        s = content.find(word)
        e = content.rfind(word)

        Lt = abs(numpy.array(L) - s)
        L1 = list(Lt).index(Lt.min())
        Lt = abs(numpy.array(L) - e)
        L2 = list(Lt).index(Lt.min())
        # print(L1,'\t', L2,'\t', t)

        if L1 == 0:
            if L2 == 1:
                self._wordLocal['q'] += 1
            elif L2 == 2:
                self._wordLocal['qz'] += 1
            else:
                self._wordLocal['qzh'] += 1
        elif L1 == 1:
            if L2 == 2:
                self._wordLocal['z'] += 1
            else:
                self._wordLocal['zh'] += 1
        elif L1 == 2:
            self._wordLocal['h'] += 1

    def get在文章中出现次数(self):
        for key, value in self._wordDict.items():
            print(key, value['statList'])
        print('+++++++++++++++++++++++')

'''统计词频'''
# def 统计词频(file):
# print(b.count(a))

'''统计词长'''

'''统计词性'''

'''统计词性组合'''

if __name__ == "__main__":

    # filePath = input("input file:")
    # filePath = '../data/articles.xml'
    filePath = '../data/context.txt'
    if not os.path.exists(filePath):
        print("文件[%s]不存在，重新输入" % (filePath))
        assert False

    xml = XML2Dict()
    r = xml.parse(filePath)

    stat = WordStatisticalInfo()

    print('文章总数：',len(r.articles.article))
    for i,data in enumerate( r.articles.article):
        for key in list(data.tags.split(',')):
            stat.addWord(key, i, data.title.count(key), data.content.count(key))
            stat.setWordLocal(key, data.content)
    stat.getAvgLen()
    stat.getLangWord()
    stat.getNotContext()
    stat.getWordLocal()
    stat.getPosCount()
    # stat.get在文章中出现次数()