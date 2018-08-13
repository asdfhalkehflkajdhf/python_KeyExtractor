import configparser
import os
from enum import Enum

import commons.ChineseStopKeywords as ChineseStopKeywords
import commons.SegmentFactory as SegmentFactory
import keywords.SpecifiedWeight as SpecifiedWeight
from commons.log import get_logger
from keywords.graph.ClusterWordGraph import ClusterWordGraph
from keywords.graph.WeightedPositionWordGraph import WeightedPositionWordGraph
from keywords.graph.Word2VecWordGraph import Word2VecWordGraph

from commons import wordVector
import g_config

class GraphType(Enum):
    TF_IDF=0
    # // 传统的TextRank方法   夏天. 词语位置加权TextRank的关键词抽取研究. 现代图书情报技术, 2013, 29(9): 30-34.
    TextRank=1
    # // 词语位置加权 夏天. 词语位置加权 TextRank 的关键词抽取研究  2013,  区别于TextRank的是权值
    PositionRank_夏天2013=2
    ###################### 主要是以上的，不进行词向量加载#########################
    # // 融合Word2vec 与 TextRank的关键词抽取研究 NingJianfei 融合 Word2vec 与 TextRank 的关键词抽取研究
    NingJianfei=3
    # // 词向量聚类加权
    ClusterRank_李跃鹏=4
    # // 词向量聚类 + 位置加权  夏天 词向量聚类加权 TextRank 的关键词抽取
    ClusterPositionRank_夏天2016=5

    # 提出的基于  Word2Vec   的词向量聚类关键词抽取   李跃鹏, 金翠, 及俊川. 基于 Word2vec 的关键词提取算法
    # 没有实现

    # 我的
    MyWPRank = 6
    '''
    print(list(GraphType))
    [<GraphType.TF_IDF: 0>, <GraphType.TextRank: 1>, <GraphType.PositionRank_夏天2013: 2>, <GraphType.NingJianfei: 3>, <GraphType.ClusterRank_李跃鹏: 4>, <GraphType.ClusterPositionRank_夏天2016: 5>, <GraphType.MyWPRank: 6>]

    2. 枚举取值

    　2.1 通过成员的名称来获取成员

    Color['red']
    　2.2 通过成员值来获取成员

    Color(2)
    　2.3 通过成员，来获取它的名称和值

    red_member = Color.red

        4. 枚举比较

    　4.1 枚举成员可进行同一性比较

    Color.red is Color.red
    　　输出结果是：True

    Color.red is not Color.blue
    　　输出结果是：True

    　4.2 枚举成员可进等值比较

    Color.blue == Color.red
    　　输出结果是：False

    Color.blue != Color.red
    　　输出结果是：True

    　4.3 枚举成员不能进行大小比较

    Color.red < Color.blue
    '''

#判断是否为正确的模型
def getGraphType(type):
    """#获取的模型参数"""
    try:
        t = GraphType(type)
    except:
        t = None
    return t


