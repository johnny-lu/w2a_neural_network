from lifelines.statistics import logrank_test
import scipy.stats as stats
import numpy as np
import pickle
import pandas

dtype = [('T', 'float64'), ('E', 'bool')]

with open('scinbound_lhdepart_table', 'rb') as data_file:
            data1 = np.array(pickle.load(data_file) , dtype = dtype)
with open('scinbound_lhdepart2_table', 'rb') as data_file:
            data2 = np.array(pickle.load(data_file) , dtype = dtype)

df1 = pandas.DataFrame(data1, columns=['T', 'E'])
df2 = pandas.DataFrame(data2, columns=['T', 'E'])

T1 = df1['T'] # array of durations/time
E1 = df1['E'] # array of booleans/flags
T2 = df2['T'] # array of durations/time
E2 = df2['E'] # array of booleans/flags

results = logrank_test(T1, T2, event_observed_A=E1, event_observed_B=E2)
results.print_summary()

# for analyzing the statistical correlation between any two routes' data.
