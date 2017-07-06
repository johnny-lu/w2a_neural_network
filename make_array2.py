# imports
import MySQLdb
import json
import numpy

# locations of interest
MYLIST = ['OM_CONSIGN', 'SC_INBOUND_SUCCESS', 'LH_HO_IN_SUCCESS','LH_DEPART',\
          'LH_ARRIVE','SIGNED']
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

# reference for storing arrays of time differences
storage = [om_sc,sc_lh,lh_lh,lh_cc,cc_sign] # change the structure, this is bad

for tid in ids:
    # string tid to be used in query
    idstring = str(tid[0])

    # starting status
    cur.execute("""SELECT *
                FROM delivery_statuses
                WHERE TID = %s
                AND (status = %s)
                ORDER BY statustime LIMIT 1""",
                (idstring, MYLIST[0]))
    status_info = cur.fetchall()
    #print(status_info)
    previous = status_info[0]

    # all following statuses in the parcel movement
    for i in range(1, len(MYLIST)):
        # pull next relevant status in the shipment
        cur.execute(
            """SELECT *
                FROM delivery_statuses
                WHERE TID = %s
                AND (status = %s)
                ORDER BY statustime LIMIT 1""",
                (idstring, MYLIST[i]))
        status_info = cur.fetchall()
        #print(status_info)

        # calculate time difference in the statuses if possible
        if len(status_info) > 0:
            current = status_info[0]
            start_time = previous[2]
            end_time = current[2]
            delta_time = (end_time - start_time).total_seconds()
            storage[i-1] = numpy.append(storage[i-1],delta_time)
            previous = current            
        else:
            break
    
count  = 0
for i in TRAVELPATHS:
    #print(storage[count])
    anArray = storage[count].tolist()
    with open('%s.json' % i, 'w') as outfile:
        json.dump(anArray, outfile)
    count+=1

