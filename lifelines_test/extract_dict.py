import re
import sys
import json

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
            print(curr_dict)
            assert isinstance(curr_dict, dict)

        name = getFilename(filename)  # stores the filename without extension
        with open(name + "_list.json", "w") as outfile:
            json.dump(curr_dict.values(), outfile)


if __name__ == "__main__":
    main(sys.argv[1:])
