''''''
'''检查对比过的文件'''
# /**
#  * 关键词词图的基类，目前有如下实现：
#  *
#  * 词语位置加权的词图实现WeightedPositionWordGraph, 参考：夏天. 词语位置加权TextRank的关键词抽取研究. 现代图书情报技术, 2013, 29(9): 30-34.
#  *
#  * @author 夏天
#  * @organization 中国人民大学信息资源管理学院
#  */

import commons.SegmentFactory as SegmentFactory
import keywords.SpecifiedWeight as SpecifiedWeight
# from keywords.graph.PageRankGraph import PageRankGraph
from keywords.graph.WordNode import WordNode
from commons.log import get_logger

class WordGraph:

    def __init__(self):
        # 是否在后面的词语中加上指向前面词语的链接关系
        self.linkBack = True
        # 如果读取的单词数量超过该值，则不再处理以后的内容，以避免文本过长导致计算速度过慢,这个现在不管用
        self.maxReadableWordCount = 500000
        # 读取的词语的数量
        self.readWordCount = 0
        self.__wordNodeMap = {}

        self._logger = get_logger(' ')
        pass

    def getWordDictSize(self):
        """获取字典大小"""
        return len(self.__wordNodeMap)
    def setWordDictKey(self, key, value):
        """存在，更新字典值；不存在，新添加一个值"""
        self.__wordNodeMap[key]=value
    def getWordDictValue(self,key):
        """获取value, 不存在时返回None"""
        if key in list(self.__wordNodeMap.keys()):
            return self.__wordNodeMap[key]
        else:
            return None
    def showWordDict(self):
        print(list(self.__wordNodeMap.keys()))
    def _isExistsKey(self,key):
        """判断一个key在字典中是否存在"""
        return key in list(self.__wordNodeMap.keys())
    def getWordDictYield(self):
        """返回每一个对key，value值"""
        for key, value in self.__wordNodeMap.items():
            yield key,value
    def getWordKeysList(self):
        return list(self.__wordNodeMap.keys())
    def getWordValuesList(self):
        return list(self.__wordNodeMap.values())
    # 直接通过传入的词语和重要性列表构建关键词图,这个还需要用到的时候再看
    # def build(self, wordsWithImportanceDict):
    #     """
    #
    #     :param wordsWithImportanceDict: 词典
    #     :return:
    #     """
    #
    #     lastPosition = -1
    #     for i,word in enumerate(wordsWithImportanceDict):
    #         importance = wordsWithImportanceDict[word]
    #
    #         # 如果已经读取了最大允许的单词数量，则忽略后续的内容
    #         self.readWordCount+=1
    #         if (self.readWordCount > self.maxReadableWordCount):
    #             return
    #
    #         wordNode = self.getWordDictValue(word)
    #
    #         if wordNode is None:
    #             # 如果额外指定了权重，则使用额外指定的权重代替函数传入的权重
    #             specifiedWeight = SpecifiedWeight.getWordWeight(word, 0.0)
    #             if specifiedWeight < importance:
    #                 specifiedWeight = importance
    #
    #             wordNode = WordNode(word, pos = "IGNORE", count=0, importance=specifiedWeight)
    #             # 添加一个字典结点
    #             self.setWordDictKey(word, wordNode)
    #             # self.wordNodeMap[word] = wordNode
    #         elif wordNode.getImportance() < importance:
    #             wordNode.setImportance(importance)
    #
    #         # 自增
    #         wordNode.incCount()
    #         # wordNode.setCount(wordNode.getCount()+1)
    #
    #         # 加入邻接点
    #         if lastPosition >=0:
    #             t = list(wordsWithImportanceDict.keys())[lastPosition]
    #             lastWordNode = self.getWordDictValue(t)
    #             # lastWordNode = self.wordNodeMap[t]
    #
    #             if self.linkBack:
    #                 # 加入逆向链接
    #                 wordNode.addAdjacentWord(lastWordNode.getName())
    #             pass
    #
    #             if lastPosition == i-1:
    #                 if wordNode.getPos().startswith("n") and ( lastWordNode.getPos()=="adj" or  lastWordNode.getPos().startswith("n")):
    #                     wordNode.addLeftNeighbor(lastWordNode.getName())
    #                     lastWordNode.addRightNeighbor(wordNode.getName())
    #                 pass
    #             pass
    #         pass
    #
    #         lastPosition = i
    #     pass

    def getLeftNeighborsList(self, word):
        """返回一个左相邻，"""
        res = self.getWordDictValue(word)
        if res is None:
            return []
        return res.getLeftNeighbors()

    def getRightNeighborsList(self, word):
        res = self.getWordDictValue(word)
        if res is None:
            return None
        if res.getPos()=="nr":
            # 相当于不合并人名后面的词语
            return []
        else:
            return res.getRightNeighbors()

    '''这个是构建图，本不应该在这里新建的，因为每一个算法的构建方法都不太一样。具体的算法都应该在继承这个图类的基础上构建自己 的图'''
    def build2(self, text, importance):
        # 切分句子并进行词性标记，words是一个词性词曲
        wordTupleList = SegmentFactory.getSegmentTag(text)
        self._logger.info("++++build2+++++++++ 分词这么多个：%s"%(wordTupleList.__len__()))
        # print("内容：",text)
        # print("分词：", wordTupleList)
        # print(' '.join(wordDict.keys()))

        '''统计下过滤掉多少个词'''
        guoluCount=0
        '''统计加入计算的词信息'''
        t_addWord=[]
        lastPosition = -1
        for i,segWord in enumerate(wordTupleList):
            word= segWord[0]
            pos = segWord[1]

            # w表示标点符号
            if 'w'.lower() == pos.lower():
                guoluCount+=1
                continue

            #词太短，关键词没有单字的
            if len(word)<2:
                guoluCount += 1
                continue
            #名词，形容词，动词
            if pos.startswith('n') or pos.startswith('a') or pos.startswith('v') or pos.startswith('x') or pos.startswith('un'):
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
                    # if specifiedWeight>1:
                        # print(specifiedWeight,word )

                    if pos=='x':
                        specifiedWeight = specifiedWeight*2
                    # "ns": "地名" "nr": "人名"
                    if(pos == "ns" or pos  == "nr") :
                        specifiedWeight = specifiedWeight*1.3
                    #动词
                    elif (pos.startswith("v")) :
                        specifiedWeight *= 0.5

                    wordNode = WordNode(word, pos, 0, specifiedWeight)
                    self.setWordDictKey(word, wordNode)

                elif (wordNode.getImportance() < importance) :
                    # 如果已经存在
                    wordNode.setImportance(importance)

                # wordNode.setCount(wordNode.getCount()+1)
                #词出现次数加1
                wordNode.incCount()
                t_addWord.append("%s/%s/权重%d/计数%d "%(word ,pos, wordNode.getImportance(), wordNode.getCount()))


                # //加入邻接点
                if (lastPosition >= 0):
                    t_word =wordTupleList[lastPosition][0]
                    lastWordNode = self.getWordDictValue(t_word)
                    lastWordNode.addAdjacentWord(word)

                    if (self.linkBack):
                        # //加入逆向链接
                        wordNode.addAdjacentWord(lastWordNode.getName())


                    if (lastPosition == i - 1):
                        if(wordNode.getPos().startswith("n") and
                                (lastWordNode.getPos() == "adj" or lastWordNode.getPos().startswith("n"))) :
                            wordNode.addLeftNeighbor(lastWordNode.getName())
                            lastWordNode.addRightNeighbor(wordNode.getName())

                lastPosition = i
            else:
                guoluCount+=1
            pass

        self._logger.info('过滤词：%d 添加词：%d'%(guoluCount, self.readWordCount))
        self._logger.info(str(t_addWord))
        pass

    # /**
    #  * 设置最大可以读取的词语数量
    #  *
    #  * @param maxReadableWordCount
    #  */
    def setMaxReadableWordCount(self, maxReadableWordCount):
        self.maxReadableWordCount = maxReadableWordCount
