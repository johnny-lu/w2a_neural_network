def getNNParcelData(fileString="datasets/parcel-training.txt", limit=100000):
    '''
    returns limit # of examples from parcel-training file
    '''
    examples = []
    data = open(fileString)
    lineNum = 0
    for line in data:
        '''
         data attributes = [omconsign_scinbound, scinbound_lhdepart,
                            lhdepart_lharrive, ccin_ccout, ccout_signed,
                            late flag]
        '''
        inVec = [0, 0, 0, 0]  # change later to add more legs.
        # change later? Use percentage past middle instead of flag?
        outVec = [0]
        count = 0
        for val in line.split(','):
            if count == 4:  # number of legs in journey
                outVec[0] = float(val)  # change later?
            else:
                inVec[count] = float(val)
            count = count + 1
        inVecNorm = [float(i) / sum(inVec) for i in inVec]
        examples.append((inVecNorm, outVec))
        lineNum = lineNum + 1
        if (lineNum >= limit):
            break
    return examples


# Used for testing purposes (brain3.py)
def buildExamplesFromParcelData(size=1000000):  # size originally 10000
    '''
    build Neural-network friendly data struct

    parcel data format
    5 input(attributes): time in seconds for each respective leg of route
    5 output values: time in seconds for each respective leg of route??
    '''

    parcelDataTrainList = getNNParcelData('datasets/parcel-training.txt')
    parcelDataTestList = getNNParcelData('datasets/parcel-test.txt')

    return parcelDataTrainList, parcelDataTestList


def buildPotentialHiddenLayers(numIns, numOuts):
    """
    This builds a list of lists of hidden layer layouts
    numIns - number of inputs for data
    some -suggestions- for hidden layers - no more than 2/3 # of input nodes per layer, and
    no more than 2x number of input nodes total (so up to 3 layers of 2/3 # ins max
    """
    resList = []
    tmpList = []
    maxNumNodes = max(numOuts + 1, 2 * numIns)
    if (maxNumNodes > 15):
        maxNumNodes = 15

    for lyr1cnt in range(numOuts, maxNumNodes):
        for lyr2cnt in range(numOuts - 1, lyr1cnt + 1):
            for lyr3cnt in range(numOuts - 1, lyr2cnt + 1):
                if (lyr2cnt == numOuts - 1):
                    lyr2cnt = 0

                if (lyr3cnt == numOuts - 1):
                    lyr3cnt = 0
                tmpList.append(lyr1cnt)
                tmpList.append(lyr2cnt)
                tmpList.append(lyr3cnt)
                resList.append(tmpList)
                tmpList = []
    return resList


def getNNData(fileString="datasets/parcel-training.txt",
              limit=100000, inVecSize=5, outVecSize=1):
    '''
    returns limit # of examples from data file
    '''
    assert inVecSize > 0
    assert outVecSize > 0

    examples = []
    data = open(fileString)
    lineNum = 0
    for line in data:
        '''
        data attributes example = [omconsign_scinbound, scinbound_lhdepart,
                                   lhdepart_lharrive, ccin_ccout, ccout_signed,
                                   late flag]
        '''
        inVec = [0] * inVecSize  # number of input neurons per layer
        # change later? Use percentage past middle instead of flag?
        outVec = [0] * outVecSize # number of output neurons
        count = 0
        for val in line.split(','):
            if count == inVecSize:  # number of input
                outVec[0] = float(val)  # change later with number of output
            else:
                inVec[count] = float(val)
            count = count + 1
        inVecNorm = [float(i) / sum(inVec) for i in inVec]
        examples.append((inVecNorm, outVec))
        lineNum = lineNum + 1
        if (lineNum >= limit):
            break
    return examples
