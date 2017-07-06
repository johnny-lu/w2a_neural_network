import MySQLdb
import numpy
'''
ccout_signed, consign_scinbound, lharrive_ccout, lhdepart_lharrive, scinbound_lhdepart
'''


def reject_outliers(data, m=3.5):
    d = numpy.abs(data - numpy.median(data))
    mdev = numpy.median(d)
    s = d / mdev if mdev else 0.
    if isinstance(s, float):
        return data # when the median is 0, avoids division by 0
    return data[s < m]

def pull_training_data():
        # calculate median and stddev w/o outliers    
        db = MySQLdb.connect(
                user="root",
                 passwd="w2a88888",
                 db="delivery_status2")
        cur = db.cursor()

        cur.execute('select scinbound_lhdepart from time_diff')
        row = numpy.array(cur.fetchall())
        row = reject_outliers(row)
        median = numpy.median(row)
        # std = numpy.std(row)
        threshold = median
                
        cur.execute('''select scinbound_lhdepart/30000, (%d > scinbound_lhdepart) AS Y from time_diff where finished = 1 ORDER BY RAND();''' % threshold)
        training_data = cur.fetchall()
        cur.close()
        db.close()
        return training_data

def main():

    data = pull_training_data()
    train_data = data[:-10000]
    test_data = data[-10000:] # gets last 10000 lines as test data

    with open("datasets/train_scinbound_lhdepart_vsSelf", "w+") as f:
        for row in train_data:
            row = ','.join(map(str, row))
            f.write(row+"\n")

    with open("datasets/test_scinbound_lhdepart_vsSelf", "w+") as f:
        for row in test_data:
            row = ','.join(map(str, row))
            f.write(row+"\n")


if __name__ == "__main__":
    main()
