#这个都是全局的，接口函数，并不需要定义类来完成 测试过
import jieba
import jieba.posseg  # 需要另外加载一个词性标注模块
import codecs,sys
import os
import re


from commons import log
from commons import xml2dict
from commons import ChineseStopKeywords

def getSegment(content):
    """分词后的直接结果,文本路径或是内容        返回分词后的list列表    """
    seg_list = []
    if os.path.isfile(content):
        f = codecs.open(content, 'r', encoding="utf-8")
        line = f.read()
        seg_list =  jieba.cut(line, cut_all=True)  # 全模式
        f.close()
    elif content is not None:
        seg_list =  jieba.cut(content, cut_all=True)  # 全模式

    return list(seg_list)

def getSegmentTag( sentence):
    """切分句子并进行词性标记， 返回分词，和标注元组 tuple list。词曲有一个问题就是会去重 [ [词, 词性, 序,[可选项，为合并词后的词，为了不打乱词序，这个词所有属性与原词一样，同样参加图的计算]] ''']"""
    """切分句子并进行词性标记， 返回分词，和标词典。有一个严重的问题就是会去重 """

    fenchi_seg_list = jieba.cut(sentence)  # 全模式

    seg_dict = {}
    res_seg_tuple_list = []
    seg_list = jieba.posseg.cut(sentence)

    # 生成词性词曲
    for setiterm in seg_list:
        seg_dict[setiterm.word]=setiterm.flag

    # a = set(list(fenchi_seg_list))
    # b = set(list(seg_dict.keys()))
    # print(a-b)
    # assert False
    # 生成元组list
    for i,word in enumerate(fenchi_seg_list):
        if word in list(seg_dict.keys()):
            # 生成词项[ [词, 词性, 序,[可选项，为合并词后的词，为了不打乱词序，这个词所有属性与原词一样，同样参加图的计算]] ''']
            res_seg_tuple_list.append([word, seg_dict[word], i,[]])

    return res_seg_tuple_list


def insertUserDefinedWord( word, pos=None, freq=None):
    """这个还没有用到"""
    jieba.add_word(word=word, freq=freq, tag=pos)

def addUserWordDict(pathList=[]):
    logger = log.get_logger("fenchi")
    for path in pathList:
        if os.path.isfile(path):
            jieba.load_userdict(path)
            logger.info("加载用户词典：%s"%(path))
    logger.info("加载用户词典结束：%s"%(pathList))


def fenchiToFile(src_file, output_fil):
    logger = log.get_logger("fenchi")
    if not os.path.exists(src_file):
        logger.info("源文件不存在：%s"%(src_file))
        exit(0)
    if not os.path.exists(os.path.split(output_fil)[0]):
        logger.info("目标输出目录不存在")
        exit(0)

    f=codecs.open(src_file,'r',encoding="utf-8")
    target = codecs.open(output_fil, 'w',encoding="utf-8")
    logger.info('open files %s to %s'%(src_file, output_fil))
    line_num=1
    line = f.readline()
    while line:
        # print(line)
        if line_num%10000 == 0:
            logger.info('---- processing %d article----------------'%(line_num))
        line_seg = ' '.join(jieba.cut(line,cut_all=True))#全模式
        target.writelines(line_seg)
        line_num = line_num + 1
        line = f.readline()
    f.close()
    target.close()
    logger.info('---- processing row totle %d article----------------' % (line_num))
    logger.info("分词完成")

def get停用词(res):
    """res 结构[ [词, 词性, 序,[可选项，为合并词后的词，为了不打乱词序，这个词所有属性与原词一样，同样参加图的计算]] ''']"""
    # print("去停用词==============================")
    for j in range(res.__len__()).__reversed__():
        if ChineseStopKeywords.isStopKeyword(res[j][0]):
            del res[j]
    # print(res.__len__())
    # print(res)
    return res

def _词合并操作(isDelWord, resList, c, h):
    # 地名+名词,相加后长度不大于4
    if isDelWord:
        # 生成新词项,删除旧词
        resList[c][0] += resList[h][0]
        del resList[h]
    else:
        # 生成新词项，添加到list
        resList[c][-1].append(resList[c][0] + resList[h][0])

