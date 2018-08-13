[config]
# 词语的覆盖影响力因子
extractor.keyword.alpha = 0.33
# 词语的位置影响力因子
extractor.keyword.beta = 0.34
# 词语的频度影响力因子
extractor.keyword.gamma = 0.33
extractor.keyword.lambda = 30
#kmeans聚类时，中心数
extractor.keyword.maxk = 5
#模型选择:[<GraphType.TF_IDF: 0>, <GraphType.TextRank: 1>, <GraphType.PositionRank: 2>, <GraphType.NingJianfei: 3>, <GraphType.ClusterRank: 4>, <GraphType.ClusterPositionRank: 5>]
extractor.keyword.mode = 0
#
extractor.keyword.valid.word.count = 2000
extractor.keyword.merge.neighbor = True



#以上内容配置文件中都没有使用
#=========================================
#我的算法，是否进行合并词，在算法执行前操作的
my_method_is_combination_word = True
#算法，合并词后，是否删除旧词
my_method_old_word_is_del_when_word_merged = False

[log]
#日志输出文件，没有的话默认就是log.txt
logpath = log.txt

[segment]
#如果开启 fenchiinput fenchioutput要有
enable = False
fenchiinput =
fenchioutput =
#停用词文件，多个文件时，用空格分割，没有就空着
stopdictfile = resources/stoplists/cn.txt resources/stoplists/cn_keywords.txt
userdictfile = resources/new_wiki_words.dic

[word2vec]
#如果开启 window size　infile　outfile　loadmode，要有内容，进行词向量训练
enable = False
window = 5
size = 50
infile =
outfile =

#加载词向量需要的配置
loadmode = c_vec
w2v_modepath = resources/alldata_wiki_sohuNews__vector_size50_win5

#当有，分词和词向量训练时，优先进行分词和词向量训练，不会执行关键词提取




#P ＝ 抽取结果中与人工标注相同的关键词个数/人工标注的关键词总个数
#R = 抽取结果中与人工标注相同的关键词个数/抽取关键词总个数
#F-measure = 2PR/(P+R)



