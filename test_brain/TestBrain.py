from NeuralNetUtil import buildExamplesFromParcelData
from NeuralNet import buildNeuralNet

parcelData = buildExamplesFromParcelData()

def testParcelData(hiddenLayers = [4]):
    return buildNeuralNet(parcelData, maxItr = 200, hiddenLayerList = hiddenLayers)

def main():
    numPerceptrons = 0

    maxAccs = []
    avgAccs = []
    stdDevs = []

    while numPerceptrons <= 40:
        accList = []
        for iteration in range(5):
            testAccuracy = 0.0
            nnet, testAccuracy = testParcelData(hiddenLayers = [numPerceptrons])
            accList.append(testAccuracy)

        maxAccs.append((max(accList), numPerceptrons))
        avgAccs.append((average(accList), numPerceptrons))
        stdDevs.append((stDeviation(accList), numPerceptrons))
        numPerceptrons += 5

        print("Max accuracies: " + str(maxAccs))
        print("Average accuracies: " + str(avgAccs))
        print("Standard deviations: " + str(stdDevs))

if __name__ == "__main__":
    main()