class TextRankExtractor():

    def __init__(self):
        self.alpha_f = 0.1
        self.beta_f = 0.9
        self.gamma_f = 0.0
        self.lambda_f = 30.0
        self.maxReadWordCount_int = 2000
        self.mergeNeighbor_bool = False

        self.graphType = GraphType.TF_IDF
        self.logger = get_logger('TR_E')

        self.logger.info("使用 %s 提取包"%(self.graphType.name))

    def setExtractMode(self, typeid):
        graphType = getGraphType(typeid)
        if graphType is None:
            self.logger.info("选择模型失败 %s"%(str(GraphType)))
            return False
        else:
            self.graphType = graphType
        self.logger.info("使用 %s 提取包"%(self.graphType.name))

        if self.graphType == GraphType.NingJianfei or self.graphType == GraphType.ClusterRank_李跃鹏 or self.graphType == GraphType.ClusterPositionRank_夏天2016:
            res = wordVector.w2v_load(g_config.w2v_modePath, g_config.w2v_loadMode)
            if not res:
                self.logger.info("词向量加载失败%s %s"%(g_config.w2v_modePath, g_config.w2v_loadMode))
                return False
            self.logger.info("词向量加载成功%s %s" % (g_config.w2v_modePath, g_config.w2v_loadMode))

        return True

    #
    # /**
    #  * 设置人工指定的权重,这个用不到
    #  * @param word
    #  * @param weight
    #  */
    def setSpecifiedWordWeight(self,word, pos, weight):
        '''
        String word, String pos, float weight
        :param word:
        :param pos:
        :param weight:
        :return:
        '''
        SpecifiedWeight.setWordWeight(word, weight)
        # //同时插入分词程序
        # SegmentFactory.getSegment(None)
        SegmentFactory.insertUserDefinedWord(word, pos, 10)


    def extractAsList(self,title, content, topN):
        """返回关键词list [keyword1, keyword2, .....]"""
        keywords=[]
        if self.graphType == GraphType.TF_IDF:
            from jieba import analyse
            # tfidf = analyse.extract_tags
            TR = analyse.textrank
            resList = TR(title+content, topK=topN)
            return list(resList)
        elif self.graphType == GraphType.MyWPRank:
            from keywords.graph.MyWPWordGraph import MyWPWordGraph
            wordGraph = MyWPWordGraph(0.33, 0.34, 0.33, True)
            wordGraph.myWpBuild(title, self.lambda_f)
            wordGraph.myWpBuild(content, 1.0)
            g = wordGraph.makePageRankGraph()
            g.iterateCalculation(20, 0.15)
            g.quickSort()
            keywords = g.lableSortRes[0:topN]
            return keywords
        else:
            # 这个是夏天的算法
            # wordGraph = WordGraph()
            if self.graphType == GraphType.TextRank:
                # self.logger.info("使用TextRank提取")
                wordGraph = WeightedPositionWordGraph(1,0,0,True)
            elif self.graphType == GraphType.PositionRank_夏天2013:
                # self.logger.info("使用 PositionRank_夏天2013 提取")
                wordGraph = WeightedPositionWordGraph(0.33, 0.34, 0.33, True)
            elif self.graphType == GraphType.NingJianfei:
                # self.logger.info("使用 NingJianfei 提取")
                '''这个需要加载词向量'''
                wordGraph = Word2VecWordGraph(self.alpha_f, self.beta_f, self.gamma_f, True)
            elif self.graphType == GraphType.ClusterRank_李跃鹏:
                # self.logger.info("使用 ClusterRank_李跃鹏 提取")
                '''这个需要加载词向量'''
                wordGraph = ClusterWordGraph(0.5, 0, 0.5, topN, True)
            else:
                '''这个需要加载词向量'''
                wordGraph = ClusterWordGraph(0.33, 0.34, 0.33, topN, True)

            # 生成图,在标题出现，则权重为30
            wordGraph.build2(title, self.lambda_f)
            wordGraph.build2(content, 1.0)

            g = wordGraph.makePageRankGraph()

            g.iterateCalculation(20, 0.15)
            g.quickSort()
            count = 0
            limit = topN

            if self.mergeNeighbor_bool:
                # // 多挑选10个候选关键词，以尽可能使合并后的关键词数量也能够取到topN个
                limit +=10

            # 挑选前N个关键词
            for word in g.lableSortRes:
                if not ChineseStopKeywords.isStopKeyword(word):
                    keywords.append(word)
                    count += 1

                if count>limit:
                    # 挑选个数满足条件
                    break

            if not self.mergeNeighbor_bool:
                return keywords

            # // 对抽取出的关键词，合并相邻出现的词语, 如玉米、价格、指数，合并为玉米价格指数
            filteredResult=[]

            count = 0
            while len(keywords)>0:
                word = keywords.pop(0)
                merged = self.merge(word, wordGraph, keywords)
                filteredResult.append(merged)
                count+=1
                if count == topN:
                    break

            return filteredResult
    # /**
    #  * 合并词语current相邻的词语
    #  *
    #  * @param current
    #  * @param graph
    #  * @param candidates
    #  * @return
    #  */

    def merge(self, current, graph, candidates):
        """"""
        """python k 传值都是引用，除了基础变量，就是直接改变参数值，出到函数外边也是有作用的
        
        a = [ '1','2','3','4']
        b = 2
        def up(f):
            t =f.index('1')
            print(t)
            del f[t]
            
            #这个不会传到函数外边，因为f是一个新的变量了,这里要用到一些隐copy内容
            f = list(f)
            f[0]=0

        up(a)
        print(a)
        
        结果为，在up函数中被删除了，但是不能重新
        0
        ['2', '3', '4']

        
        """
        rights = graph.getRightNeighborsList(current)
        lefts = graph.getLeftNeighborsList(current)

        mergedText = current
        mergedItems = []

        for word in candidates:
            #查看word 是否存在
            if word in rights:
                mergedText = mergedText + word
                rights = graph.getRightNeighborsList(word) # // 该边右邻集合，不断向右合并
                mergedItems.append(word)
            elif word in lefts:
                mergedText = word + mergedText
                lefts = graph.getLeftNeighborsList(word) #//该边左邻集合，不断向左合并
                mergedItems.append(word)

        # // 删除已经合并掉的词语
        for w in mergedItems:
            id = candidates.index(w)
            del candidates[id]

        return mergedText

    """没有使用过"""
    def loadBiGram(self):
        pass
    def extractAsString(self, title, content, topN):
        return ' '.join(self.extractAsList(title, content, topN))

if __name__ == "__main__":

    title  = "维基解密否认斯诺登接受委内瑞拉庇护"
    content = "有俄罗斯国会议员，9号在社交网站推特表示，" \
              "美国中情局前雇员斯诺登，已经接受委内瑞拉的庇护，不过推文在发布几分钟后随即删除。" \
              "俄罗斯当局拒绝发表评论，而一直协助斯诺登的维基解密否认他将投靠委内瑞拉。" \
              "　　俄罗斯国会国际事务委员会主席普什科夫，在个人推特率先披露斯诺登已接受委内瑞拉的庇护建议，令外界以为斯诺登的动向终于有新进展。" \
              "　　不过推文在几分钟内旋即被删除，普什科夫澄清他是看到俄罗斯国营电视台的新闻才这样说，而电视台已经作出否认，称普什科夫是误解了新闻内容。" \
              "　　委内瑞拉驻莫斯科大使馆、俄罗斯总统府发言人、以及外交部都拒绝发表评论。而维基解密就否认斯诺登已正式接受委内瑞拉的庇护，说会在适当时间公布有关决定。" \
              "　　斯诺登相信目前还在莫斯科谢列梅捷沃机场，已滞留两个多星期。他早前向约20个国家提交庇护申请，委内瑞拉、尼加拉瓜和玻利维亚，先后表示答应，不过斯诺登还没作出决定。" \
              "　　而另一场外交风波，玻利维亚总统莫拉莱斯的专机上星期被欧洲多国以怀疑斯诺登在机上为由拒绝过境事件，涉事国家之一的西班牙突然转口风，外长马加略]号表示愿意就任何误解致歉，但强调当时当局没有关闭领空或不许专机降落。"
    extractor =  TextRankExtractor()
    extractor.setExtractMode(GraphType.TextRank.value)
    print(extractor.extractAsString(title, content, 5))
