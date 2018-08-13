''''''
'''检查对比过的文件'''
# /**
#  * 词语位置加权实现的关键词词图，词性分析
#  *

#  */
import numpy
from keywords.graph.WordGraph import WordGraph
from keywords.graph.PageRankGraph import PageRankGraph
import commons.SegmentFactory as SegmentFactory
import keywords.SpecifiedWeight as SpecifiedWeight
from keywords.graph.WordNode import WordNode
from commons.log import get_logger

import g_config

class MyWPWordGraph(WordGraph):

    def __init__(self, paramAlpha = 0.1, paramBeta = 0.8, paramGamma = 0.1, linkBack=False):
        '''初始化父类的属性'''
        super().__init__()
        # 词语的覆盖影响力因子
        self.paramAlpha = paramAlpha
        # 词语的位置影响力因子
        self.paramBeta = paramBeta
        # 词语的频度影响力因子
        self.paramGamma = paramGamma

        ## 是否在后面的词语中加上指向前面词语的链接关系WordGraph,继承过来的
        self.linkBack = linkBack

        # 词分布
        self._wordLocal = {'q': 1.06, 'z': 1.04, 'h': 1.05, 'qz': 1.15, 'zh': 1.10, 'qzh': 1.60}

        self._logger = get_logger("MyWPWordGraph")
        # 日志输出默认为关闭
        self._logger.disabled = True

    # def _get分布(self, len, s, e):
    #     L = numpy.array([0, len / 3, len / 3 * 2, len])
    #     Lt = abs(numpy.array(L) - s)
    #     L1 = list(Lt).index(Lt.min())
    #     Lt = abs(numpy.array(L) - e)
    #     L2 = list(Lt).index(Lt.min())
    #     # print(L1,'\t', L2,'\t', t)
    #
    #     if L1 == 0:
    #         if L2 == 1:
    #             res = self._wordLocal['q']
    #         elif L2 == 2:
    #             res = self._wordLocal['qz']
    #         else:
    #             res = self._wordLocal['qzh']
    #     elif L1 == 1:
    #         if L2 == 2:
    #             res = self._wordLocal['z']
    #         else:
    #             res = self._wordLocal['zh']
    #     elif L1 == 2:
    #         res = self._wordLocal['h']
    #     else:
    #         res = 1
    #     return res
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
                # res = 1.06 * 1.04 * 1.15
                res = self._wordLocal['qz']
            else:
                # res = 1.06 * 1.06 * 1.04 * 1.1 * 1.15 *1.6
                res = self._wordLocal['qzh']
        elif L1 == 1:
            if L2 == 2:
                res = self._wordLocal['z']
            else:
                # res = 1.06 * 1.04 * 1.1
                res = self._wordLocal['zh']
        elif L1 == 2:
            res = self._wordLocal['h']
        else:
            res = 1
        return res

    def _get位置分布权重(self, word, content, specifiedWeight):
        # 词位置统计   [词距占比，位置分布]
        t = len(content)
        if t<50:
            return specifiedWeight

        s = content.find(word)
        e = content.rfind(word)

        if (e - s)==0:
            return 0.1*specifiedWeight

        # 其他组合都不如以下配置好用
        位置分布权重 = (e - s) / t
        # return 位置分布权重
        return 位置分布权重*self._get分布(t, s, e)*specifiedWeight

    def _get词性权重(self, pos, specifiedWeight):
        """
        获取词性权重设置
        :param pos:
        :param specifiedWeight:
        :return:
        """
        '''这个配置的结果为 是在合并词删除旧词 夏天数据 res: p=0.380435 r=0.275410 f=0.319513'''
        # if pos=='x':
        #     specifiedWeight = specifiedWeight*2
        # # "ns": "地名" "nr": "人名"
        # if pos =='n':
        #     specifiedWeight *= 2
        # elif(pos == "ns" ):
        #     specifiedWeight = specifiedWeight*1.3
        # elif  pos  == "nr":
        #     specifiedWeight *= 1.2
        # #动词
        # if (pos.startswith("v")) :
        #     specifiedWeight *= 1.2

        '''下次跑下结果 是在合并词删除旧词 夏天数据 res: p=0.382065 r=0.276590 f=0.320882'''
        if pos == 'x':
            specifiedWeight = specifiedWeight * 2
        # "ns": "地名" "nr": "人名"
        # n占比： 0.4414855072463768 # v占比： 0.13496376811594202 # nr占比： 0.10235507246376811 # ns占比： 0.08333333333333333 # nz占比： 0.026992753623188405 # j占比： 0.044384057971014496
        # [1.52966746  1.16192132  1.12279939  1.09997827  1.03238426  1.05324929]
        if pos == 'n':
            specifiedWeight *= 1.5
        # 动词
        if (pos.startswith("v")):
            specifiedWeight *= 1.2
        if pos.startswith("nr"):
            specifiedWeight *= 1.15
        if (pos == "ns"):
            specifiedWeight *= 1.1
        if pos == 'nz':
            specifiedWeight *= 1.05
        if (pos.startswith("j")):
            specifiedWeight *= 1.1
        return specifiedWeight

    def setDebug(self, value):
        self._logger.disabled = not value


    def myWpBuild(self, text, importance):
        # 切分句子并进行词性标记，words是一个词性词曲
        wordTupleList = SegmentFactory.getSegmentTag(text)

        self._logger.info("分词这么多个：%d"%(wordTupleList.__len__()))
        # print("内容：",text)
        # print("分词：", wordTupleList)
        # print(' '.join(wordDict.keys()))

        SegmentFactory.get停用词(wordTupleList)
        if g_config.conf_我的方法是否合并词:
            SegmentFactory.get合并词(wordTupleList, isDelWord=g_config.conf_在合并词时是否删除旧词)
        SegmentFactory.get去单字(wordTupleList)

        '''统计下过滤掉多少个词,输出信息'''
        guoluCount=0
        '''统计加入计算的词信息'''
        t_addWord=[]
        for i,segWord in enumerate(wordTupleList):
            wordList = [segWord[0]]+segWord[-1]
            # word= segWord[0]
            pos = segWord[1]

            # w表示标点符号
            if 'w'.lower() == pos.lower():
                guoluCount+=1
                continue

            for word in wordList:
                #词太短，关键词没有单字的
                if len(word)<2:
                    guoluCount += 1
                    continue

                wordNode = self.getWordDictValue(word)

                # 如果已经读取了最大允许的单词数量，则忽略后续的内容
                self.readWordCount+=1
                if (self.readWordCount > self.maxReadableWordCount) :
                    return

                # 新词不，在字典中，
                if wordNode is None:
                    # 如果额外指定了权重，则使用额外指定的权重代替函数传入的权重,
                    # 一般都是0
                    specifiedWeight = SpecifiedWeight.getWordWeight(word, 0.0)
                    if (specifiedWeight < importance):
                        specifiedWeight = importance

                    specifiedWeight = self._get词性权重(pos, specifiedWeight)

                    specifiedWeight = self._get位置分布权重(word, text,specifiedWeight)

                    # 生成一个新的词项，并添加到词典中
                    wordNode = WordNode(word, pos, 0, specifiedWeight)
                    self.setWordDictKey(word, wordNode)

                elif (wordNode.getImportance() < importance) :
                    # 如果已经存在,这个最小位置权重，
                    wordNode.setImportance(importance)

                # wordNode.setCount(wordNode.getCount()+1)
                #词出现次数加1
                wordNode.incCount()

                '''统计参加计算的词，和权重，计数'''
                t_addWord.append("%s/%s/权重%d/计数%d "%(word ,pos, wordNode.getImportance(), wordNode.getCount()))

                # //加入邻接点,第一个词跳过
                if (  i > 0):
                    # 能进来的都不是第一个词,

                    # 获取上一次的词喉选词
                    t_word =wordTupleList[i-1][0]
                    lastWordNode = self.getWordDictValue(t_word)
                    #把当前词添加到邻接点上，是为了计算覆盖重要性的。就是看看，连接他的词多不多
                    lastWordNode.addAdjacentWord(word)

                    if (self.linkBack):
                        # //加入逆向链接，把上一个词添加到当前邻接点中
                        wordNode.addAdjacentWord(lastWordNode.getName())

                else:
                    guoluCount+=1
            pass #for word in wordList:
        pass #for i,segWord in enumerate(wordTupleList):
        # 输出调试信息
        self._logger.info('过滤词：%d 添加词：%d'%(guoluCount, self.readWordCount))
        self._logger.info(str(t_addWord))
    pass #def myWpBuild(self, text, importance):

    def makePageRankGraph(self):
        """返回的是一个PageRankGraph类"""

        #初始化数据,wordNodeMap
        wordDictSize = self.getWordDictSize()
        values = [0.1/wordDictSize]*wordDictSize
        matrix = numpy.zeros((wordDictSize, wordDictSize))

        for i, (_, nodeFrom) in enumerate(self.getWordDictYield()):
            if nodeFrom is None:
                continue

            adjacentWordsDict = nodeFrom.getAdjacentWords()

            totalImportance = 0.0 # // 相邻节点的节点重要性之和
            totalOccurred = 0 #; // 相邻节点出现的总频度

            for w in adjacentWordsDict:
                totalImportance += self.getWordDictValue(w).getImportance()
                totalOccurred+=self.getWordDictValue(w).getCount()

            for j,(wordTo, nodeTo) in enumerate(self.getWordDictYield()):
                if nodeTo is None:
                    continue

                # 判断p集合对象中是否包含指定的键名。如果Map集合中包含指定的键名，则返回true，否则返回false。
                if wordTo in list(adjacentWordsDict.keys()):
                    # 计算i到j的转移概率
                    partA = 1/ len(adjacentWordsDict)
                    partB = nodeTo.getImportance() / totalImportance
                    partC = nodeTo.getCount() / totalOccurred

                    matrix[j][i] = partA * self.paramAlpha + partB * self.paramBeta + partC * self.paramGamma

        return PageRankGraph(self.getWordKeysList(), values, matrix)