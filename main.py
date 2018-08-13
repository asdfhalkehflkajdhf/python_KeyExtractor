
import os
import time

import keywords.TextRankExtractor as KeyExtractor
from commons import log
from commons import SegmentFactory
from commons import ChineseStopKeywords
from commons import wordVector
from commons import xml2dict

from evaluation import EvalResult
from evaluation import 其他结果统计
import g_config



def mode自动():
    logger = log.get_logger("mode自动")

    while True:

        logger.info("可选择算法模型，以空格分割 [%s]"%(list(KeyExtractor.GraphType)))
        while True:
            modeList = input("输入选择模型id list：").strip()
            modeList = set(modeList.split())
            modeList = list(map(int, modeList))
            if len(modeList)!=0:
                break
        logger.info("选择算法模型 %s"%(modeList))

        while True:
            filePath = input("input file(输入提取关键词的文本文件):")
            if len(filePath)!=0 and os.path.exists(filePath):
                break
            logger.info("文件[%s]不存在，重新输入" % (filePath))
        pass

        logger.info("选择topN范围（不分前后，只取最大和最小，默认为1），以空格分割。" )
        topNlist = input("选择topN范围：")
        topNlist = list(set(topNlist.split()))
        topNlist = list(map(int, topNlist))
        minTopN = min(topNlist)
        if minTopN<1:
            minTopN=1
        maxTopN = max(topNlist)

        logger.info("\nmodeList：%s \ntopN范围：[%d %d] \n原文件：%s"%(str(modeList), minTopN, maxTopN, filePath))
        ok = input("运行结果会保存在当前目录下data/res/time，[Y/N](默认Y)。如果有问题，请查看日志文件进行程序调试：")
        if ok.__len__()==0 or ok.lower()=='y':
            break
    pass

    resDir = 'data/res/'+time.strftime("%Y%m%d%H%M%S", time.localtime())
    #  新建结果目录
    if not os.path.exists(resDir):
        logger.info("新建结果存放目录 %s"%(resDir))
        os.makedirs(resDir, exist_ok=True)

    # 解析文本
    xml = xml2dict.XML2Dict()
    r = xml.parse(filePath)


    for modeId in modeList:
    #     以模型开始
        extractor = KeyExtractor.TextRankExtractor()
        extractor.setExtractMode(modeId)

        keyResFile = os.path.join(resDir, KeyExtractor.GraphType(modeId).name + "_maxTop.%d" % (maxTopN))
        f = open(keyResFile, mode='w', encoding='utf8')
        print("#id\t提取出来的关键词\t原来的关键词", file=f)
        # 取出maxTopN个词
        for id, article in enumerate(r.articles.article):
            startTime = time.time()
            # logger.info("start id=%d %s"%(id, time.strftime("%H%M%S", time.localtime())))
            keywordsList = extractor.extractAsList(article.title, article.content, maxTopN)
            #保存到文件
            srcKey = list(article.tags.split(','))
            for i in range(len(srcKey)).__reversed__():
                srcKey[i] = SegmentFactory.get去中文标点符号(srcKey[i])
            print(id, '\t', ','.join(keywordsList), '\t', ','.join(srcKey), file=f)
            f.flush()
            logger.info("id=%d 运行时间=%d" % (id, time.time()-startTime))
        pass
        f.close()
    pass
    '''======================================'''
    # 对结果进行分析,PRF,输出到文件
    EvalResult.result分析(resDir, maxTopN)
    # 其他结果统计分析
    其他结果统计.分析(resDir, maxTopN)

def mode手动():
    logger = log.get_logger("mode自动")

    '''其他参数self.alpha_f, self.beta_f, self.gamma_f,需要先写死'''
    extractor = KeyExtractor.TextRankExtractor()
    evaRes = EvalResult.EvalResult()



    while True:
        print("输入测试文件（默认data/test.txt）")
        print("模型选择：", list(KeyExtractor.GraphType))
        print("提取关键词个数：（默认为5个）\n输出关键词信息[Y/N]（默认为N）")
        filePath = input("input file(输入end时结束程序):").strip()
        if filePath == "end":
            break
        if len(filePath)<=0:
            filePath = 'data/test.txt'
        if not os.path.exists(filePath):
            logger.info("文件[%s]不存在，重新输入"%(filePath))
            continue
        # _---------------------------------------------
        mode = input("模型选择:")
        if len(mode) <= 0:
            mode = 0
        else:
            mode = int(mode)
        # _---------------------------------------------
        topN = input("input topN:")
        if len(topN)==0:
            topN= 5
        else:
            topN = int(topN)
        # _---------------------------------------------

        logger.info("提取关键词开始：%s mode=%d topN=%d "%(filePath, mode,topN))

        if not extractor.setExtractMode(mode):
            logger.info("mode=%d 不存在" % ( mode))
            continue
        # 评价类重置
        evaRes.reSet()
        # 以上为参数判断+++++++++++++++++++++++++++++++++++++++++
        xml = xml2dict.XML2Dict()
        r = xml.parse(filePath)

        for id, article in enumerate(r.articles.article):
            # topN = len(list(article.tags.split(',')))
            logger.info("文本id:%d"%(id))
            keywordsList = extractor.extractAsList(article.title, article.content, topN)
            srcKey = list(article.tags.split(','))
            logger.info("抽取的关键词：%s\t源关键词：%s \n"%(str(keywordsList) , str(srcKey)))

            for i in range(len(srcKey)).__reversed__():
                srcKey[i] = SegmentFactory.get去中文标点符号(srcKey[i])
            #保存到文件
            print(id, '\t', ','.join(keywordsList), '\t', ','.join(srcKey))
            evaRes.addKeyList(srcKey, keywordsList)

        logger.info(evaRes.getRes_String())
        # 统计信息写入文件
        res = evaRes.getRes_PRF()
        print("topN=", topN, '\t', res[0], '\t', res[1], '\t', res[2])

    pass


if __name__ == '__main__':

    '''关于配置说明：如果不知道那个配置的选项，可以在配置文件中删除了，进行程序，在日志文件中会输出说明'''
    '''其他参数self.alpha_f, self.beta_f, self.gamma_f,需要先写死'''


    logger = log.get_logger("main")

    #初始化加载项 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if g_config.segmentEnable or g_config.w2v_enable:
        if g_config.segmentEnable:
            logger.info("开始分词")
            SegmentFactory.fenchiToFile(g_config.segmentfenchiInput, g_config.segmentfenchiOutput)
            logger.info("分词结束")
        if g_config.w2v_enable:
            logger.info("开始词向量训练")
            wordVector.w2v_tarin(g_config.w2v_inFile, g_config.w2v_outFile,g_config.w2v_size, g_config.w2v_window)
            logger.info("词向量训练结束")
        exit(0)
    logger.info("开始加载词典")
    SegmentFactory.addUserWordDict(list(g_config.segmentuserDictFile.split()))
    ChineseStopKeywords.addStopKeywords(list(g_config.segmentstopDictFile.split()))
    logger.info("加载词典结束")

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++

    mode = int(input("选择[手动－1/自动－2/退出-0]模式(默认为0)："))
    print("mode = ",mode)
    if mode == 1:
        mode手动()
    elif mode == 2:
        mode自动()





# data/test.txt
# data/articles.xml