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
    os.system("""mysql -u root -pw2a88888 delivery_status -e "select travel_time.tid,receiver_district, receiver_state, receiver_city, receiver_town,receiver_zip,pay_consign,consign_scinbound,scinbound_lhdepart,lhdepart_lharrive,lharrive_ccout,ccout_signed,pay_consign + consign_scinbound AS pay_scinbound,pay_consign + consign_scinbound + scinbound_lhdepart AS pay_lhdepart,pay_consign + consign_scinbound + scinbound_lhdepart + lhdepart_lharrive AS pay_lharrive,pay_consign + consign_scinbound + scinbound_lhdepart + lhdepart_lharrive + lharrive_ccout AS pay_ccout,total_time from travel_time left outer join past_finished ON(travel_time.tid = past_finished.tid) where past_finished.tid IS NULL and consign_scinbound > 0 and scinbound_lhdepart > 0 and lhdepart_lharrive > 0 and lharrive_ccout > 0 and ccout_signed > 0 and finished = 1;" -B | sed "s/'/\\'/;s/\\t/\\",\\"/g;s/^/\\"/;s/$/\\"/;s/\\n//g" > finished_transactions.csv""")
    os.system("""mysql -u root -pw2a88888 delivery_status -e "select travel_time.tid,receiver_district, receiver_state, receiver_city, receiver_town,receiver_zip,pay_consign,consign_scinbound,scinbound_lhdepart,lhdepart_lharrive,lharrive_ccout,ccout_signed,pay_consign + consign_scinbound AS pay_scinbound,pay_consign + consign_scinbound + scinbound_lhdepart AS pay_lhdepart,pay_consign + consign_scinbound + scinbound_lhdepart + lhdepart_lharrive AS pay_lharrive,pay_consign + consign_scinbound + scinbound_lhdepart + lhdepart_lharrive + lharrive_ccout AS pay_ccout,total_time from travel_time where finished = 0;" -B | sed "s/'/\\'/;s/\\t/\\",\\"/g;s/^/\\"/;s/$/\\"/;s/\\n//g" > unfinished_transactions.csv""")

def update_delivery_status():
##  THIS COMMAND REMOVES THE DROP COMMAND NORMALLY IN A SQL DUMP FILE
#sed -i '/DROP TABLE IF EXISTS `delivery_status`;/d' delivery_status_2017-06-20.sql

## THESE TWO LINES CREATE A CSV FROM A DATABASE CALLED TRAVEL_TIME WITH TIME DIFFERENCES
#mysql -u root -pw2a88888 delivery_status -e "select * from travel_time where" -B | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > atest.csv

#mysql -u root -pw2a88888 delivery_status -e "select tid,receiver_zip,pay_consign,consign_scinbound,scinbound_lhdepart,lhdepart_lharrive,lharrive_ccout,ccout_signed,pay_consign + consign_scinbound AS pay_scinbound,pay_consign + consign_scinbound + scinbound_lhdepart AS pay_lhdepart,pay_consign + consign_scinbound + scinbound_lhdepart + lhdepart_lharrive AS pay_lharrive,pay_consign + consign_scinbound + scinbound_lhdepart + lhdepart_lharrive + lharrive_ccout AS pay_ccout,total_time from travel_time where consign_scinbound > 0 and scinbound_lhdepart > 0 and lhdepart_lharrive > 0 and lharrive_ccout > 0 and ccout_signed > 0 and finished = 1;" -B | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > atest6.csv

