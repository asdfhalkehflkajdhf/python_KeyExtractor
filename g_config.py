import logging
import sys
import os
import configparser


confFile = 'conf-extractor.cfg'
confFile = os.path.join(os.getcwd(), confFile)
confFile = 'E:\\毕业研究内容\\3、关键词提取\\python_KeyExtractor\\conf-extractor.cfg'
if not os.path.exists(confFile):
    print("工程目录下配置文本[ %s ]不存在"%(confFile))
    exit(1)

#读取配置文件
_conf = configparser.RawConfigParser()
_conf.read(confFile, encoding='utf8')


#log 部分===================================================
t = _conf.has_option('log', 'logPath')
_logPath = 'log.txt'
if t:
    _logPath = _conf.get('log', 'logPath')
    # <description>自动生成关键词和摘要, 不再取网页中的Ｍeta信息</description>
else:
    # _logger.info( "'log', 'logPath', 'log.txt' 不存在时")
    _conf.set('log', 'logPath', 'log.txt')

_logDir = os.path.split(_logPath)[0]
if len(_logDir)>1 and not os.path.exists( _logDir ):
    os.makedirs(_logDir, exist_ok=True)
#这都是全局变量
formatter = logging.Formatter('%(asctime)s | %(filename)s | %(module)s | %(lineno)d | %(levelname)-8s: %(message)s')
file_handler = logging.FileHandler(_logPath, encoding='utf8')
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式
# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

_logger = logging.getLogger("config")
_logger.addHandler(file_handler)
_logger.addHandler(console_handler)
# 指定日志的最低输出级别，默认为WARN级别
_logger.setLevel(logging.INFO)

#分词 部分===================================================
# 分词,自定义词典信息
segmentEnable = False
_t = _conf.has_option('segment', 'enable')
if _t:
    segmentEnable = _conf.getboolean('segment', 'enable')
    # <description>自动生成关键词和摘要, 不再取网页中的Ｍeta信息</description>
else:
    _logger.info("'segment', 'enable', 'False'  #分词功能，单独使用,进行分词，完成词向量训练")
    _conf.set('segment', 'enable', 'False')

segmentfenchiInput=''
segmentfenchiOutput=''
if segmentEnable:
    _t = _conf.has_option('segment', 'fenchiInput')
    if _t:
        segmentfenchiInput = _conf.get('segment', 'enable')
    else:
        _logger.info("分词，必须要有源文件，segment fenchiInput 配置缺失")
        _conf.set('segment', 'fenchiInput')
        exit(0)

    _t = _conf.has_option('segment', 'fenchiOutput')
    if _t:
        segmentfenchiOutput = _conf.get('segment', 'fenchiOutput')
    else:
        _conf.set('segment', 'fenchiOutput', '')
        _logger.info("分词，必须要有输出文件，segment fenchiOutput 配置缺失")
        exit(0)

segmentstopDictFile = ''
segmentuserDictFile = ''
_t = _conf.has_option('segment', 'stopDictFile')
if _t:
    segmentstopDictFile = _conf.get('segment', 'stopDictFile')
    # <description>自动生成关键词和摘要, 不再取网页中的Ｍeta信息</description>
else:
    _conf.set('segment', 'stopDictFile', '')

_t = _conf.has_option('segment', 'userDictFile')
if _t:
    segmentuserDictFile = _conf.get('segment', 'userDictFile')
    # <description>自动生成关键词和摘要, 不再取网页中的Ｍeta信息</description>
else:
    _conf.set('segment', 'userDictFile', '')


#词向量分部 部分===================================================

w2v_enable=False
_t = _conf.has_option('word2vec', 'enable')
if _t:
    w2v_enable = _conf.getboolean('word2vec', 'enable')
    # <description>自动生成关键词和摘要, 不再取网页中的Ｍeta信息</description>
else:
    _conf.add_section('word2vec')
    _logger.info("'word2vec', 'enable', 'False'  #词向量训练，单独使用")
    _conf.set('word2vec', 'enable', 'False')


w2v_loadMode = 'c_vec'
w2v_modePath = ''

_t = _conf.has_option('word2vec', 'loadMode')
if _t:
    w2v_loadMode = _conf.get('word2vec', 'loadMode')
    # <description>自动生成关键词和摘要, 不再取网页中的Ｍeta信息</description>
else:
    _logger.info("'word2vec', 'loadMode', #保存方式不同，有三种情况，c_vec,c_bin,p_bin'")
    _conf.set('word2vec', 'loadMode', 'c_vec')

_t = _conf.has_option('word2vec', 'w2v_modePath')
if _t:
    w2v_modePath = _conf.get('word2vec', 'w2v_modePath')
    # <description>自动生成关键词和摘要, 不再取网页中的Ｍeta信息</description>
else:
    _conf.set('word2vec', 'w2v_modePath')



