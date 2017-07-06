# imports
import MySQLdb
import json
import numpy


def calc_diff(prev, curr):
    start_time = prev[2]
    end_time = curr[2]
    timediff = (end_time - start_time).total_seconds()
    return timediff


'''
def find_tids(cursor):
    cursor.execute("""SELECT DISTINCT tid, status FROM delivery_statuses
                            WHERE  status = "SIGNED" ORDER BY RAND();""")
    ids = cursor.fetchall()
    return ids[:15000], ids[15000:45000], ids[45000:]
'''


def process_ids(cursor, ids, statuses, storage):
    num = 0
    for tid in ids:
        tidString = str(tid[0])
        num += 1
        print(num)
        check_times(tidString, cursor, storage, statuses)


def check_times(tid, cursor, storage, statuses):
    # beginning status, should be OM CONSIGN
    cursor.execute("""SELECT *
                FROM delivery_statuses
                WHERE TID = %s
                AND (status = %s)
                ORDER BY statustime LIMIT 1""",
                   (tid, statuses[0]))
    row = cursor.fetchall()
    first = row[0]
    previous = row[0]

    for i in range(1, len(statuses)):
        cursor.execute(
            """SELECT *
                    FROM delivery_statuses
                    WHERE TID = %s
                    AND (status = %s)
                    ORDER BY statustime DESC LIMIT 1""",
            (tid, statuses[i]))
        row = cursor.fetchall()
        if len(row) > 0:
            current = row[0]
            delta_time = calc_diff(previous, current)
            if delta_time > 0:
                storage[i - 1] = numpy.append(storage[i - 1], delta_time)
            else:
                storage[i - 1] = numpy.append(storage[i - 1], -1)
            previous = current
        else:
            return 0
    # overall time difference calculation
    delta_time = calc_diff(first, current)
    storage[i] = numpy.append(storage[i], delta_time)


def main():

    # locations of interest
    STATUSES = ['OM_CONSIGN', 'SC_INBOUND_SUCCESS', 'LH_DEPART',
                'LH_ARRIVE', 'SIGNED']
    TRAVEL_PATHS = ['om_sc', 'sc_lh', 'lh_cc', 'cc_sign', 'om_sign']
    # reference for storing arrays of time differences
    # change the structure, this is bad
    storage = [[] for x in range(len(TRAVEL_PATHS))]

    # set up connection with the mysql server
    db = MySQLdb.connect(
        user="root",
        passwd="w2a88888",
        db="delivery_status2")
    cur = db.cursor()

    # fetch all unique unique parcel tracking ids
    with open('training1.json') as data_file:
        data = json.load(data_file)

    process_ids(cur, data, STATUSES, storage)

    cur.close()
    db.close()

    count = 0
    # write arrays to dump files
    for i in TRAVEL_PATHS:
        anArray = storage[count].tolist()
        with open('%s.json' % i, 'w') as outfile:
            json.dump(anArray, outfile)
        count += 1


if __name__ == "__main__":
    main()
