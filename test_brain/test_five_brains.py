from NeuralNet import buildNeuralNet
import pickle
import numpy as np

'''
ccout_signed, consign_scinbound, lharrive_ccout, lhdepart_lharrive, scinbound_lhdepart
'''
def getNNParcelData(fileString="datasets/parcel-training.txt", limit=100000):
    '''
    returns limit # of examples from parcel-training file
    '''
    inVec = np.array([]) # change later to add more legs.
    outVec = np.array([]) # change later? Use percentage past middle instead of flag?
    examples = []
    data = open(fileString)
    lineNum = 0
    for line in data:
        '''
         data attributes = [omconsign_scinbound, scinbound_lhdepart, 
                            lhdepart_lharrive, ccin_ccout, ccout_signed,
                            late flag]
        '''
        count = 0
        for val in line.split(','):
            if count == 1: # number of legs in journey
                outVec = np.append(outVec, [float(val)])
            else:
                inVec = np.append(inVec, [float(val)])
            count = count + 1

        lineNum = lineNum + 1
        if (lineNum >= limit):
            break

    inVecNorm = inVec/sum(inVec)
    i = 0
    while i < len(outVec):
        examples.append(([inVecNorm[i]], [outVec[i]]))
        i += 1
    return examples


hiddenLayers = [1]

train_ccout_signed = getNNParcelData('datasets/train_ccout_signed_vsSelf')
test_ccout_signed = getNNParcelData('datasets/test_ccout_signed_vsSelf')
ccout_signed_examples = (train_ccout_signed, test_ccout_signed)
ccout_signedNN = buildNeuralNet(ccout_signed_examples, maxItr = 100, hiddenLayerList = hiddenLayers)[0]
# save the neural net
with open("ccout_signed_neuralNet.file", "wb") as f:
    pickle.dump(ccout_signedNN, f, pickle.HIGHEST_PROTOCOL)


train_consign_scinbound = getNNParcelData('datasets/train_consign_scinbound_vsSelf')
test_consign_scinbound = getNNParcelData('datasets/test_consign_scinbound_vsSelf')
consign_scinbound_examples = (train_consign_scinbound, test_consign_scinbound)
consign_scinboundNN = buildNeuralNet(consign_scinbound_examples, maxItr = 100, hiddenLayerList = hiddenLayers)[0]
# save the neural net
with open("consign_scinbound_neuralNet.file", "wb") as f:
    pickle.dump(consign_scinboundNN, f, pickle.HIGHEST_PROTOCOL)

train_lharrive_ccout = getNNParcelData('datasets/train_lharrive_ccout_vsSelf')
test_lharrive_ccout = getNNParcelData('datasets/test_lharrive_ccout_vsSelf')
lharrive_ccout_examples = (train_lharrive_ccout, test_lharrive_ccout)
lharrive_ccoutNN = buildNeuralNet(lharrive_ccout_examples, maxItr = 100, hiddenLayerList = hiddenLayers)[0]
# save the neural net
with open("consign_scinbound_neuralNet.file", "wb") as f:
    pickle.dump(lharrive_ccoutboundNN, f, pickle.HIGHEST_PROTOCOL)

train_lhdepart_lharrive = getNNParcelData('datasets/train_lhdepart_lharrive_vsSelf')
test_lhdepart_lharrive = getNNParcelData('datasets/test_lhdepart_lharrive_vsSelf')
lhdepart_lharrive_examples = (train_lhdepart_lharrive, test_lhdepart_lharrive)
lhdepart_lharriveNN = buildNeuralNet(lhdepart_lharrive_examples, maxItr = 100, hiddenLayerList = hiddenLayers)[0]
# save the neural net
with open("lhdepart_lharrive_neuralNet.file", "wb") as f:
    pickle.dump(lhdepart_lharriveNN, f, pickle.HIGHEST_PROTOCOL)

train_scinbound_lhdepart = getNNParcelData('datasets/train_scinbound_lhdepart_vsSelf')
test_scinbound_lhdepart = getNNParcelData('datasets/test_scinbound_lhdepart_vsSelf')
scinbound_lhdepart_examples = (train_scinbound_lhdepart, test_scinbound_lhdepart)
scinbound_lhdepartNN = buildNeuralNet(scinbound_lhdepart_examples, maxItr = 100, hiddenLayerList = hiddenLayers)[0]
# save the neural net
with open("scinbound_lhdepart_neuralNet.file", "wb") as f:
    pickle.dump(scinbound_lhdepartNN, f, pickle.HIGHEST_PROTOCOL)

