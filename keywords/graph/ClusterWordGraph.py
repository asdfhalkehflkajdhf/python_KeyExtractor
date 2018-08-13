import commons.wordVector as wordVector
import numpy as np
from keywords.graph.WordGraph import WordGraph
from keywords.graph.PageRankGraph import PageRankGraph
from commons.log import get_logger
from sklearn.cluster import KMeans
# /**
#  * 融合Word2Vec的关键词抽取
#  *
#  */
class ClusterWordGraph(WordGraph):
    def __init__(self,alpha=0.33, beta=0.34, gamma=0.33, maxK=5, linkBack=False):
        super().__init__()
        # //词语的覆盖影响力因子
        self.paramAlpha = alpha

        # //词语的位置影响力因子
        self.paramBeta = beta

        # //词语的频度影响力因子
        self.paramGamma = gamma


        self.linkBack = linkBack
        self.maxK = maxK

        self._logger = get_logger("w2v")
    #
    # public double similarity(double[] vector1, double[] vector2) {
    #     float cosine = 0.0f;
    #     for (int i = 0; i < vector1.length; i++) {
    #         cosine += vector1[i] * vector2[i];
    #     }
    #
    #     return cosine;
    # }

    # /**
    #  * 对图的wordNodeMap包含的词语对应的word2vec词向量进行k-means聚类，然后根据每个词语到质心的距离，计算该词语在簇中的重要性
    #  *
    #  * @return
    #  */
    def _clustering(self):
        """返回一个词典"""
        instanceNames = []
        vectors = []

        lastPosition = -1

        for _,(word,_) in enumerate(self.getWordDictYield()):
            vec = wordVector.w2v_getVec(word)
            if vec is None:
                continue
            instanceNames.append(word)
            vectors.append(vec)

        vectors = np.array(vectors)
        '''字典为空，直接返回，不进行聚类'''
        if vectors.__len__()==0:
            # 没有结果
            self._logger.info("没有结果，直接返回空字典")
            return {}

        '''如果词个的数小于关键词提取的个数，则每一个词都做为关键词直接返回，不进行聚类'''
        if vectors.shape[0] < self.maxK:
            map={}
            for word in instanceNames:
                map[word] = 1
            return map

        k = max(self.maxK,2) #; //至少要分为两簇
        '''n_clusters:簇的个数，即你想聚成几类
init: 初始簇中心的获取方法
n_init: 获取初始簇中心的更迭次数，为了弥补初始质心的影响，算法默认会初始10个质心，实现算法，然后返回最好的结果。
max_iter: 最大迭代次数（因为kmeans算法的实现需要迭代）
tol: 容忍度，即kmeans运行准则收敛的条件
precompute_distances：是否需要提前计算距离，这个参数会在空间和时间之间做权衡，如果是True 会把整个距离矩阵都放到内存中，auto 会默认在数据样本大于featurs*samples 的数量大于12e6 的时候False,False 时核心实现的方法是利用Cpython 来实现的
verbose: 冗长模式（不太懂是啥意思，反正一般不去改默认值）
random_state: 随机生成簇中心的状态条件。
copy_x: 对是否修改数据的一个标记，如果True，即复制了就不会修改数据。bool 在scikit-learn 很多接口中都会有这个参数的，就是是否对输入数据继续copy 操作，以便不修改用户的输入数据。这个要理解Python 的内存机制才会比较清楚。
n_jobs: 并行设置
algorithm: kmeans的实现算法，有：’auto’, ‘full’, ‘elkan’, 其中 ‘full’表示用EM方式实现'''
        kmeans = KMeans(n_clusters=k)  # 构造聚类器


        kmeans.fit(vectors)  # 聚类
        clusterLabel = kmeans.labels_  # 获取聚类标签
        centroids = kmeans.cluster_centers_  # 获取聚类中心
        inertia = kmeans.inertia_  # 获取聚类准则的总和


        # //记录每个实例的重要性：可以用距离来衡量
        clusterInstDistances = [0]*len(clusterLabel)
        # //每个簇里面，所有实例到质心的总距离
        clusterTotalDistances = [0]*len(centroids)
        # //每个簇所拥有的实例数量
        clusterInstCounts = [0]*len(centroids)

        for i in range(len(clusterLabel)):
            c = clusterLabel[i]
            # //每个簇所拥有的实例数量 +1
            clusterInstCounts[c]+=1
            # 计算欧氏距离（Euclidean Distance）
            distance = np.linalg.norm(centroids[c] - vectors[i])
            # 每个实例
            clusterInstDistances[i] = distance
            # 总距离到质心的距离
            clusterTotalDistances[c] += distance

        map = {}
        for i in range(len(clusterLabel)):
            c = clusterLabel[i]
            v = clusterInstDistances[i] / clusterTotalDistances[c]

            #// 距离质心越远，携带的不同信息量越大，越重要。
            v = v * clusterInstCounts[c]

            #添加到词典
            map[instanceNames[i]]=v

        return map

    def makePageRankGraph(self):
        """返回PageRankGraph 类"""

        clusterImportanceMap = self._clustering()
        #初始化数据,wordNodeMap
        wordDictSize = self.getWordDictSize()
        values = [0.1/wordDictSize]*wordDictSize
        matrix = np.zeros((wordDictSize, wordDictSize))



        # //输出word2vec的重要性
        for i, (_, nodeFrom) in enumerate(self.getWordDictYield()):
            if nodeFrom is None:
                continue

            adjacentWordsDict = nodeFrom.getAdjacentWords()


            #    //相邻节点的节点重要性之和
            totalImportance = 0.0
            #       //相邻节点出现的总频度
            totalOccurred = 0

            totalClusterImportance = 0.0
            for w in adjacentWordsDict:
                totalImportance += self.getWordDictValue(w).getImportance()
                totalOccurred+=self.getWordDictValue(w).getCount()
                totalClusterImportance += clusterImportanceMap.get(w, 1.0)

            for j,(wordTo, nodeTo) in enumerate(self.getWordDictYield()):
                # 判断p集合对象中是否包含指定的键名。如果Map集合中包含指定的键名，则返回true，否则返回false。
                if wordTo in list(adjacentWordsDict.keys()):
                    # 计算i到j的转移概率
                    partA = 1/ len(adjacentWordsDict)
                    partB = nodeTo.getImportance() / totalImportance
                    # partC = nodeTo.getCount() / totalOccurred
                    partC = clusterImportanceMap.get(wordTo, 1.0) / totalClusterImportance
                    matrix[j][i] = partA * self.paramAlpha + partB * self.paramBeta + partC * self.paramGamma



        return PageRankGraph(self.getWordKeysList(), values, matrix)

