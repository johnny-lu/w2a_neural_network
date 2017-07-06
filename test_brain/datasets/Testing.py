from NeuralNetUtil import buildExamplesFromCarData,buildExamplesFromPenData
from NeuralNet import buildNeuralNet
from math import pow, sqrt

def average(argList):
    return sum(argList)/float(len(argList))

def stDeviation(argList):
    mean = average(argList)
    diffSq = [pow((val-mean),2) for val in argList]
    return sqrt(sum(diffSq)/len(argList))
'''
penData = buildExamplesFromPenData() 
def testPenData(hiddenLayers = [24]):
    return buildNeuralNet(penData,maxItr = 200, hiddenLayerList =  hiddenLayers)

carData = buildExamplesFromCarData()
def testCarData(hiddenLayers = [16]):
    return buildNeuralNet(carData,maxItr = 200,hiddenLayerList =  hiddenLayers)
'''
parcelData = buildExamplesFromParcelData()
def testParcelData(hiddenLayers = [4]):
    return buildNeuralNet(parcelData, maxItr = 200, hiddenLayerList = hiddenLayers)

# Vary the amount of perceptrons in the hidden layer from 0 to 40 inclusive in increments of 5, and
# get the max, average, and standard deviation of 5 runs of testPenData
def varyPerceptrons(func):
    numPerceptrons = 0

    maxAccs = []
    avgAccs = []
    stdDevs = []

    while numPerceptrons <= 40:
        accList = []
        for iteration in range(5):
            testAccuracy = 0.0
            if func == 0:
                nnet, testAccuracy = testPenData(hiddenLayers = [numPerceptrons])
            elif func == 1:
                nnet, testAccuracy = testCarData(hiddenLayers = [numPerceptrons])
            accList.append(testAccuracy)

        maxAccs.append((max(accList), numPerceptrons))
        avgAccs.append((average(accList), numPerceptrons))
        stdDevs.append((stDeviation(accList), numPerceptrons))
        numPerceptrons += 5

        print("Max accuracies: " + str(maxAccs))
        print("Average accuracies: " + str(avgAccs))
        print("Standard deviations: " + str(stdDevs))

# varyPerceptrons(0)
# varyPerceptrons(1)

penAccList = [0.885363, 0.908805, 0.902802, 0.905089, 0.905089]
print("Max (testPenData): " + str(max(penAccList)))
print("Average (testPenData): " + str(average(penAccList)))
print("Standard deviation (testPenData): " + str(stDeviation(penAccList)))

carAccList = [0.885471, 0.856675, 0.865838, 0.857984, 0.850785]
print("Max (testCarData): " + str(max(carAccList)))
print("Average (testCarData): " + str(average(carAccList)))
print("Standard deviation (testCarData): " + str(stDeviation(carAccList)))






