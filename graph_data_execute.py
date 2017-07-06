import re
import sys
import json
import math
import datetime
import numpy as np
import matplotlib.dates
import scipy.stats as stats
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# removes outliers from either end of curve
# the higher the m or tolerance, the more data is intact
def reject_outliers(data, m=3.5):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0.
    return data[s < m]

# use regex to grab name of files without the extension
def getFilename(filename):
    matchObj = re.match('(.+?)(\.[^.]*$|$)', filename, re.M | re.I)
    return matchObj.group(1)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    tolerance = 5.  # for calculating outliers

    for filename in argv:
        name = getFilename(filename)  # stores the filename without extension

        # Open specified file within the same directory
        with open(filename) as data_file:
            data = np.array(json.load(data_file))
        data.sort()  # necessary?
        data = reject_outliers(data, tolerance) # remove outliers skewing data

        minimum = min(data)
        maximum = max(data)
        mean = np.mean(data)
        std = np.std(data)

        # write to log.txt file
        log = open(name + "_log.txt", "w")
        log.write(name + "\n")
        log.write("Min:	" + str(datetime.timedelta(seconds=minimum)) + "\n")
        log.write("Max:	" + str(datetime.timedelta(seconds=maximum)) + "\n")
        log.write("Mean: " + str(datetime.timedelta(seconds=mean)) + "\n")
        log.write("Std:	" + str(datetime.timedelta(seconds=std)) + "\n")
        log.write("Tolerance:	" + str(tolerance) + "\n")
        log.close()
        '''
        print "\n" + name
        print "Min:", datetime.timedelta(seconds=minimum)
        print "Max:", datetime.timedelta(seconds=maximum)
        print "Median:", datetime.timedelta(seconds=median)
        print "Std:", datetime.timedelta(seconds=std)
        '''
        # probability density function = norm.pdf,
        # norm.sf = survival function
        pdf = stats.norm.sf(data, mean, std)
        plt.figure()
        plt.plot(data, pdf)
        plt.xlabel('Time in seconds')
        plt.grid()
        plt.savefig(filename=name + ".pdf", format='pdf')
        # plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
