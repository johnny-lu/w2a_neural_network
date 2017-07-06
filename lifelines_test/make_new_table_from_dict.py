import re
import sys
import json
import pickle
import numpy as np

# use regex to grab name of files without the extension
def getFilename(filename):
    matchObj = re.match('(.+?)(\.[^.]*$|$)', filename, re.M | re.I)
    return matchObj.group(1)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    for filename in argv:

        with open(filename) as data_file:
            curr_dict = json.load(data_file)
            print(type(curr_dict))
            assert isinstance(curr_dict, dict)

        name = getFilename(filename)  # stores the filename without extension
        allValues = curr_dict.values()
        assert isinstance(allValues, list)

        median = np.median(allValues)
        sdev = np.std(allValues)
        lateTime = median + sdev
        print lateTime # remove later
        myList = []

        for i in allValues:
            if i >= 0:
                isLate = (i - lateTime) >= 0 # 0 or false for okay, 1 for late.
            else: 
                isLate = 0 # if negative time, then ahead of schedule!
            myList.append((i, isLate))

        with open(name + "_table", "wb") as outfile:
            pickle.dump(myList, outfile)


if __name__ == "__main__":
    main(sys.argv[1:])
