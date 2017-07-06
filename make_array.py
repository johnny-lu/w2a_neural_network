# imports
import MySQLdb
import json
import numpy

# locations of interest
MYLIST = ['OM_CONSIGN', 'SC_SIGN_IN_SUCCESS', 'LH_HO_IN_SUCCESS','LH_DEPART',\
          'LH_ARRIVE','CC_HO_IN_SUCCESS', 'CC_HO_OUT_SUCCESS', 'SIGNED']
TRAVELPATHS = ['om_sc', 'sc_lh', 'lh_lh', 'lh_cc', 'cc_sign']

# set up connection with the mysql server
db = MySQLdb.connect(
    user="root",
     passwd="powerpoint",
     db="delivery_status")
cur = db.cursor()

# fetch all unique unique parcel tracking ids
cur.execute("""SELECT DISTINCT tid FROM delivery_statuses""")
ids = cur.fetchall()

# path time arrays
om_sc = numpy.array([])  # start order to germany warehouse
sc_lh = numpy.array([])  # germany warehouse to london airport
lh_lh = numpy.array([])  # london to china flight
lh_cc = numpy.array([])  # china customs clearance
cc_sign = numpy.array([])  # china delivery

for tid in ids:
    # string tid to be used in query
    idstring = str(tid[0])
    
    '''
    # pull rows in respect to t ransactions
    cur.execute("""SELECT *
                            FROM delivery_statuses
                            WHERE TID = %s
                            AND (status IN %s)
                            ORDER BY statustime""",
                            (idstring, MYLIST))
    transactions = cur.fetchall()
    '''
    cur.execute("""SELECT *
                FROM delivery_statuses
                WHERE TID = %s
                AND (status = %s)
                ORDER BY statustime LIMIT 1""",
                (idstring, MYLIST[0]))
    status_info = cur.fetchall()
    previous = status_info[0]
    for i in range(1, len(TRAVELPATHS) + 1):
        cur.execute(
            """SELECT *
                FROM delivery_statuses
                WHERE TID = %s
                AND (status = %s)
                ORDER BY statustime LIMIT 1""",
                (idstring, MYLIST[i]))
        status_info = cur.fetchall()
        print(status_info)
        current = status_info[0]
        if current != None:        
            start_time = previous[2]
            end_time = current[2]
            delta_time = (end_time - start_time).total_seconds()
            print(delta_time)
            input()
            previous = current
        else:
            print('hello')

    break
    '''
    # start order to germany warehouse
    if len(transactions) > 1:
            start_time = transactions[0][2]
            end_time = transactions[1][2]
            delta_time = (end_time - start_time).total_seconds()
            om_sc = numpy.append(om_sc, delta_time)
    # germany warehouse to london airport
    if len(transactions) > 2:
            start_time = transactions[1][2]
            end_time = transactions[2][2]
            delta_time = (end_time - start_time).total_seconds()
            sc_lh = numpy.append(sc_lh, delta_time)
    # london to china flight
    if len(transactions) > 3:
            start_time = transactions[2][2]
            end_time = transactions[3][2]
            delta_time = (end_time - start_time).total_seconds()
            lh_lh = numpy.append(lh_lh, delta_time)
    # china customs clearance
    if len(transactions) > 4:
            start_time = transactions[3][2]
            end_time = transactions[4][2]
            delta_time = (end_time - start_time).total_seconds()
            lh_cc = numpy.append(lh_cc, delta_time)
    # china delivery
    if len(transactions) > 5:
            start_time = transactions[4][2]
            end_time = transactions[5][2]
            delta_time = (end_time - start_time).total_seconds()
            cc_sign = numpy.append(cc_sign, delta_time)


    if len(transactions) == 2:
        print('Files: ' + str(count))
        count+=1
        end_time = transactions[1][2]
        delta_time = (end_time - start_time).total_seconds()
        my_arr = numpy.append(my_arr, delta_time)
        #my_arr.append(delta_time)
    '''

'''
om_sc = om_sc.tolist()
sc_lh = sc_lh.tolist()
lh_lh = lh_lh.tolist()
lh_cc = lh_cc.tolist()
cc_sign = cc_sign.tolist()
for i in TRAVELPATHS:
    with open('%s.json' % i, 'w') as outfile:
        json.dump(eval(i), outfile)
'''
