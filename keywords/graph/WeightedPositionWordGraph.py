''''''
'''检查对比过的文件'''
# /**
#  * 词语位置加权实现的关键词词图
#  *
#  * 参数说明请参考：夏天. 词语位置加权TextRank的关键词抽取研究. 现代图书情报技术, 2013, 29(9): 30-34.
#  * User: xiatian
#  * Date: 3/10/13 4:07 PM
#  */
import numpy as np
from keywords.graph.WordGraph import WordGraph
from keywords.graph.PageRankGraph import PageRankGraph

class WeightedPositionWordGraph(WordGraph):

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

    def makePageRankGraph(self):
        """返回的是一个PageRankGraph类"""

        #初始化数据,wordNodeMap
        wordDictSize = self.getWordDictSize()
        values = [0.1/wordDictSize]*wordDictSize
        matrix = np.zeros((wordDictSize, wordDictSize))

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