import pickle
from NeuralNet import buildNeuralNet, predict, buildNeuralNetComplete
from NeuralNetUtil import buildExamplesFromParcelData, getNNData

parcelData = buildExamplesFromParcelData()[0]
predictData = buildExamplesFromParcelData()[1]

with open("neuralNet.file", "rb") as f:
    nnet = pickle.load(f)

#predict(predictData, nnet = nnet) # predict using predict function
#nnet = buildNeuralNetComplete(parcelData, maxItr = 10, startNNet=nnet) # load old nnet to test
#nnet = buildNeuralNetComplete(parcelData, maxItr = 10, hiddenLayerList=[5]) # remove later
parcelData = getNNData(inVecSize=4)
nnet = buildNeuralNet(parcelData, maxItr = 10, hiddenLayerList=[5]) # build new nnet
#print predict(predictData, nnet = nnet) # predict using predict function
#print nnet
'''
# save the neural net
with open("neuralNet.file", "wb") as f:
    pickle.dump(newNet, f, pickle.HIGHEST_PROTOCOL)
'''
# print nnet
