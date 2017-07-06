import copy
import sys
from datetime import datetime
from math import exp
from random import random, randint, choice


class Perceptron(object):
    """
    Class to represent a single Perceptron in the net.
    """

    def __init__(self, inSize=1, weights=None):
        # number of perceptrons feeding into this one; add one for bias
        self.inSize = inSize + 1
        if weights is None:
            # weights of previous layers into this one, random if passed in as
            # None
            self.weights = [1.0] * self.inSize
            self.setRandomWeights()
        else:
            self.weights = weights

    def getWeightedSum(self, inActs):
        """
        Returns the sum of the input weighted by the weights.

        Inputs:
            inActs (list<float/int>): input values, same as length as inSize
        Returns:
            float
            The weighted sum
        """
        return sum([inAct * inWt for inAct, inWt in zip(inActs, self.weights)])

    def sigmoid(self, value):
        """
        Return the value of a sigmoid function.

        Args:
            value (float): the value to get sigmoid for
        Returns:
            float
            The output of the sigmoid function parametrized by
            the value.
        """
        """YOUR CODE"""
        return 1 / (1 + exp(-value))

    def sigmoidActivation(self, inActs):
        """
        Returns the activation value of this Perceptron with the given input.
        Same as g(z) in book.
        Remember to add 1 to the start of inActs for the bias input.

        Inputs:
            inActs (list<float/int>): input values, not including bias
        Returns:
            float
            The value of the sigmoid of the weighted input
        """
        """YOUR CODE"""
        inputs = [1.0] + inActs
        return self.sigmoid(self.getWeightedSum(inputs))

    def sigmoidDeriv(self, value):
        """
        Return the value of the derivative of a sigmoid function.

        Args:
            value (float): the value to get sigmoid for
        Returns:
            float
            The output of the derivative of a sigmoid function
            parametrized by the value.
        """
        """YOUR CODE"""
        # 1/(1 + e^value) = (1 + e^value)^-1
        # derivative = (-(1 + e^value)^-2)*(e^value) = -e^value / (1 +
        # e^value)^2
        return exp(value) / (pow((1 + exp(value)), 2))

    def sigmoidActivationDeriv(self, inActs):
        """
        Returns the derivative of the activation of this Perceptron with the
        given input. Same as g'(z) in book (note that this is not rounded.
        Remember to add 1 to the start of inActs for the bias input.

        Inputs:
            inActs (list<float/int>): input values, not including bias
        Returns:
            int
            The derivative of the sigmoid of the weighted input
        """
        """YOUR CODE"""
        acts = [1.0] + inActs
        return self.sigmoidDeriv(self.getWeightedSum(acts))

    def updateWeights(self, inActs, alpha, delta):
        """
        Updates the weights for this Perceptron given the input delta.
        Remember to add 1 to the start of inActs for the bias input.

        Inputs:
            inActs (list<float/int>): input values, not including bias
            alpha (float): The learning rate
            delta (float): If this is an output, then g'(z)*error
                           If this is a hidden unit, then the as defined-
                           g'(z)*sum over weight*delta for the next layer
        Returns:
            float
            Return the total modification of all the weights (sum of each abs(modification))
        """
        totalModification = 0
        """YOUR CODE"""
        # add 1 to the start of inActs for the bias input
        inputs = [1.0] + inActs

        for weightIndex in range(self.inSize):
            # first modification is for w0, which should stay the same
            modification = alpha * inputs[weightIndex] * delta
            totalModification += abs(modification)
            self.weights[weightIndex] += modification

        return totalModification

    def setRandomWeights(self):
        """
        Generates random input weights that vary from -1.0 to 1.0
        """
        for i in range(self.inSize):
            self.weights[i] = (random() + .0001) * (choice([-1, 1]))

    def __str__(self):
        """ toString """
        outStr = ''
        outStr += 'Perceptron with %d inputs\n' % self.inSize
        outStr += 'Node input weights %s\n' % str(self.weights)
        return outStr


