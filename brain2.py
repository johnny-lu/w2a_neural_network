# This file attempts to create a neural net which approximates weights to model a path. The
# assumption is made that y-values can be 1 or 0 (1 means on time, 0 means overtime). Given
# previous existing path data, it attempts to guess whether or not the end journey was on time or
# late.

from math import exp
from random import seed
from random import random
import MySQLdb
import sys


# Initialize a network
def initialize_network(n_inputs, n_hidden, n_outputs):
    network = list()
    hidden_layer = [{'weights': [random() for i in range(n_inputs + 1)]}
                    for i in range(n_hidden)]
    network.append(hidden_layer)
    output_layer = [{'weights': [random() for i in range(n_hidden + 1)]}
                    for i in range(n_outputs)]
    network.append(output_layer)
    return network

# Calculate neuron activation for an input
def activate(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights) - 1):
        activation += weights[i] * float(inputs[i])
    return activation

# Transfer neuron activation
def transfer(activation):
    return 1.0 / (1.0 + exp(-activation))

# Forward propagate input to a network output
def forward_propagate(network, row):
    inputs = row
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate(neuron['weights'], inputs)
            neuron['output'] = transfer(activation)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs

# Calculate the derivative of an neuron output


def transfer_derivative(output):
    return output * (1.0 - output)

# Backpropagate error and store in neurons


def backward_propagate_error(network, expected):
    for i in reversed(range(len(network))):
        layer = network[i]
        errors = list()
        if i != len(network) - 1:
            for j in range(len(layer)):
                error = 0.0
                for neuron in network[i + 1]:
                    error += (neuron['weights'][j] * neuron['delta'])
                errors.append(error)
        else:
            for j in range(len(layer)):
                neuron = layer[j]
                errors.append(expected[j] - neuron['output'])
        for j in range(len(layer)):
            neuron = layer[j]
            neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])

# Update network weights with error


def update_weights(network, row, l_rate):
    for i in range(len(network)):
        inputs = row[:-1]
        if i != 0:
            inputs = [neuron['output'] for neuron in network[i - 1]]
        for neuron in network[i]:
            for j in range(len(inputs)):
                neuron['weights'][j] += l_rate * \
                    neuron['delta'] * float(inputs[j])
            neuron['weights'][-1] += l_rate * neuron['delta']

# Train a network for a given n_runs with a learning speed of 0 < l_rate < 1 where l_rate is a percentage of
# weight allowed to change


def train_network(network, train, l_rate, n_runs, n_outputs):
    for run in range(n_runs):
        sum_error = 0
        for row in train:
            outputs = forward_propagate(network, row)
            expected = [0 for i in range(n_outputs)]
            expected[row[-1]] = 1
            sum_error += sum([(expected[i] - outputs[i]) **
                              2 for i in range(len(expected))])
            backward_propagate_error(network, expected)
            update_weights(network, row, l_rate)
        print('>Run=%d, lrate=%.3f, error=%.3f' % (run, l_rate, sum_error))

# Forward propogates a row through the network to determine whether or not it is late


def predict(network, row):
    outputs = forward_propagate(network, row)
    return outputs.index(max(outputs))

# Test the full process of training a network to predict based on given information


def main():
    seed(1)
    # Test training backprop algorithm
    # Create connection to a database of calculated differences between key statuses (time_diff table)
    db = MySQLdb.connect(
        user="root",
        passwd="powerpoint",
        db="delivery_status")
    cur = db.cursor()
    # Retrieve data and randomly split into a training and test set (total number of values used indicated by LIMIT)
    # A late parcel shipment is defined as total time being greater than or equal to the average total shipment time
    # X-values include the all columns selected before the late column, Y-value (1 or 0) defines late given above condition
    cur.execute('select consign_scinbound/30000, scinbound_lhdepart/30000, lhdepart_lharrive/30000, lharrive_ccout/30000,(select avg(total_time) from time_diff)-total_time > 0 as slow from time_diff where consign_scinbound + scinbound_lhdepart + lhdepart_lharrive + lharrive_ccout + ccout_signed - total_time = 0 ORDER BY RAND() LIMIT 15000;')
    dataset = cur.fetchall()
    # training set is marked off at certain point (convert to ratio later)
    training_set = dataset[:10000]
    # test set; picks up on where data was split to training point until end
    test_set = dataset[10000:]
    answers = [d[-1] for d in test_set]
    test_set = [d[0:-1] for d in test_set]  # fix
    n_inputs = len(training_set[0]) - 1  # number of columns to take a look at
    n_outputs = len(set([row[-1] for row in training_set]))
    network = initialize_network(n_inputs, 1, n_outputs)
    train_network(network, training_set, 0.2, 5, n_outputs)
    for layer in network:
        for items in layer:
            print 'weights: ' + str(items['weights'])

    # Test prediction accuracy
    count = 0
    total = 0
    for row in test_set:
        prediction = predict(network, row)
        if prediction == answers[total]:
            count += 1
        total += 1
    print str(float(count) / float(total) * 100) + '% guessed correctly'
    db.close()


main()
