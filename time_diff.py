# This programs loops through the existing database and calculates differences between key statuses. The output
# is stored inside another table called time_diff that holds information on time differences between key statuses
# for different transactions, identified by tid.

import MySQLdb
import transaction
import json
import time

def main():
    # set up connection with the mysql server
    db = MySQLdb.connect(
            user="root",
             passwd="w2a88888",
             db="delivery_status2")
    cur = db.cursor()
    counter = 0
    cur.execute('CREATE TABLE IF NOT EXISTS time_diff(tid VARCHAR(30) PRIMARY KEY, consign_scinbound int(30), scinbound_lhdepart int(30), lhdepart_lharrive int(30), lharrive_ccout int(30), ccout_signed int(30), ccin_ccout int(30), total_time int(30), finished bit(1));')
    db.commit()
    while True:
        # all unique ids within a data dump
        cur.execute('select distinct tid from delivery_statuses')
        ids = cur.fetchall()

        for tid in ids:
            tempid = (str(tid[0]))
            cur.execute('''select * from delivery_statuses where tid = %s ORDER BY statustime''' % tempid)
            row = cur.fetchall()
            newTransaction = transaction.Transaction(tempid)
            count = 0
            for x in row:
                if x[1] in ['OM_CONSIGN', 'SC_INBOUND_SUCCESS','LH_DEPART',\
                            'LH_ARRIVE', 'CC_HO_IN_SUCCESS', 'CC_HO_OUT_SUCCESS', 'SIGNED']:
                    newTransaction.add(x)
                    count += 1
            newTransaction.calc_time_passed()
            if count > 7:
                print(count)
            else:
                print((newTransaction.tid))
                # tries to insert new information on a distinct tid that has not been logged yet
                try:
                    if newTransaction.is_finished():
                        cur.execute('''insert into time_diff(tid, consign_scinbound, scinbound_lhdepart, lhdepart_lharrive, ccin_ccout,
                                    ccout_signed, total_time, finished, lharrive_ccout) VALUES(%d,%d,%d,%d,%d,%d,%d,1, %d)
                                    ON DUPLICATE KEY UPDATE consign_scinbound = VALUES(consign_scinbound), scinbound_lhdepart = values(scinbound_lhdepart),
                                    lhdepart_lharrive = values(lhdepart_lharrive), ccin_ccout = values(ccin_ccout), ccout_signed = values(ccout_signed), total_time = values(total_time),
                                    finished = values(finished), lharrive_ccout = values(lharrive_ccout);'''
                                    % (newTransaction.tid, newTransaction.om_sc_time(), newTransaction.sc_lh_time(),\
                                       newTransaction.lh_china_time(), newTransaction.china_customs_time(), newTransaction.signing_time(), \
                                       newTransaction.get_time_passed(), newTransaction.china_ccclear_time()))
                    else:
                        cur.execute('''insert into time_diff(tid, consign_scinbound, scinbound_lhdepart, lhdepart_lharrive, ccin_ccout,
                                    ccout_signed, total_time, finished, lharrive_ccout) VALUES(%d,%d,%d,%d,%d,%d,%d,0, %d)
                                    ON DUPLICATE KEY UPDATE consign_scinbound = VALUES(consign_scinbound), scinbound_lhdepart = values(scinbound_lhdepart),
                                    lhdepart_lharrive = values(lhdepart_lharrive), ccin_ccout = values(ccin_ccout), ccout_signed = values(ccout_signed), total_time = values(total_time),
                                    finished = values(finished), lharrive_ccout = values(lharrive_ccout);'''
                                    % (newTransaction.tid, newTransaction.om_sc_time(), newTransaction.sc_lh_time(),\
                                       newTransaction.lh_china_time(), newTransaction.china_customs_time(), newTransaction.signing_time(), \
                                       newTransaction.get_time_passed(), newTransaction.china_ccclear_time()))
                except:
                    pass
                db.commit()
                """
                    if newTransaction.is_finished():
                        cur.execute('''update time_diff set consign_scinbound = %d, scinbound_lhdepart = %d, lhdepart_lharrive = %d,
                                            ccin_ccout = %d, lharrive_ccout = %d, ccout_signed = %d, total_time = %d, finished = 1  where tid = %d''' \
                                        %(newTransaction.om_sc_time(), newTransaction.sc_lh_time(),\
                                       newTransaction.lh_china_time(), newTransaction.china_customs_time(), newTransaction.china_ccclear_time(), newTransaction.signing_time(), \
                                       newTransaction.get_time_passed(), newTransaction.tid))
                    else:
                        cur.execute('''update time_diff set consign_scinbound = %d, scinbound_lhdepart = %d, lhdepart_lharrive = %d, ccin_ccout = %d,
                                            lharrive_ccout = %d, ccout_signed = %d, total_time = %d,  finished = 0  where tid = %d''' \
                                        %(newTransaction.om_sc_time(), newTransaction.sc_lh_time(),\
                                       newTransaction.lh_china_time(), newTransaction.china_customs_time(), newTransaction.china_ccclear_time(), newTransaction.signing_time(), \
                                       newTransaction.get_time_passed(), newTransaction.tid))
                    """
                
            counter += 1
        print(counter)
        cur.close()
        db.close()
        time.sleep(360)
        db = MySQLdb.connect(
            user="root",
                 passwd="w2a88888",
             db="delivery_status2")
        cur = db.cursor()     
        
if __name__ == '__main__':
    main()