w2v_size = 50
w2v_window = 5
w2v_inFile = ''
w2v_outFile = ''
if w2v_enable:
    _t = _conf.has_option('word2vec', 'size')
    if _t:
        w2v_size = _conf.getint('word2vec', 'size')
        # <description>自动生成关键词和摘要, 不再取网页中的Ｍeta信息</description>
    else:
        _logger.info(" 'word2vec', 'size', 向量大小")
        _conf.set('word2vec', 'size', w2v_size)

    _t = _conf.has_option('word2vec', 'window')
    if _t:
        w2v_window = _conf.getint('word2vec', 'window')
        # <description>自动生成关键词和摘要, 不再取网页中的Ｍeta信息</description>
    else:
        _logger.info(" 'word2vec', 'window', 窗口大小")
        _conf.set('word2vec', 'window', w2v_window)
    _t = _conf.has_option('word2vec', 'inFile')
    if _t:
        w2v_inFile = _conf.get('word2vec', 'inFile')
        # <description>自动生成关键词和摘要, 不再取网页中的Ｍeta信息</description>
    else:
        _conf.set('word2vec', 'inFile', '')
        _logger.info("'word2vec', 'inFile', ''词向量，必须要有源文件，inFile 配置缺失")
        exit(0)

    _t = _conf.has_option('word2vec', 'outFile')
    if _t:
        w2v_outFile = _conf.get('word2vec', 'outFile')
        # <description>自动生成关键词和摘要, 不再取网页中的Ｍeta信息</description>
    else:
        _conf.set('word2vec', 'outFile','')
        _logger.info("'word2vec', 'outFile',''词向量，必须要输出文件前缀，outFile 配置缺失")
        exit(0)



#算法 部分===================================================
#算法参数
# 词语的覆盖影响力因子
conf_alpha_f = 0.1
# 词语的位置影响力因子
conf_beta_f = 0.9
# 词语的频度影响力因子
conf_gamma_f = 0.0
conf_lambda_f = 30.0
conf_maxReadWordCount_int = 2000
conf_mergeNeighbor_bool = True

conf_我的方法是否合并词=False
conf_在合并词时是否删除旧词=False


_t = _conf.has_option('config', 'extractor.keyword.valid.word.count')
if _t:
    conf_maxReadWordCount_int = _conf.getint('config', "extractor.keyword.valid.word.count")
else:
    _logger.info("'config', 'extractor.keyword.valid.word.count',最大读取多少个词")
    _conf.set('config', 'extractor.keyword.valid.word.count', '2000')

_t = _conf.has_option('config', 'extractor.keyword.alpha')
if _t:
    conf_alpha_f = _conf.getfloat('config', "extractor.keyword.alpha")
else:
    _conf.set('config', 'extractor.keyword.alpha', '0.9')

_t = _conf.has_option('config', 'extractor.keyword.beta')
if _t:
    conf_beta_f = _conf.getfloat('config', "extractor.keyword.beta")
else:
    _conf.set('config', 'extractor.keyword.beta', '0.1')

_t = _conf.has_option('config', 'extractor.keyword.gamma')
if _t:
    conf_gamma_f = _conf.getfloat('config', "extractor.keyword.gamma")
else:
    _conf.set('config', 'extractor.keyword.gamma', '0.0')

_t = _conf.has_option('config', 'extractor.keyword.lambda')
if _t:
    conf_lambda_f = _conf.getfloat('config', "extractor.keyword.lambda")
else:
    _conf.set('config', 'extractor.keyword.lambda', '30')

# 这个合并词是夏天的方法
_t = _conf.has_option('config', 'extractor.keyword.merge.neighbor')
if _t:
    conf_mergeNeighbor_bool = _conf.getboolean('config', "extractor.keyword.merge.neighbor")
else:
    _logger.info("'config', 'extractor.keyword..merge.neighbor',合并结果的词")
    _conf.set('config', 'extractor.keyword.merge.neighbor', 'False')

# 以下配置的合并词是我的方法
conf_我的方法是否合并词=False
# my_Method_Is_Combination_Word
# 我的方法是否合并词
_t = _conf.has_option('config', 'my_Method_Is_Combination_Word')
if _t:
    conf_我的方法是否合并词 = _conf.getboolean('config', "my_Method_Is_Combination_Word")
else:
    _logger.info("'config', '我的方法是否合并词',训练前进行合并词")
    _conf.set('config', 'my_Method_Is_Combination_Word', 'False')

conf_在合并词时是否删除旧词=False
# Whether or not the old words are deleted when the words are merged
# my_Method_old_Word_Is_Del_When_Word_Merged
# 在合并词时是否删除旧词
_t = _conf.has_option('config', 'my_Method_old_Word_Is_Del_When_Word_Merged')
if _t:
    conf_在合并词时是否删除旧词 = _conf.getboolean('config', "my_Method_old_Word_Is_Del_When_Word_Merged")
else:
    _logger.info("'config', '我的方法是否合并词',训练前进行合并词")
    _conf.set('config', 'my_Method_old_Word_Is_Del_When_Word_Merged', 'False')

_conf.write(open(confFile,"w", encoding='utf8'))



