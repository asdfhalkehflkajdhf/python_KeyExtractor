
# pylab.plot(X, Y, marker = marker, color = color, markerfacecolor = markerfacecolor, label=label, linewidth = linewidth, linestyle = linestyle)
#
# 'X': X,
# 'Y': Y2,
# 'marker': 'o',
# 'color': 'b',
# 'markerfacecolor': 'r',
# 'label': '222',
# 'linewidth': 3,
# 'linestyle': '--'

# 颜色（color 简写为 c）：
#
# 蓝色： 'b' (blue)
# 绿色： 'g' (green)
# 红色： 'r' (red)
# 蓝绿色(墨绿色)： 'c' (cyan)
# 红紫色(洋红)： 'm' (magenta)
# 黄色： 'y' (yellow)
# 黑色： 'k' (black)
# 白色： 'w' (white)
# 灰度表示： e.g. 0.75 ([0,1]内任意浮点数)
# RGB表示法： e.g. '#2F4F4F' 或 (0.18, 0.31, 0.31)
# 任意合法的html中的颜色表示： e.g. 'red', 'darkslategray'
# 线型（linestyle 简写为 ls）：
#
# 实线： '-'
# 虚线： '--'
# 虚点线： '-.'
# 点线： ':'

# 点型（标记marker）：
#
# 像素： ','
# 圆形： 'o'
# 上三角： '^'
# 下三角： 'v'
# 左三角： '<'
# 右三角： '>'
# 方形： 's'
# 加号： '+'
# 叉形： 'x'
# 棱形： 'D'
# 细棱形： 'd'
# 三脚架朝下： '1'（就是丫）
# 三脚架朝上： '2'
# 三脚架朝左： '3'
# 三脚架朝右： '4'
# 六角形： 'h'
# 旋转六角形： 'H'
# 五角形： 'p'
# 垂直线： '|'
# 水平线： '_'
# gnuplot 中的steps： 'steps' （只能用于kwarg中）
# 标记大小（markersize 简写为 ms）：
#
# markersize： 实数
# 标记边缘宽度（markeredgewidth 简写为 mew）：
#
# markeredgewidth：实数
# 标记边缘颜色（markeredgecolor 简写为 mec）：
#
# markeredgecolor：颜色选项中的任意值
# 标记表面颜色（markerfacecolor 简写为 mfc）：
#
# markerfacecolor：颜色选项中的任意值
# 透明度（alpha）：
#
# alpha： [0,1]之间的浮点数
# 线宽（linewidth）：
#
# linewidth： 实数
import matplotlib.pyplot as plt
import math
import numpy

from commons.LoadData import loadCsvData_Np
###############################################################
#画图时显示中文
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = [u'SimHei']
mpl.rcParams['axes.unicode_minus'] = False

linestyle=['-', '--', '-.',':']
marker=['o','D','+','s','*','v','<','>','X','^', '.']
linewidth=[1.1,1.2,1.3,1.4,1.5,1.6,1.7]

res = [
[1 ,0.142960419,0.509009009,0.223225624,'合并词，删除旧词'],
[1 ,0.138622809,0.493564994,0.21645266,'聚类加权夏天'],
[1 ,0.136634737,0.486486486,0.213348384,'不合并词'],
[1 ,0.135550334,0.482625483,0.211655143,'合并词，不删除旧词'],
[1 ,0.13392373,0.476833977,0.209115282,'位置加权'],
[10 ,0.444424363,0.158338699,0.233490006,'合并词，不删除旧词'],
[10 ,0.440267486,0.156888002,0.231339031,'不合并词'],
[10 ,0.432857401,0.154277248,0.227477798,'合并词，删除旧词'],
[10 ,0.420025303,0.149751917,0.220786624,'位置加权'],
[10 ,0.419302368,0.149494168,0.220406612,'聚类加权夏天'],
[2 ,0.228628231,0.407014157,0.292790186,'合并词，不删除旧词'],
[2 ,0.227724562,0.405405405,0.291632913,'不合并词'],
[2 ,0.227543828,0.405083655,0.291401458,'合并词，删除旧词'],
[2 ,0.225555756,0.401544402,0.288855457,'聚类加权夏天'],
[2 ,0.22284475,0.396718147,0.285383636,'位置加权'],
[3 ,0.287185975,0.340840841,0.311721432,'合并词，不删除旧词'],
[3 ,0.285559371,0.338910339,0.309955861,'不合并词'],
[3 ,0.283390566,0.336336336,0.307601766,'聚类加权夏天'],
[3 ,0.283209832,0.336121836,0.307405591,'合并词，删除旧词'],
[3 ,0.28122176,0.333762334,0.30524767,'位置加权'],
[4 ,0.324055666,0.288449163,0.305217465,'合并词，不删除旧词'],
[4 ,0.323694198,0.288127413,0.304877011,'不合并词'],
[4 ,0.32044099,0.28523166,0.30181292,'聚类加权夏天'],
[4 ,0.319537322,0.284427284,0.300961784,'位置加权'],
[4 ,0.317910718,0.282979408,0.299429739,'合并词，删除旧词'],
[5 ,0.356587746,0.253925354,0.296624821,'合并词，不删除旧词'],
[5 ,0.354599675,0.252509653,0.294971059,'不合并词'],
[5 ,0.347551057,0.247490347,0.28910772,'位置加权'],
[5 ,0.345924453,0.246332046,0.287754642,'合并词，删除旧词'],
[5 ,0.345562986,0.246074646,0.287453958,'聚类加权夏天'],
[6 ,0.381529008,0.226429261,0.284194938,'合并词，不删除旧词'],
[6 ,0.378998735,0.224927598,0.282310178,'不合并词'],
[6 ,0.372311585,0.220982622,0.277347694,'合并词，删除旧词'],
[6 ,0.367070305,0.217848332,0.273424879,'位置加权'],
[6 ,0.366528104,0.217526547,0.273021002,'聚类加权夏天'],
[7 ,0.403397795,0.205222508,0.272045829,'合并词，不删除旧词'],
[7 ,0.398879451,0.202942529,0.269015115,'不合并词'],
[7 ,0.390204229,0.198565253,0.263196392,'合并词，删除旧词'],
[7 ,0.383155612,0.194960456,0.258426281,'聚类加权夏天'],
[7 ,0.382794144,0.194776531,0.258182483,'位置加权'],
[8 ,0.419121634,0.186594786,0.258226157,'合并词，不删除旧词'],
[8 ,0.416591361,0.185498149,0.256695807,'不合并词'],
[8 ,0.406651003,0.181101095,0.250598652,'合并词，删除旧词'],
[8 ,0.399602386,0.177962009,0.246254942,'位置加权'],
[8 ,0.396168444,0.176432711,0.244138776,'聚类加权夏天'],
[9 ,0.433218869,0.171471493,0.245694957,'合并词，不删除旧词'],
[9 ,0.431050063,0.170637476,0.244490005,'不合并词'],
[9 ,0.419663835,0.166165736,0.238068386,'合并词，删除旧词'],
[9 ,0.411169348,0.162825651,0.23327352,'位置加权'],
[9 ,0.40791614,0.16153736,0.231427839,'聚类加权夏天']
]



