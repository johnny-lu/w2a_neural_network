# -*- coding: utf-8 -*-

import MySQLdb
import numpy
import time
import sys
from transaction import Transaction
from subprocess import call
import os

def xstr(s):
    if s is None:
        return ''
    else:
        return s

def create_csv():

    os.system("""mysql -u root -pw2a88888 test620 -e "select * from status_time" -B | sed "s/'/\\'/;s/\\t/\\",\\"/g;s/^/\\"/;s/$/\\"/;s/\\n//g" > time_stamps.csv""")

def process(transaction,info):

    if len(info) == 0:
        return None
    # adds information to transaction
    for status in info:
        if status[0] in ['OM_CONSIGN','SC_INBOUND_SUCCESS','LH_DEPART',\
                            'LH_ARRIVE','CC_HO_IN_SUCCESS','CC_HO_OUT_SUCCESS','SIGNED']:
            transaction.add(status)
    return

def save_info(transaction,table,cur):

    command = '''insert into %s(tid,pay,consign, scinbound, lhdepart, lharrive, ccout, signed) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)ON DUPLICATE KEY UPDATE pay = VALUES(pay), consign = VALUES(consign), scinbound = VALUES(scinbound), lhdepart = VALUES(lhdepart), lharrive = VALUES(lharrive), ccout = VALUES(ccout), signed = VALUES(signed);''' % (table,transaction.get_tid(),"\'" + str(transaction.pay_time) + "\'", "\'" + str(transaction.consign_time()) + "\'", "\'" + str(transaction.scinbound_time()) + "\'", "\'" + str(transaction.lhdepart_time()) + "\'", "\'" + str(transaction.lharrive_time()) + "\'", "\'" + str(transaction.ccout_time()) + "\'", "\'" + str(transaction.signed_time()) + "\'")
    
    #print command
    cur.execute(command)

    
def update_travel_times():

    db = MySQLdb.connect(user="root",passwd="w2a88888",db="test620",charset = 'utf8')
    cur = db.cursor()
    TABLE = 'status_time'


    cur.execute('CREATE TABLE IF NOT EXISTS %s(tid bigint(20) PRIMARY KEY, pay TIMESTAMP, consign TIMESTAMP, scinbound TIMESTAMP, lhdepart TIMESTAMP, lharrive TIMESTAMP, ccout TIMESTAMP, signed TIMESTAMP) CHARACTER SET = utf8;' % (TABLE))
    
    cur.execute('SELECT * FROM delivery_profile')
    tids = cur.fetchall()
    for transaction in tids:
        print(transaction[0])
        newTransaction = Transaction(transaction[0],transaction[2].encode('utf8'),transaction[3].encode('utf8'),transaction[4].encode('utf8'),transaction[5].encode('utf8'),transaction[6],transaction[7])
        
        cur.execute('SELECT status,statustime FROM delivery_status WHERE tid = %s ORDER BY STATUSTIME' % transaction[0])
        tid_info = cur.fetchall()
        #if newTransaction.is_finished():
        process(newTransaction,tid_info)
        save_info(newTransaction,TABLE,cur)
        
        

    db.commit()
    cur.close()
    db.close()

    create_csv()

def main():
        
        update_travel_times()

main()
        
