import multiprocessing
import os

from gensim.models import KeyedVectors
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

from commons import log

'''用gensim函数库训练Word2Vec模型有很多配置参数。这里对gensim文档的Word2Vec函数的参数说明进行翻译，以便不时之需。

class gensim.models.word2vec.Word2Vec(sentences=None,size=100,alpha=0.025,window=5, min_count=5, max_vocab_size=None, sample=0.001,seed=1, workers=3,min_alpha=0.0001, sg=0, hs=0, negative=5, cbow_mean=1, hashfxn=<built-in function hash>,iter=5,null_word=0, trim_rule=None, sorted_vocab=1, batch_words=10000)

参数：

·  sentences：可以是一个·ist，对于大语料集，建议使用BrownCorpus,Text8Corpus或·ineSentence构建。
·  sg： 用于设置训练算法，默认为0，对应CBOW算法；sg=1则采用skip-gram算法。
·  size：是指特征向量的维度，默认为100。大的size需要更多的训练数据,但是效果会更好. 推荐值为几十到几百。
·  window：表示当前词与预测词在一个句子中的最大距离是多少
·  alpha: 是学习速率
·  seed：用于随机数发生器。与初始化词向量有关。
·  min_count: 可以对字典做截断. 词频少于min_count次数的单词会被丢弃掉, 默认值为5
·  max_vocab_size: 设置词向量构建期间的RAM限制。如果所有独立单词个数超过这个，则就消除掉其中最不频繁的一个。每一千万个单词需要大约1GB的RAM。设置成None则没有限制。
·  sample: 高频词汇的随机降采样的配置阈值，默认为1e-3，范围是(0,1e-5)
·  workers参数控制训练的并行数。
·  hs: 如果为1则会采用hierarchica·softmax技巧。如果设置为0（defau·t），则negative sampling会被使用。
·  negative: 如果>0,则会采用negativesamp·ing，用于设置多少个noise words
·  cbow_mean: 如果为0，则采用上下文词向量的和，如果为1（defau·t）则采用均值。只有使用CBOW的时候才起作用。
·  hashfxn： hash函数来初始化权重。默认使用python的hash函数
·  iter： 迭代次数，默认为5
·  trim_rule： 用于设置词汇表的整理规则，指定那些单词要留下，哪些要被删除。可以设置为None（min_count会被使用）或者一个接受()并返回RU·E_DISCARD,uti·s.RU·E_KEEP或者uti·s.RU·E_DEFAU·T的函数。
·  sorted_vocab： 如果为1（defau·t），则在分配word index 的时候会先对单词基于频率降序排序。
·  batch_words：每一批的传递给线程的单词的数量，默认为10000
'''



w2v_mode = None
def w2v_load(w2v_path, mode):
    global w2v_mode

    # 只加载一次
    if w2v_mode is not None:
        return True

    if os.path.isfile(w2v_path):
        try:
            if mode.lower()=='c_vec':
                w2v_mode = KeyedVectors.load_word2vec_format(w2v_path, binary=False)
            elif mode.lower()=='p_bin':
                w2v_mode=Word2Vec.load(w2v_path)
            elif mode.lower() == 'c_bin':
                w2v_mode = KeyedVectors.load_word2vec_format(w2v_path, binary=False)
            else:
                return False
        except:
            return False
    else:
        return False
    return True


def w2v_tarin(inFile, outFile, size=50, window=5):
    logger = log.get_logger("wordVector")
    logger.info("running ")


    inp = inFile
    outp1 = outFile+"_pBin_size"+str(size)+"_win"+str(window)
    outp2 = outFile+"_cVec_size"+str(size)+"_win"+str(window)
    outp3 = outFile+"_cBin_size"+str(size)+"_win"+str(window)

    model = Word2Vec(LineSentence(inp), size=size, window=window, min_count=5,
                     workers=multiprocessing.cpu_count())

    # trim unneeded model memory = use(much) less RAM
    # model.init_sims(replace=True)
    '''以二进制格式存储'''
    model.save(outp1)
    '''C语言以文本格式存储，一行一个词的向量'''
    model.wv.save_word2vec_format(outp2, binary=False)
    '''C语言以二进制格式存储'''
    model.wv.save_word2vec_format(outp3, binary=True)
    #from gensim.models import KeyedVectors
    #model = KeyedVectors.load_word2vec_format('alldata_wiki_sohuNews__vector_size50_win5', binary=False)


def w2v_similarity(word1, word2):
    """不存在时，返回None"""
    global w2v_mode
    if w2v_mode is None:
        return None
    try:
        res = w2v_mode.similarity(word1, word2)
    except:
        res = None
    return res
    pass

def w2v_getVec(word1):
    """不存在时，返回None"""
    global w2v_mode
    try:
        vec = w2v_mode[word1]
    except:
        vec = None
    return vec



if __name__ == "__main__":

    w2v_load('../resources/alldata_wiki_sohuNews__vector_size50_win5', isVector=True)

    vec = w2v_getVec('斯诺登')

    print(vec)
    vec = w2v_getVec('质量')
    print(vec)
    # # 计算两个词的相似度/相关程度
    # try:
    #     y1 = model.similarity("淮南子", "斯诺登")
    #     print(y1)
    #     print("--------\n")
    # except:
    #     pass
    # # 计算某个词的相关词列表
    # # y2 = model.most_similar("斯诺登")  # 20个最相关的
    # # for item in y2:
    # #     print (item[0], item[1])
    # # print ("--------\n")
    #
    # # 寻找对应关系
    # print(u"书-不错，质量-")
    # y3 = model.most_similar([u'质量', u'不错'], [u'书'], topn=3)
    # for item in y3:
    #     print(item[0], item[1])
    # print("--------\n")
    #
    # # 寻找不合群的词
    # y4 = model.doesnt_match(u"书 书籍 教材 很".split())
    # print(u"不合群的词：", y4)
    # print("--------\n")