class NeuralNet(object):
    """
    Class to hold the net of perceptrons and implement functions for it.
    """

    def __init__(self, layerSize):  # default 3 layer, 1 percep per layer
        """
        Initiates the NN with the given sizes.

        Args:
            layerSize (list<int>): the number of perceptrons in each layer
        """
        self.layerSize = layerSize  # Holds number of inputs and percepetrons in each layer
        self.outputLayer = []
        self.numHiddenLayers = len(layerSize) - 2
        self.hiddenLayers = [[] for x in range(self.numHiddenLayers)]
        self.numLayers = self.numHiddenLayers + 1

        # build hidden layer(s)
        for h in range(self.numHiddenLayers):
            for p in range(layerSize[h + 1]):
                # num of perceps feeding into this one
                percep = Perceptron(layerSize[h])
                self.hiddenLayers[h].append(percep)

        # build output layer
        for i in range(layerSize[-1]):
            # num of perceps feeding into this one
            percep = Perceptron(layerSize[-2])
            self.outputLayer.append(percep)

        # build layers list that holds all layers in order - use this structure
        # to implement back propagation
        self.layers = [self.hiddenLayers[h]
                       for h in range(self.numHiddenLayers)] + [self.outputLayer]

    def __str__(self):
        """toString"""
        outStr = ''
        outStr += '\n'
        for hiddenIndex in range(self.numHiddenLayers):
            outStr += '\nHidden Layer #%d' % hiddenIndex
            for index in range(len(self.hiddenLayers[hiddenIndex])):
                outStr += 'Percep #%d: %s' % (index,
                                              str(self.hiddenLayers[hiddenIndex][index]))
            outStr += '\n'
        for i in range(len(self.outputLayer)):
            outStr += 'Output Percep #%d:%s' % (i, str(self.outputLayer[i]))
        return outStr

    def feedForward(self, inActs):
        """
        Propagate input vector forward to calculate outputs.

        Args:
            inActs (list<float>): the input to the NN (an example)
        Returns:
            list<list<float/int>>
            A list of lists. The first list is the input list, and the others are
            lists of the output values of all perceptrons in each layer.
        """
        """YOUR CODE"""
        output = [inActs]

        inputs = list(inActs)
        for layer in self.layers:
            newInputs = []
            for unit in layer:
                newInputs.append(unit.sigmoidActivation(inputs))
            # These are the outputs for this layer and the inputs for the next
            # layer
            inputs = newInputs
            output.append(newInputs)

        return output

    def backPropLearning(self, examples, alpha):
        """
        Run a single iteration of backward propagation learning algorithm.
        See the text and slides for pseudo code.

        Args:
            examples (list<tuple<list<float>,list<float>>>):
              for each tuple first element is input(feature)"vector" (list)
              second element is output "vector" (list)
            alpha (float): the alpha to training with
        Returns
           tuple<float,float>

           A tuple of averageError and averageWeightChange, to be used as stopping conditions.
           averageError is the summed error^2/2 of all examples, divided by numExamples*numOutputs.
           averageWeightChange is the summed absolute weight change of all perceptrons,
           divided by the sum of their input sizes (the average weight change for a single perceptron).
        """
        # keep track of output
        averageError = 0
        averageWeightChange = 0
        numWeights = 0

        # Calculate output layer deltas
        for example in examples:  # for each example
            # keep track of deltas to use in weight change
            deltas = []
            # Neural net output list
            exampleInput = example[0]
            exampleOutput = example[1]
            allLayerOutput = self.feedForward(exampleInput)
            lastLayerOutput = allLayerOutput[-1]
            # Empty output layer delta list
            outLayerDeltas = []
            # iterate through all output layer neurons
            for outputNum in range(len(exampleOutput)):
                # Use the outputs from the layer before the outer layer as
                # inputs to the outer layer
                gPrime = self.outputLayer[outputNum].sigmoidActivationDeriv(
                    allLayerOutput[-2])
                error = exampleOutput[outputNum] - lastLayerOutput[outputNum]
                delta = error * gPrime
                averageError += error * error / 2
                outLayerDeltas.append(delta)
            deltas.append(outLayerDeltas)

            """
            Backpropagate through all hidden layers, calculating and storing
            the deltas for each perceptron layer.
            """
            # loop through the hidden layers backwards
            for layerNum in range(self.numHiddenLayers - 1, -1, -1):
                deltaCurrLayer = []
                # percepIndex refers to the index of a perceptron in the
                # current layer
                percepIndex = 0

                # This is the layer we're backpropagating to
                currLayer = self.layers[layerNum]
                # This is the layer we're backpropagating from
                nextLayer = self.layers[layerNum + 1]

                # Need to calculate weightedSum for all layers above the
                # current one
                for currentPercep in currLayer:
                    gPrime = currentPercep.sigmoidActivationDeriv(
                        allLayerOutput[layerNum])
                    # deltaj = g'(inj)sum(wj,k)deltak
                    weightedSum = 0.0
                    # Index of the delta corresponding to a perceptron in the
                    # next layer
                    nextPercepDeltaIndex = 0
                    for nextPercep in nextLayer:
                        # deltas[0] refers to the outer layer deltas b/c these were added first
                        # sum((wj,k)deltak), k ranges over nodes in the output layer
                        # wj,k = the kth perceptron's weight value for the input coming from the jth perceptron in the
                        # previous layer
                        weightedSum += nextPercep.weights[percepIndex + \
                            1] * deltas[0][nextPercepDeltaIndex]
                        nextPercepDeltaIndex += 1

                    deltaCurrPercep = gPrime * weightedSum
                    deltaCurrLayer.append(deltaCurrPercep)
                    percepIndex += 1

                # Put this delta at the front of the deltas list so it stays in
                # layer order
                deltas = [deltaCurrLayer] + deltas
            """Get output of all layers"""

            # if layerNum == 0:
            #     print(deltas)

            """
            Having aggregated all deltas, update the weights of the
            hidden and output layers accordingly.
            """
            for layerNum in range(0, self.numLayers):
                layer = self.layers[layerNum]
                for neuronNum in range(len(layer)):
                    weightMod = layer[neuronNum].updateWeights(
                        allLayerOutput[layerNum], alpha, deltas[layerNum][neuronNum])
                    averageWeightChange += weightMod
                    numWeights += layer[neuronNum].inSize
            # end for each example
        # calculate final output
        # number of examples x length of output vector
        averageError /= (len(examples) * len(examples[0][1]))
        averageWeightChange /= (numWeights)
        return averageError, averageWeightChange