def drowRes(resData, title, colNum,nameList=[]):
    """

    :param resData:每一行为一个数据[[topN,P,R,F,name]....]
    :param title:
    :param colNum:
    :return:
    """
    assert resData is not None
    assert colNum in [1,2,3]
    t = sorted(res, key=lambda x: (x[4], x[0]))
    t = numpy.array(t)
    # P
    pname=[]
    p=[]
    for i in range(int(res.__len__()/10)):
        start = i*10
        end = start+10
        p.append(numpy.array(t[start:end][:,colNum:colNum+1]).T)
        pname.append(t[start][-1])
    # print(p)
    # print(pname)
    '''改变画布大小'''
    dpi = 100.0
    figsize = 600 / float(dpi), 620 / float(dpi)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.patch.set_alpha(0)

    '''将figure设置的画布大小分成几个部分，参数‘221’表示2(row)x2(colu),即将画布分成2x2，两行两列的4块区域，1表示选择图形输出的区域在第一块，图形输出区域参数必须在“行x列”范围
    ，此处必须在1和2之间选择——如果参数设置为subplot(111)，则表示画布整个输出，不分割成小块区域，图形直接输出在整块画布上'''
    plt.subplot(111)#

    for i,pi in enumerate(p):
        if nameList.__len__()==0 or pname[i] in nameList:
            plt.plot(pi[0], label=pname[i], linestyle=linestyle[i.__mod__(linestyle.__len__())],marker=marker[i], linewidth=linewidth[i])

    # 设置图例字体大小
    # box = plt.get_position()

    # plt.set_position([box.x0, box.y0, box.width, box.height * 0.8])
    '''图例的位置 loc表示起始位置，center left'''
    plt.legend(loc='center left', bbox_to_anchor=(0.1, -0.1), ncol=3)
    # plt.legend(fontsize=15, loc='BestOutside')#ax is the axes instance
    plt.title(title)
    '''表边界到图边界的距离，不算 label 和刻度'''
    plt.subplots_adjust(bottom=.15, top=.99, left=.05, right=.99)
    # 对Ｘ坐标重新标号  rotation为旋转度
    group_labels = ['1', '2','3','4','5','6','7','8','9','10']
    plt.xticks( range(11),group_labels, rotation=0)
    plt.show()


if __name__=='__main__':
    res=[]
    filePath = '../data/res/20180301141258/allRes.csv'
    f = open(filePath, 'r', encoding='utf-8')
    for id,a in enumerate(f.readlines()):
        if id == 0:
            continue
        a =a.strip().split(',')
        # res.append([int(a[0].split('=')[1]), float(a[1]), float(a[2]), float(a[3]), a[4]])
        res.append([int(a[0]), float(a[1]), float(a[2]), float(a[3]), a[4]])
    f.close()

    '''==========================='''
    modeName = numpy.array(res)[:,4:5]
    modeName=list(set(modeName.ravel().tolist()))
    # modeName = [(id, x) for id, x in enumerate(modeName)]
    print([(id, x) for id, x in enumerate(modeName)])
    modeList = input("输入选择模型id list(默认为全部)：").strip()
    modeList = set(modeList.split())
    modeList = list(map(int, modeList))
    if modeList.__len__()==0:
        destModeName = modeName
    else:
        destModeName = [modeName[i] for i in modeList]
    print(destModeName)
    '''==========================='''

    # assert False
    # # # res = loadCsvData_Np(filePath, skiprows=1,dtype='float', ColumnList=[1])
    # # # print(res)
    # # # assert False


    # drowRes(res, 'P', 1, destModeName)
    drowRes(res, 'R', 2, destModeName)
    drowRes(res, 'F', 3, destModeName)