# mysql -u root -pw2a88888 delivery_status -e "select travel_time.tid,receiver_district, receiver_state, receiver_city, receiver_town,receiver_zip,pay_consign,consign_scinbound,scinbound_lhdepart,lhdepart_lharrive,lharrive_ccout,ccout_signed,pay_consign + consign_scinbound AS pay_scinbound,pay_consign + consign_scinbound + scinbound_lhdepart AS pay_lhdepart,pay_consign + consign_scinbound + scinbound_lhdepart + lhdepart_lharrive AS pay_lharrive,pay_consign + consign_scinbound + scinbound_lhdepart + lhdepart_lharrive + lharrive_ccout AS pay_ccout,total_time from travel_time left outer join past_finished ON(travel_time.tid = past_finished.tid) where past_finished.tid IS NULL and consign_scinbound > 0 and scinbound_lhdepart > 0 and lhdepart_lharrive > 0 and lharrive_ccout > 0 and ccout_signed > 0 and finished = 1;" -B | sed "s/'/\'/;s/\t/\",\"/g;s/^/\"/;s/$/\"/;s/\n//g" > finished_transactions.csv

    os.system('cd $HOME/Desktop')
    os.system("sed '25,31d' jstdb-delivery_status-29-Jun-20172.sql > reduced_status.sql")
    os.system("sed '25,35d' jstdb-delivery_profile-29-Jun-2017.sql > reduced_profile.sql")
    os.system("sed -i '/DROP TABLE IF EXISTS `delivery_status`;/d' reduced_status.sql")
    os.system("sed -i '/DROP TABLE IF EXISTS `delivery_profile`;/d' reduced_profile.sql")
    #os.system('mysql -u root -pw2a88888 --force delivery_status < jstdb-delivery_status-29-Jun-2017.sql')
    #os.system('mysql -u root -pw2a88888 --force delivery_status < jstdb-delivery_profile-29-Jun-2017.sql')
  
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

    if transaction.is_finished(): 

            cur.execute('''insert into %s(tid,receiver_district,receiver_state,receiver_city,receiver_town,receiver_zip,pay_consign,consign_scinbound,scinbound_lhdepart,lhdepart_lharrive,lharrive_ccout,ccout_signed,total_time,finished) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,1)ON DUPLICATE KEY UPDATE pay_consign = VALUES(pay_consign),consign_scinbound = VALUES(consign_scinbound),scinbound_lhdepart = values(scinbound_lhdepart),lhdepart_lharrive = values(lhdepart_lharrive),lharrive_ccout = values(lharrive_ccout),ccout_signed = values(ccout_signed),total_time = values(total_time),finished = values(finished);''' % (table,transaction.get_tid(),"\'" + transaction.district.decode('utf8') + "\'","\'" + transaction.state.decode('utf8') +"\'","\'" + transaction.city.decode('utf8') + "\'","\'"+ transaction.town.decode('utf8') + "\'","\'" + transaction.get_zipcode() + "\'",transaction.pay_om_time(),transaction.om_sc_time(),transaction.sc_lh_time(),transaction.lh_china_time(),transaction.china_ccclear_time(),transaction.signing_time(),transaction.total_time()))
    else:
            cur.execute('''insert into %s(tid,receiver_district,receiver_state,receiver_city,receiver_town,receiver_zip,pay_consign,consign_scinbound,scinbound_lhdepart,lhdepart_lharrive,lharrive_ccout,ccout_signed,total_time,finished) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,0) ON DUPLICATE KEY UPDATE pay_consign = VALUES(pay_consign),consign_scinbound = VALUES(consign_scinbound),scinbound_lhdepart = values(scinbound_lhdepart),lhdepart_lharrive = values(lhdepart_lharrive),ccout_signed = values(ccout_signed),total_time = values(total_time),finished = values(finished),lharrive_ccout = values(lharrive_ccout);''' % (table,transaction.get_tid(),"\'" + transaction.district.decode('utf8') + "\'","\'" + transaction.state.decode('utf8') + "\'", "\'" + transaction.city.decode('utf8') + "\'","\'"+ transaction.town.decode('utf8') + "\'","\'" + transaction.get_zipcode() + "\'",transaction.pay_om_time(),transaction.om_sc_time(),transaction.sc_lh_time(),transaction.lh_china_time(),transaction.china_ccclear_time(),transaction.signing_time(),transaction.total_time()))
    
def update_travel_times():

        db = MySQLdb.connect(user="root",passwd="w2a88888",db="test620",charset = 'utf8')
        cur = db.cursor()
        TABLE = 'travel_time'
        #cur.execute('DROP TABLE IF EXISTS %s' % TABLE)
        cur.execute('DROP TABLE IF EXISTS past_finished')
        cur.execute('CREATE TABLE past_finished AS SELECT tid from travel_time where finished = 1')
        cur.execute('CREATE UNIQUE INDEX idx on past_finished(tid)')
        cur.execute('CREATE TABLE IF NOT EXISTS %s(tid bigint(20) PRIMARY KEY,receiver_district varchar(100),receiver_state varchar(100),receiver_city varchar(100),receiver_town varchar(100),receiver_zip varchar(100),pay_consign int(30),consign_scinbound int(30),scinbound_lhdepart int(30),lhdepart_lharrive int(30),lharrive_ccout int(30),ccout_signed int(30),total_time int(30),finished bit(1)) CHARACTER SET = utf8;' % (TABLE))
        
        cur.execute('SELECT * FROM delivery_profile ORDER BY RAND()')
        tids = cur.fetchall()
        for transaction in tids:
            print(transaction[0])
            newTransaction = Transaction(transaction[0],transaction[2].encode('utf8'),transaction[3].encode('utf8'),transaction[4].encode('utf8'),transaction[5].encode('utf8'),transaction[6],transaction[7])
            
            cur.execute('SELECT status,statustime FROM delivery_status WHERE tid = %s ORDER BY STATUSTIME' % transaction[0])
            tid_info = cur.fetchall()
            #if newTransaction.is_finished():
            process(newTransaction,tid_info)
            print(newTransaction.state)
            save_info(newTransaction,TABLE,cur)
            

        db.commit()
        cur.close()
        db.close()

        create_csv()

def main():
        update_delivery_status()
        update_travel_times()

main()
        
