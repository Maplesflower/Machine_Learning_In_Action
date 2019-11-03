from numpy import *

'''4_1词表到向量的转换函数
2019_11_3
'''
#创建一些实验样本
def loadDataSet():
    #进行词条切分后的文档集合
    postingList = [['my', 'dog', 'has', 'flea', 'problem', 'help', 'please'], \
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'], \
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'], \
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'], \
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'], \
                   ['quit', 'buying', 'wortless', 'dog', 'food', 'stupid']]
    #1代表侮辱性文字，0代表正常言论，类别标签的集合
    classVec = [0, 1, 0, 1, 0, 1] 
    return postingList, classVec
#创建一个包含在所有文档中出现的不重复词的列表
def creatVocabList(dataSet):
    #1创建一个空集
    vocabSet = set([])
    for document in dataSet:
        #2创建两个集合的并集,将每个词汇加入集合，重复的就不再加入
        vocabSet = vocabSet | set(document)
    return list(vocabSet)
#表示词汇表中的单词在输入文档中是否出现
def setOfWords2Vec(vocabList, inputSet):
    #3创建一个其中所含元素都为0的向量
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        #如果出现词汇表中的单词，则将输出的文档向量中的对应值设为1
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word: %s is not in my Vocabulary!" % word)
    return returnVec

'''4_2朴素贝叶斯分类器训练函数
2019_11_3
'''
#trainMatrix: 输入参数为文档矩阵
#trainCategory: 每篇文档类别标签所构成的向量
def trainNB0(trainMatrix, trainCategory):
    #求出整个矩阵中有多少个实例(6)
    numTrainDocs = len(trainMatrix)
    #求出的词列表中词的总数(33)
    numWords = len(trainMatrix[0])
    #计算侮辱言论的例子在总的例子中比重
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    #1初始化概率
    #数字0表示非侮辱性文档，数字1表示侮辱性文档
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        #如果该条实例对应是侮辱性标签
        if trainCategory[i] == 1:
            #2向量相加
            #增加侮辱性词条的数值,向量加,维度是33
            p1Num += trainMatrix[i]
            #同时增加总的词条的数值
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    #3对每个元素做除法
    p1Vect = log(p1Num / p1Denom)
    p0Vect = log(p0Num / p0Denom)
    return p0Vect, p1Vect, pAbusive

'''4_3朴素贝叶斯分类函数
2019_11_3
'''

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():
    listOPosts, listClasses = loadDataSet()
    myVocabList = creatVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb))
    testEntry = ['stupid', 'garbage']
    thisDoc =array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb))

if __name__ == '__main__':
    '''测试词表转换为向量函数'''
    listOPosts, listClasses = loadDataSet()
    myVocabList = creatVocabList(listOPosts)
    print("词汇列表")
    print(myVocabList)
    print("\n转换第一行的词为向量")
    print(setOfWords2Vec(myVocabList, listOPosts[0]))
    
    '''测试朴素贝叶斯分类器训练函数'''
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V, p1V, pAb = trainNB0(trainMat, listClasses)
    print("pAb")
    print(pAb)
    print("\np0V")
    print(p0V)
    print('\np1V')
    print(p1V)

    '''测试朴素贝叶斯分类函数'''
    print(testingNB())
