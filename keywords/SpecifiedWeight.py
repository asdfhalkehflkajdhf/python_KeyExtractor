

# /**
#  * 人工设置的权重，保持了特殊词语的权重信息，这个在这里并没用使用，是一个全局变量
#  * <p/>
#  * SpecifiedWeight
#  * Date: 4/2/13 2:44 PM
#  */
global __wordDict
__wordDict= {}


def setWordWeight(word, weight):
    __wordDict[word] = weight


def removeWord(word):
    if word in list(__wordDict.keys()):
        del __wordDict[word]


def getWordWeight(word, defaultValue):
    # dict.get(key, default=None)
    # 返回指定键的值，如果值不在字典中返回default值
    return __wordDict.get(word, defaultValue)



if __name__ == "__main__":
    setWordWeight('a',1)
    setWordWeight('b',2)

    setWordWeight('c', 3)

    removeWord('d')

    t =getWordWeight('b',0)
    print(t)
    t =getWordWeight('f', 0)
    print(t)