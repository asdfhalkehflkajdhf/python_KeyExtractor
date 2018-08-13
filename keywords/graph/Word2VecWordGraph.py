import commons.wordVector as wordVector
import numpy as np
from keywords.graph.WordGraph import WordGraph
from keywords.graph.PageRankGraph import PageRankGraph

# /**
#  * 融合Word2Vec的关键词抽取
#  */
class Word2VecWordGraph(WordGraph):
    def __init__(self,alpha=0.1, beta=0.8, gamma=0.1, linkBack=False):
        super().__init__()

        # //词语的覆盖影响力因子
        self.paramAlpha = alpha

        # //词语的位置影响力因子
        self.paramBeta = beta

        # //词语的频度影响力因子
        self.paramGamma = gamma

        self.linkBack = linkBack

    # /**
    #  * 计算词图节点两两之间的word2vec相似度，保存到二维数组中
    #  * @return
    #  */
    def word2vecSimMatrix(self,wordList):
        matrix = np.zeros((len(wordList),len(wordList)))
        for i ,iword in enumerate(wordList):
            for j, jword in enumerate(wordList):
                sim = wordVector.w2v_similarity(iword, jword)
                if sim is None:
                    sim = 1 / len(wordList)
                matrix[i][j] = matrix[j][i] = sim

        return matrix

    def makePageRankGraph(self):
        """返回PageRankGraph 类"""
        #初始化数据,wordNodeMap
        wordDictSize = self.getWordDictSize()
        values = [0.1/wordDictSize]*wordDictSize
        matrix = np.zeros((wordDictSize, wordDictSize))

        # //输出word2vec的重要性
        for i, (wordFrom, nodeFrom) in enumerate(self.getWordDictYield()):
            if nodeFrom is None:
                continue



        # //        float[][] simMatrix = word2vecSimMatrix(words);
        # //        float[] word2vecScores = new float[words.length];
        # //        float word2vecTotalScore = 0;
        # //        for(i=0; i<words.length; i++) {
        # //            float lineTotal = 0;
        # //            for(int j=0; j<words.length; j++) {
        # //                lineTotal += simMatrix[i][j];
        # //            }
        # //            word2vecScores[i] = lineTotal;
        # //            word2vecTotalScore += lineTotal;
        # //        }
            adjacentWordsDict = nodeFrom.getAdjacentWords()

            totalImportance = 0.0 # // 相邻节点的节点重要性之和
            totalOccurred = 0 #; // 相邻节点出现的总频度
            totalWord2VecScore = 0

            for w in adjacentWordsDict:
                totalImportance += self.getWordDictValue(w).getImportance()
                totalOccurred+=self.getWordDictValue(w).getCount()

                sim = wordVector.w2v_similarity(wordFrom, w)
                if sim is not None:
                    totalWord2VecScore += sim

            for j,(wordTo, nodeTo) in enumerate(self.getWordDictYield()):
                if nodeTo is None:
                    continue

                # 判断p集合对象中是否包含指定的键名。如果Map集合中包含指定的键名，则返回true，否则返回false。
                # //根据宁建飞 刘降珍:《融合 Word2vec 与 TextRank 的关键词抽取研究》一文设置的权重
                if wordTo in list(adjacentWordsDict.keys()):
                    # 计算i到j的转移概率
                    partA = 1/ len(adjacentWordsDict)
                    # partB = nodeTo.getImportance() / totalImportance
                    # partC = nodeTo.getCount() / totalOccurred
                    sim = wordVector.w2v_similarity(wordFrom, wordTo)
                    if sim is None:
                        # 作为0处理
                        partD = 0
                    else:
                        partD = sim/totalWord2VecScore
                    # matrix[j][i] = partA * self.paramAlpha + partB * self.paramBeta + partC * self.paramGamma
                    matrix[j][i] = 0.5 * partA + 0.5 * partD


#         //合并Word2Vec的相似度计算结果
# //        for (i = 0; i < words.length; i++) {
# //            String word1 = words[i];
# //
# //            for(int j=1; j<words.length; j++) {
# //                String word2 = words[j];
# //                double sim = word2Vec.similarity(word1, word2);
# //                matrix[i][j] = 0.8*matrix[i][j] + 0.2*sim;
# //                matrix[j][i] = 0.8*matrix[j][i] + 0.2*sim;
# //            }
# //        }

        return PageRankGraph(self.getWordKeysList(), values, matrix)
