from pandas import read_csv
from keras.models import Sequential, load_model, Model
from keras.layers import Dense
from os.path import isfile
import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas

def graph(aModel):
    
    plt.plot(aModel.history['val_acc'])
    plt.plot(aModel.history['acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.ylim([0,1])
    plt.legend(['train','test'], loc = 'upper left')
    plt.show()
    return

def normalize (df):
    INVALIDS = ['receiver_state', 'receiver_city','receiver_town','receiver_zip','receiver_district','pay_scinbound', 'pay_lhdepart', 'pay_lharrive', 'pay_ccout', 'total_time']
    STATUSES = ['pay_consign', 'consign_scinbound', 'scinbound_lhdepart','lhdepart_lharrive', 'lharrive_ccout', 'ccout_signed']

    result = df.copy()
    if isfile('model_std_mean'):
        f = open('model_std_mean', 'r')
        for feature_name in df.columns:
            if feature_name in INVALIDS:
                pass
            else:
                info = f.readline().split('\t')
                currCol = df[feature_name]
                result[feature_name] = (currCol-float(info[1]))/float(info[2])
        f.close()
    else:

        with open('model_std_mean', 'wb') as out:
            for feature_name in df.columns:
                currCol = df[feature_name]
                if feature_name in INVALIDS:
                    pass
                else:
                    currCol = df[feature_name]
                    result[feature_name] = (currCol-currCol.mean())/currCol.std()
            for i in STATUSES:
                out.write(i + ':\t' + str(df[i].mean()) + '\t' + str(df[i].std()) + '\n')
    return result

DAY = 60*60*24 # seconds
STATUSES = ['pay_consign', 'consign_scinbound', 'scinbound_lhdepart','lhdepart_lharrive', 'lharrive_ccout', 'ccout_signed']
OUTS = ['pay_scinbound', 'pay_lhdepart', 'pay_lharrive', 'pay_ccout', 'total_time']

number = 0
print ('Reading data...')
series = read_csv('finished_transactions.csv', header = 0, index_col=0)
print ('Normalizing data...')
series = normalize(series)
training = series

for i in STATUSES:
    if number == 5:
        break
    number += 1
    cols = list(STATUSES[:number])
    training_in = np.array(training[STATUSES[:number]])
    median = np.median(series[OUTS[number-1]])
    training_out = [[d] for d in training[OUTS[number-1]].tolist()]
    std = np.std(series[STATUSES[number-1]])

    
    for i in range(len( training_out)):
        if training_out[i] <= median:
            training_out[i] = [0,0,0,1]
        elif training_out[i] <= median + std:
            training_out[i] = [0,0,1,0]
        elif training_out[i] <= median + 2*std:
            training_out[i] = [0,1,0,0]
        else:
            training_out[i] = [1,0,0,0]

    filename = 'curr_perf%d' % number # formerly 'my_weird4_model%d'

    try:
        model = load_model(filename)
        print('Model Loaded')
        model.summary()
        history = model.fit(training_in,training_out, validation_split = 0.2,epochs=10, batch_size=100)
        #graph(history)
        model.save(filename)
    except:
        print('Missing save. Making Model.')
        model = Sequential()

        model.add(Dense(8, input_dim = number, activation = 'relu')) # input layer (number of neurons, number of inputs, activation function) Hard coded input number, change later
        model.add(Dense(8, activation = 'relu')) # output layer (number of output neurons, activation function)
        model.add(Dense(4, activation = 'softmax')) # output layer (number of output neurons, activation function)

        model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
        model.summary() # remove later
        history = model.fit(training_in,training_out, validation_split = 0.2,epochs=50, batch_size=100)
        #graph(history)

        model.save(filename)

