import re
import sys
import json
import math
import datetime
import numpy as np
import matplotlib.dates
import scipy.stats as stats
from bisect import bisect_left
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# removes outliers from either end of curve
# the higher the m or tolerance, the more data is intact
def reject_outliers(data, m=3.5):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0.
    if isinstance(s, float):
        return data  # when the median is 0, avoids division by 0
    return data[s < m]

# use regex to grab name of files without the extension
def getFilename(filename):
    matchObj = re.match('(.+?)(\.[^.]*$|$)', filename, re.M | re.I)
    return matchObj.group(1)

# use bisect to find the index of the closest matching number in a list
# assumes list is pre-sorted; returns index of smaller of two numbers if tied.
def takeClosest(myList, myNumber):
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return 0
    if pos == len(myList):
        return -1
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
        return pos
    else:
        return pos - 1


# for writing into a log file the median, stdev, and other useful information
# that can be used later. log file is in .txt
def writeToLog(data, name):
    
    # calculate using the data
    minimum = min(data)
    maximum = max(data)
    median = np.median(data)
    std = np.std(data)

    # write to log.txt file
    log = open(name + "_log.txt", "w")
    log.write(name + "\n")
    log.write("Min:	" + str(datetime.timedelta(seconds=minimum)) + "\n")
    log.write("Max:	" + str(datetime.timedelta(seconds=maximum)) + "\n")
    log.write("Median: " + str(datetime.timedelta(seconds=median)) + "\n")
    log.write("Std:	" + str(datetime.timedelta(seconds=std)) + "\n")
    log.write("Median+Std:    " +
              str(datetime.timedelta(seconds=std + median)) + "\n")
    log.close()
    # for printing onto terminal
    '''
    print "\n" + name
    print "Min:", datetime.timedelta(seconds=minimum)
    print "Max:", datetime.timedelta(seconds=maximum)
    print "Median:", datetime.timedelta(seconds=median)
    print "Std:", datetime.timedelta(seconds=std)
    '''

def main(argv=None):
    if argv is None:
        argv = sys.argv

    tolerance = 5.  # for calculating outliers

    for filename in argv:
        name = getFilename(filename)  # stores the filename without extension

        # Open specified file within the same directory
        with open(filename) as data_file:
            data = np.array(json.load(data_file))
        data.sort()  # necessary
        data = reject_outliers(data, tolerance)  # remove outliers skewing data

        minimum = min(data)
        maximum = max(data)
        median = np.median(data)
        std = np.std(data)

        writeToLog(data, name) # writes data to .txt file

        '''
        x = np.linspace(minimum, maximum, 100)
        probability density function = norm.pdf,
        norm.sf = survival function
        norm.cdf = cumulative distribution function
        '''

        pdf = stats.norm.pdf(data, median, std)
        plt.figure()
        xy = plt.plot(data, pdf)  # change later/rename?
        xvals = xy[0].get_xdata()  # np array with all x data
        yvals = xy[0].get_ydata()  # np array with all y data
        # median can be changed to any number
        idx = takeClosest(xvals.tolist(), median)
        # the probability of taking more than this amount of time:
        #print (yvals[idx]) * 100
        plt.xlabel('Time in seconds')
        plt.grid()
        plt.xlim(xmin=0)  # assumes we only care about non-negative time
        plt.savefig(filename=name + ".pdf", format='pdf') # save the plot image
        #plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
