import os
from keywords import TextRankExtractor as KeyExtractor
from evaluation import  EvalResult

# ../data/res/20180203171846
# resDir = input("输入结果存放目录：").strip()
# maxTopN = int(input("提取关键词最大个数(默认为1),关键词结果文件的后缀数字："))

def 分析(resDir, maxTopN):
    if not os.path.exists(resDir):
        print("目录不存在")
        exit(0)
    # 保存每统计结果文便比较
    统计结果路径=os.path.join(resDir,'其他统计结果')
    if not os.path.exists(统计结果路径):
        os.makedirs(统计结果路径, exist_ok=True)
    # resDir = 'data/res/20180203171846'
    # maxTopN = 10

    modeIdList = list(range(list(KeyExtractor.GraphType).__len__()))
    minTopN = 1
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
             # print(id, end=' ')
             allResList.append([id, extKeyList, srcKeyList])
             line = f.readline()
        pass
        f.close()


        统计结果文件=os.path.join(统计结果路径,KeyExtractor.GraphType(modeId).name + "res.txt")
        f = open(统计结果文件, 'w', encoding='utf8')
        for topN in range(minTopN, maxTopN + 1):
            统计关键词文件 = os.path.join(统计结果路径, KeyExtractor.GraphType(modeId).name + "res_%d.txt"%(topN))
            keyRes_F = open(统计关键词文件,'w',encoding='utf8')
            totCount = 0
            totLen = 0
            tot没中的 = 0
            长词个数=0 #大于等于 4 的个数
            for id, extKeyList, srcKeyList in allResList:
                单篇文章预测中的 = []
                for key in extKeyList[:topN]:
                    if key in srcKeyList:
                        单篇文章预测中的.append(key)
                        totCount += 1
                        totLen += len(key)
                        # print(key ,end=' ')
                    if len(key)>=4:
                        长词个数+=1
                if 单篇文章预测中的.__len__() == 0:
                    tot没中的 += 1
                # 输出到文件
                print(id,单篇文章预测中的,file=keyRes_F)
               # print()
            keyRes_F.close()

            t_结果 = ''
            t_结果+=KeyExtractor.GraphType(modeId).name+' '
            t_结果 +="topN="+str(topN)+' '
            t_结果 += '命中总数='+str(totCount)+' '
            t_结果 +="平均每篇文章个数="+str(totCount / allResList.__len__())+' '
            t_结果 += '长词个数(>=4)='+str(长词个数)+' '
            t_结果 += '平均词长='+str(totLen / totCount)+' '
            t_结果 +="一个关键词没中的文章个数="+str(tot没中的)

            print(t_结果)

            # 输出到文件
            print(t_结果,file=f)

        pass
        f.close()


if __name__=='__main__':
    # ../data/res/20180203171846
    resDir = input("输入结果存放目录：").strip()
    maxTopN = int(input("提取关键词最大个数(默认为1),关键词结果文件的后缀数字："))
    分析(resDir, maxTopN)