def buildNeuralNet(
        examples,
        alpha=0.1,
        weightChangeThreshold=0.00008,
        hiddenLayerList=[1],
        maxItr=sys.maxsize,
        startNNet=None):
    """
    Train a neural net for the given input.

    Args:
        examples (tuple<list<tuple<list,list>>,
                        list<tuple<list,list>>>): A tuple of training and test examples
        alpha (float): the alpha to train with
        weightChangeThreshold (float):           The threshold to stop training at
        maxItr (int):                            Maximum number of iterations to run
        hiddenLayerList (list<int>):             The list of numbers of Perceptrons
                                                 for the hidden layer(s).
        startNNet (NeuralNet):                   A NeuralNet to train, or none if a new NeuralNet
                                                 can be trained from random weights.
    Returns
       tuple<NeuralNet,float>

       A tuple of the trained Neural Network and the accuracy that it achieved
       once the weight modification reached the threshold, or the iteration
       exceeds the maximum iteration.
    """
    examplesTrain, examplesTest = examples
    numIn = len(examplesTrain[0][0])
    numOut = len(examplesTest[0][1])
    time = datetime.now().time()
    if startNNet is not None:
        hiddenLayerList = [len(layer) for layer in startNNet.hiddenLayers]
    print(
        "Starting training at time %s with %d inputs, %d outputs, %s hidden layers, size of training set %d, and size of test set %d" %
        (str(time), numIn, numOut, str(hiddenLayerList), len(examplesTrain), len(examplesTest)))
    layerList = [numIn] + hiddenLayerList + [numOut]
    nnet = NeuralNet(layerList)
    if startNNet is not None:
        nnet = startNNet
    """
    YOUR CODE
    """
    iteration = 0
    trainError = 0
    weightMod = 0

    """
    Iterate for as long as it takes to reach weight modification threshold
    """
    # if iteration%10==0:
    #    print '! on iteration %d; training error %f and weight change %f'%(iteration,trainError,weightMod)
    # else :
    #    print '.',

    trainError, weightMod = nnet.backPropLearning(examplesTrain, alpha)
    while (weightMod >= weightChangeThreshold) and (iteration < maxItr):
        trainError, weightMod = nnet.backPropLearning(examplesTrain, alpha)
        iteration += 1

    time = datetime.now().time()
    print(
        'Finished after %d iterations at time %s with training error %f and weight change %f' %
        (iteration, str(time), trainError, weightMod))

    """
    Get the accuracy of your Neural Network on the test examples.
	For each text example, you should first feedforward to get the NN outputs. Then, round the list of outputs from the output layer of the neural net.
	If the entire rounded list from the NN matches with the known list from the test example, then add to testCorrect, else add to  testError.
    """

    testError = 0
    testCorrect = 0

    testAccuracy = 0  # num correct/num total

    # examplesTest is a tuple of inputs and outputs to compare against
    for example in examplesTest:
        # fullOutput[0] refers to the inputs
        # The rest of fullOutput contains lists of outputs for each perceptron
        # in each layer
        fullOutput = nnet.feedForward(example[0])
        outerLayerOutput = [round(output) for output in fullOutput[-1]]
        # example[1] refers to the outputs from each example
        # Check whether we got the correct outputs
        if outerLayerOutput == example[1]:
            testCorrect += 1
        else:
            testError += 1

    testAccuracy = testCorrect / float(len(examplesTest))

    print(
        'Feed Forward Test correctly classified %d, incorrectly classified %d, test percent error  %f\n' %
        (testCorrect, testError, testAccuracy))

    """return something"""

    return nnet, testAccuracy
