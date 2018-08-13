
# /**
#  * 一个词语，包含文本在句子中
#  * Date: 3/10/13 3:03 PM
#  */
class WordNode():
    def __init__(self, name, pos, count, importance, orderNum=0):
        # /**该节点后面相邻的词语集合 */
        self._rightNeighbors = []
        # /** 该节点前面相邻的节点集合*/
        self._leftNeighbors = []

        # /**
        #  * 词语的名称
        #  */
        self._name = name

        # /**
        #  * 词性
        #  */
        self._pos = pos

        # /**
        #  * 词语在文本中出现的数量
        #  */
        self._count = count

        # /**
        #  * 词语的重要性，如果在标题中出现，为λ(λ>1, 默认为5）, ,否则为1
        #  */
        self._importance = importance

        # /**
        #  * 当前节点所指向的节点名称及其出现次数
        #  */
        self._adjacentWordsDict = {}

        self._orderNumber=orderNum

    def getRightNeighbors(self):
        """返回一个list 列表"""
        return self._rightNeighbors

    def getLeftNeighbors(self):
        """返回一个list 列表"""
        return self._leftNeighbors

    def getName(self):
        return self._name

    def setName(self,name):
        self._name = name

    def getPos(self):
        return self._pos
    def setPos(self, pos):
        self._pos = pos

    def getCount(self):
        return self._count

    def setCount(self, count):
        self._count = count

    def incCount(self):
        self._count+=1

    def getImportance(self):
        return self._importance

    def setImportance(self, importance):
        self._importance = importance

    def getOrderNumber(self):
        """返回词在文本中的序号"""
        return self._orderNumber
    def setOrderNumber(self, number):
        self._orderNumber = number

    def getAdjacentWords(self):
        """返回一个字典Map<String, Integer>"""
        return self._adjacentWordsDict

    def setAdjacentWords(self, adjacentWords):
        self._adjacentWordsDict = adjacentWords

    def addAdjacentWord(self, word):
        # d = {'site': 'http://www.jb51.net', 'name': 'jb51', 'is_good': 'yes'}
        # # 方法1：通过has_key
        # print  d.has_key('site')
        # # 方法2：通过in
        # print     'body' in d.keys()

        if (word in self._adjacentWordsDict.keys()):
            self._adjacentWordsDict[word]+=1
        else:
            self._adjacentWordsDict[word] = 1

    def addLeftNeighbor(self, word):
        self._leftNeighbors.append(word)

    def addRightNeighbor(self, word):
        self._rightNeighbors.append(word)


    def toString(self):
        return "WordNode{" + "name='" + self._name + "'" + ", features='" + self._pos + "'" + ", count=" + self._count + ", importance=" + self._importance +"}"

