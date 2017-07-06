import re
import sys
import numpy as np
from matplotlib import pyplot as plt
import pickle
from lifelines import KaplanMeierFitter
import pandas

# use regex to grab name of files without the extension
def getFilename(filename):
    matchObj = re.match('(.+?)(\.[^.]*$|$)', filename, re.M | re.I)
    return matchObj.group(1)

def main(argv=None):
    if argv is None:
        argv = sys.argv

    dtype = [('T', 'float64'), ('E', 'bool')]

    for filename in argv:
        name = getFilename(filename)  # stores the filename without extension

        # Open specified file within the same directory
        with open(filename, 'rb') as data_file:
            data = np.array(pickle.load(data_file) , dtype = dtype)
        #data.sort()  # necessary?

        df = pandas.DataFrame(data, columns=['T', 'E'])
        kmf = KaplanMeierFitter()
        T = df['T'] # array of durations/time
        E = df['E'] # array of booleans/flags
        #t = np.linspace()
        kmf.fit(T, event_observed = E, label = name)
        #print name # remove later
        #print kmf.median_
        #kmf.survival_function_.plot() # to plot survival function
        xy = kmf.plot() # use this to get coordinates
        xvals = xy.get_xdata()
        plt.xlabel('Time in seconds')
        plt.grid()
        plt.xlim(xmin=0) # assumes we only care about non-negative time
        plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
