from DataInterface import getDummyDataset2,getDummyDataset1,getConnect4Dataset, getExtraCreditDataSet
from DecisionTree import makeTree, setEntropy,infoGain
from Testing import printDemarcation, getAverageClassificaionRate

def testVotes(setFunc = setEntropy, infoFunc = infoGain):
    """Correct classification averate rate is about 0.95"""
    examples,attrValues,labelName,labelValues = getExtraCreditDataSet()
    print('Testing votes dataset. Number of examples %d.'%len(examples))
    tree = makeTree(examples, attrValues, labelName, setFunc, infoFunc)
    f = open('votes.out','w')
    f.write(str(tree))
    f.close()
    print('Tree size: %d.\n'%tree.count())
    print('Entire tree written out to votes.out in local directory\n')
    evaluation = getAverageClassificaionRate((examples,attrValues,labelName,labelValues))
    print('Results for training set:\n%s\n'%str(evaluation))
    printDemarcation()
    return (tree,evaluation)

testVotes()