def get合并词(resList, isDelWord=False):
    """ res 结构[ [词, 词性, 序,[可选项，为合并词后的词，为了不打乱词序，这个词所有属性与原词一样，同样参加图的计算]] ''']
    :param resList:
    :param isDelWord: ,是否删除合并前的词，不删除时，把新词添加到合并词属性list的第一个最后一个
    :return:
    """
    # print("合并词==============================,合并长度为统计关键词长度得到的。")
    # 平均长度： 3.187458081824279
    # == == == == == == == == == == == == == == == ==
    # 长词(2)： 1093    占比： 0.36653252850435947
    # 长词(3)： 663    占比： 0.22233400402414488
    # 长词(4)： 975    占比： 0.32696177062374243
    # 长词( > 4)： 248    占比： 0.08316566063044936
    # 对比长对，４，５，６选择 6 比较好
    mergeWordMaxLen = 6
    for i in range(0, resList.__len__()-1).__reversed__():
        # 当前下标
        c = i
        #后一个标
        h = i+1
        # 是否相链接
        if resList[c][2] +1 == resList[h][2]:
             # 相链接， 判断词性
            if resList[c][1] == 'ns' and resList[h][1]=='n' and len(resList[c][0]+resList[h][0])<= mergeWordMaxLen:
                # 地名+名词,相加后长度不大于4
                _词合并操作(isDelWord, resList, c, h)
            elif resList[c][1] == 'nr' and resList[h][1]=='nr':
                # 人,相加后长度不
                _词合并操作(isDelWord, resList, c, h)
            elif resList[c][1] == 'n' and resList[h][1]=='n' and len(resList[c][0]+resList[h][0])<= mergeWordMaxLen:
                _词合并操作(isDelWord, resList, c, h)
            elif resList[c][1] == 'n' and resList[h][1].startswith('v') and len(resList[c][0]+resList[h][0])<= mergeWordMaxLen:
                _词合并操作(isDelWord, resList, c, h)
            elif resList[c][1].startswith('v') and resList[h][1]=='n' and len(resList[c][0]+resList[h][0])<= mergeWordMaxLen:
                _词合并操作(isDelWord, resList, c, h)
            elif resList[c][1] == 'm' and resList[h][1]=='m':
                _词合并操作(isDelWord, resList, c, h)
            else:
                # print('不合并',res[c], res[h])
                pass
    return resList

def get去单字(resList):
    """res 结构[ [词, 词性, 序,[可选项，为合并词后的词，为了不打乱词序，这个词所有属性与原词一样，同样参加图的计算]] ''']"""

    for j in range(resList.__len__()).__reversed__():
        if len(resList[j][0]) == 1:
            del resList[j]
    # print(res.__len__())
    # print(res)
    return resList

def get去中文标点符号(str):
    ruler = "[\s+\.\!\/_,$%^*(+\"\']+|[+“《》”——！，。？、~@#￥%……&*（）]+"
    # string = re.sub(ruler.decode("utf8"), "".decode("utf8"), temp)  #python 2.7
    string = re.sub(ruler, "", str) #python 3.6
    return string

def _tttt():
    # import jieba
    # import thulac
    #
    # thu1 = thulac.thulac()  #默认模式
    #
    # text = "浙江苍南城管被围殴续：3城管15滋事者受处理"
    # text = "工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作"
    # res = thu1.cut(text)
    # print(res)
    #
    # b = thu1.cut('在北京大学生活区喝进口红酒')
    # print(b)
    # #
    # #
    # # print(list(jieba.cut(text)))
    #
    #
    # # import jieba
    # # import jieba.posseg
    # # text = "浙江苍南城管被围殴续：3城管15滋事者受处理"
    # # res  = jieba.cut(text)
    # # print(list(res))
    # #
    # # res2 = jieba.posseg.cut(' '.join(res))
    # print(list(res2))
    pass

if __name__ == "__main__":

    filePath='../data/test.txt'
    xml = xml2dict.XML2Dict()
    r = xml.parse(filePath)

    ChineseStopKeywords.addStopKeywords(['../resources/stoplists/cn.txt', '../resources/stoplists/en.txt'])
    # print(ChineseStopKeywords.getStopKeywords())
    print(ChineseStopKeywords.isStopKeyword('\\n'))
    # assert False
    # for article in r.articles.article:
        # topN = len(list(article.tags.split(',')))
    article = r.articles.article[0]
    string =article.content
    # print(string)
    # res = getSegment(string)
    # print(string)
    print("原始==============================")
    res = getSegmentTag(string)
    print(res.__len__())
    print(res)

    get停用词(res)


    print("合并词==============================")
    get合并词(res)
    print(res.__len__())
    print(res)





    # import g_config
    # addUserWordDict(list(g_config.segmentuserDictFile.split()))
    #
    # jieba.add_word("市民社会")
    # string = '浙江苍南城管被市民社会围殴续：3城管15滋事者没必要受处理玉门鼠疫'
    # # string = '警方称，涉嫌滋事嫌疑人员多为县城及周边的社会闲散人员，数人有殴打他人的劣迹前科。被处理的15人中，有10人因涉嫌寻衅滋事罪被采取刑事强制措施；4人因构成寻衅滋事行为被行政拘留15日；1人因构成阻碍执行职务行为被行政拘留15日。'
    # res = getSegment(string)
    # print(res)
    # print("==============================")
    # res = getSegmentTag(string)
    # print(res)
