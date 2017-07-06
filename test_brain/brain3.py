from NeuralNetUtil import buildExamplesFromParcelData
from NeuralNet import buildNeuralNet
from math import pow, sqrt
import pickle

parcelData = buildExamplesFromParcelData()

def average(argList):
    return sum(argList)/float(len(argList))

def stDeviation(argList):
    mean = average(argList)
    diffSq = [pow((val-mean),2) for val in argList]
    return sqrt(sum(diffSq)/len(argList))

def testParcelData(hiddenLayers = [4]):
    # data = buildNeuralNet(parcelData, maxItr = 100, hiddenLayerList = hiddenLayers)
    # print type(data[0])
    return buildNeuralNet(parcelData, maxItr = 100, hiddenLayerList = hiddenLayers) # changed maxItr from 200 to 100

def main():
    numPerceptrons = 0

    maxAccs = []
    avgAccs = []
    stdDevs = []

    while numPerceptrons <= 25: # do NOT need this many layers! Takes too long. Orignally 40
        accList = []
        for iteration in range(1): # change range to run more tests
            testAccuracy = 0.0
            nnet, testAccuracy = testParcelData(hiddenLayers = [numPerceptrons])
            accList.append(testAccuracy)

            # save the neural net
            with open("neuralNet.file", "wb") as f:
                pickle.dump(nnet, f, pickle.HIGHEST_PROTOCOL)

        maxAccs.append((max(accList), numPerceptrons))
        avgAccs.append((average(accList), numPerceptrons))
        stdDevs.append((stDeviation(accList), numPerceptrons))
        numPerceptrons += 5

        print("Max accuracies: " + str(maxAccs))
        print("Average accuracies: " + str(avgAccs))
        print("Standard deviations: " + str(stdDevs))
    

if __name__ == "__main__":
    main()
