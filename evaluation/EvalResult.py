


# 评价结果计算
# P ＝ 抽取结果中与人工标注相同的关键词个数/人工标注的关键词总个数
# R = 抽取结果中与人工标注相同的关键词个数/抽取关键词总个数
# F-measure = 2PR/(P+R)


class EvalResult():
    def __init__(self):
        # precision
        self._P=0
        # recall
        self._R=0
        # F - measure
        self._F=0
        # 标注的关键词总个数
        self._srcKeyWordsTotal=0
        # 抽取关键词总个数
        self._extKeyWordsTotal=0

        # 相同的关键词个数
        self._simKeyWordsTotal=0

        self._label=''

    def addKeyList(self, srcKeys, extKeys):
        """
        参数为两个关键词list list [keyword1, keyword2, .....]
        :param srcKeys:
        :param extKeys:
        :return:
        """
        self._extKeyWordsTotal+=len(extKeys)
        self._srcKeyWordsTotal+=len(srcKeys)

        a = set(srcKeys)
        b = set(extKeys)
        # 交集，关键词相同个数
        self._simKeyWordsTotal+=len(a & b)

    def setLabel(self,label):
        self._label = label
    def getRes_PRF(self):
        self._P=0
        # recall
        self._R=0
        # F - measure
        self._F=0
        if self._srcKeyWordsTotal != 0:
            self._P = self._simKeyWordsTotal/self._srcKeyWordsTotal
        if self._extKeyWordsTotal != 0:
            self._R = self._simKeyWordsTotal/self._extKeyWordsTotal
        if self._P!=0 and self._R!=0:
            self._F = self._P*self._R*2/(self._P+self._R)
        return self._P, self._R, self._F

    def getRes_String(self):
        self.getRes_PRF()
        return "%s res: p=%f r=%f f=%f"%(self._label, self._P, self._R, self._F)

    def reSet(self):
        # 标注的关键词总个数
        self._srcKeyWordsTotal=0
        # 抽取关键词总个数
        self._extKeyWordsTotal=0

        # 相同的关键词个数
        self._simKeyWordsTotal=0

        self._label=''

def result分析( resDir, maxTopN):
    import os
    from keywords import TextRankExtractor as KeyExtractor

    # resDir = input("输入结果目录：").strip()
    if not os.path.exists(resDir):
        print("目录不存在")
        return False
    allResCsvFilePath = os.path.join(resDir, 'allRes.csv')
    allResCsv=open(allResCsvFilePath,'w',encoding='utf8')
    print("topN,P,R,F,funName", file=allResCsv)

    # maxTopN = int(input("提取关键词最大个数(默认为1)："))
    minTopN = 1
    modeIdList = list(range(list(KeyExtractor.GraphType).__len__()))
    for modeId in modeIdList:

        keyResFile = os.path.join(resDir, KeyExtractor.GraphType(modeId).name + "_maxTop.%d" % (maxTopN))
        if not os.path.exists(keyResFile):
            print("file not exists", keyResFile)
            continue
        print("open:", keyResFile)
        f = open(keyResFile, mode='r', encoding='utf8')
        if not f:
            print("open error")

        # 读取所有结果到list中 [ [id, extKeyList, srcKeyList] .....]
        allResList = []
        # 去标题行
        # print(f.readline())
        f.readline()
        line = f.readline()
        while line:
            line = line.strip("\n")
            id, extkey, srckey = line.split('\t')
            extKeyList = extkey.strip().split(',')
            srcKeyList = srckey.strip().split(',')
            # print(id, extkey, srckey)
            allResList.append([id, extKeyList, srcKeyList])
            line = f.readline()
        pass
        # assert False
        # for line in f.readlines():
        #     # print(line)
        #     # 去换行符
        #     line = line.strip("\n")
        #     id, extkey, srckey = line.split('\t')
        #     extKeyList = extkey.strip().split(',')
        #     srcKeyList = srckey.strip().split(',')
        #     # print(id, extkey, srckey)
        #     allResList.append([id, extKeyList, srcKeyList])
        # pass
        f.close()

        evaRes = EvalResult()
        keyResEvaFile = os.path.join(resDir, KeyExtractor.GraphType(modeId).name + "_eva.txt")
        evaF = open(keyResEvaFile, mode='w', encoding='utf8')

        print("\tP\tR\tF\t", file=evaF)
        for topN in range(minTopN, maxTopN + 1):
            evaRes.reSet()
            for resKey in allResList:
                evaRes.addKeyList(resKey[2], resKey[1][0:topN])

            # 统计信息写入文件
            res = evaRes.getRes_PRF()
            print("topN=", topN, '\t', res[0], '\t', res[1], '\t', res[2],'\t',KeyExtractor.GraphType(modeId).name, file=evaF)
            print( topN,  res[0],  res[1], res[2],KeyExtractor.GraphType(modeId).name, file=allResCsv, sep=',')
            print("topN=", topN, '\t', res[0], '\t', res[1], '\t', res[2], '\t', KeyExtractor.GraphType(modeId).name)
        pass
        evaF.close()
    allResCsv.close()


if __name__== "__main__":
    # resDir = input("输入结果目录：").strip()
    # maxTopN = int(input("提取关键词最大个数(默认为1)："))

    resDir="../data/res/20180204143529"
    maxTopN = 10

    result分析(resDir, maxTopN)