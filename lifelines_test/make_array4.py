# imports
import MySQLdb
import json
import numpy


def get_status_info(tid, cursor, status_name):
    cursor.execute(
        """SELECT *
                    FROM delivery_statuses
                    WHERE TID = %s
                    AND (status = %s)
                    ORDER BY statustime DESC LIMIT 1""",
        (tid, status_name))
    row = cursor.fetchall()
    return row


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


def process_ids(cursor, ids, paths, storage):
    a = [{} for x in range(len(paths))]

    num = 0
    for tid in ids:
        tidString = str(tid[0])
        num += 1
        # print(num)
        check_times(tidString, cursor, a, paths)
    for i in range(len(paths)):
        with open('%s.json' % paths[i], 'w') as outfile:
            json.dump(a[i], outfile)


def check_times(tid, cursor, storage, paths):

    # beginning status, should be OM CONSIGN
    row = get_status_info(tid, cursor, "OM_CONSIGN")
    first = row[0]
    previous = row[0]

    row = get_status_info(tid, cursor, "SC_INBOUND_SUCCESS")
    current = row[0]
    delta_time = calc_diff(previous, current)
    path1 = storage[0]
    path1[tid] = delta_time

    # germany warehouse to leaving london airport
    try:
        row = get_status_info(tid, cursor, "SC_INBOUND_SUCCESS")
        previous = row[0]

        row = get_status_info(tid, cursor, "LH_DEPART")

        current = row[0]
        delta_time = calc_diff(previous, current)
        path2 = storage[1]
        path2[tid] = delta_time
    except BaseException:
        print(str(tid) + ': missing SC_INBOUND_SUCCESS to LH_DEPART')

    # london airport departure to arriving at china
    try:
        row = get_status_info(tid, cursor, "LH_DEPART")
        previous = row[0]

        row = get_status_info(tid, cursor, "LH_ARRIVE")
        current = row[0]
        delta_time = calc_diff(previous, current)
        path3 = storage[2]
        path3[tid] = delta_time
    except BaseException:
        print(str(tid) + ': missing LH_DEPART to LH_ARRIVE')

    # customs clearance for china
    try:
        row = get_status_info(tid, cursor, "CC_HO_IN_SUCCESS")
        previous = row[0]

        row = get_status_info(tid, cursor, "CC_HO_OUT_SUCCESS")
        current = row[0]
        delta_time = calc_diff(previous, current)
        path4 = storage[3]
        path4[tid] = delta_time
    except BaseException:
        print(str(tid) + ': missing customs clearance leg')

    # finishing customs clearance to getting signed
    try:
        row = get_status_info(tid, cursor, "CC_HO_OUT_SUCCESS")
        previous = row[0]

        row = get_status_info(tid, cursor, "SIGNED")
        current = row[0]
        delta_time = calc_diff(previous, current)
        path5 = storage[4]
        path5[tid] = delta_time
    except BaseException:
        print(str(tid) + ': missing customs clearance to signing')

    # overall time difference calculation
    delta_time = calc_diff(first, current)
    path6 = storage[5]
    path6[tid] = delta_time


def main():

    # locations of interest
    TRAVEL_PATHS = ['omconsign_scinbound', 'scinbound_lhdepart', 
                    'lhdepart_lharrive', 'ccin_ccout', 
                    'ccout_signed', 'omconsign_signed']
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
    with open('training2.json') as data_file:
        data = json.load(data_file)

    process_ids(cur, data, TRAVEL_PATHS, storage)

    cur.close()
    db.close()

    count = 0
    
    # write arrays to dump files
    for i in TRAVEL_PATHS:
        anArray = numpy.array(storage[count]).tolist()
        print anArray
        with open('%s2.json' % i, 'w') as outfile:
            json.dump(anArray,outfile)
        count+=1


if __name__ == "__main__":
    main()
