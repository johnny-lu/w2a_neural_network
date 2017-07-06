import numpy as np
import pymc3 as pm
import seaborn as sns
from theano import tensor as T
from statsmodels import datasets
from matplotlib import pyplot as plt
from pymc3.distributions.timeseries import GaussianRandomWalk

# removes outliers from either end of curve
# the higher the m or tolerance, the more data is intact
def reject_outliers(data, m=3.5):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / mdev if mdev else 0.
    if isinstance(s, float):
        return data # when the median is 0, avoids division by 0
    return data[s < m]

def main():
    if argv is None:
    argv = sys.argv

    tolerance = 5.  # for calculating outliers
    
    for filename in argv:
        name = getFilename(filename)  # stores the filename without extension

        # Open specified file within the same directory
        with open(filename) as data_file:
            data = np.array(json.load(data_file))
        data.sort()  # necessary
        data = reject_outliers(data, tolerance) # remove outliers skewing data

        minimum = min(data)
        maximum = max(data)
        mean = np.mean(data)
        std = np.std(data)
        x = np.linspace(minimum, maximum, 100)
        # probability density function = norm.pdf,
        # norm.sf = survival function
        # norm.cdf = cumulative distribution function
        pdf = stats.norm.pdf(x, mean, std)
        plt.figure()
        plt.plot(x, pdf)
        plt.xlabel('Time in seconds')
        plt.grid()


if __name__ == "__main__":
    main(sys.argv[1:])
