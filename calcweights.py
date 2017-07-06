import MySQLdb
import numpy
import pickle
import sys
from transaction import Transaction
#from pybrain.tools.shortcuts import buildNetwork
#from pybrain.datasets import SupervisedDataSet
#from pybrain.supervised.trainers import BackpropTrainer
#from subprocess import call

def reject_outliers(data, m=3.5):
    d = numpy.abs(data - numpy.median(data))
    mdev = numpy.median(d)
    s = d / mdev if mdev else 0.
    if isinstance(s, float):
        return data # when the median is 0, avoids division by 0
    return data[s < m]

# be very careful calling this
def update_delivery_status():
    call('mysql -u root -pw2a88888 delivery_status < reduced.sql')
    db = MySQLdb.connect(user="root",passwd="w2a88888",db="delivery_status")
    cur = db.cursor()    
    cur.execute('CREATE INDEX qktid ON delivery_status(tid)')
    cur.close()
    db.close()
    
def process(transaction, info):

    if len(info) == 0:
        return None
    # adds information to transaction
    for status in info:
        if status[0] in ['OM_CONSIGN', 'SC_INBOUND_SUCCESS','LH_DEPART',\
                            'LH_ARRIVE', 'CC_HO_IN_SUCCESS', 'CC_HO_OUT_SUCCESS', 'SIGNED']:
            transaction.add(status)
    return

def save_info(transaction, table, cur):
    if transaction.is_finished(): 
            cur.execute('''insert into %s(tid, receiver_zip, pay_consign, consign_scinbound, scinbound_lhdepart, lhdepart_lharrive, lharrive_ccout, ccout_signed, total_time, finished) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,1)ON DUPLICATE KEY UPDATE pay_consign = VALUES(pay_consign), consign_scinbound = VALUES(consign_scinbound), scinbound_lhdepart = values(scinbound_lhdepart),lhdepart_lharrive = values(lhdepart_lharrive), lharrive_ccout = values(lharrive_ccout), ccout_signed = values(ccout_signed), total_time = values(total_time),finished = values(finished);''' \
                    % (table, transaction.get_tid(), transaction.get_zipcode(), transaction.pay_om_time(),\
                    transaction.om_sc_time(), transaction.sc_lh_time(), transaction.lh_china_time(), transaction.china_ccclear_time(),\
                    transaction.signing_time(), transaction.calc_time_passed()))
    else:
            cur.execute('''insert into %s(tid, receiver_zip, pay_consign, consign_scinbound, scinbound_lhdepart, lhdepart_lharrive, lharrive_ccout, ccout_signed, total_time, finished) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,0) ON DUPLICATE KEY UPDATE pay_consign = VALUES(pay_consign), consign_scinbound = VALUES(consign_scinbound), scinbound_lhdepart = values(scinbound_lhdepart), lhdepart_lharrive = values(lhdepart_lharrive), ccout_signed = values(ccout_signed), total_time = values(total_time),finished = values(finished), lharrive_ccout = values(lharrive_ccout);''' \
                    % (table, transaction.get_tid(), transaction.get_zipcode(), transaction.pay_om_time(), \
                    transaction.om_sc_time(), transaction.sc_lh_time(), transaction.lh_china_time(), transaction.china_ccclear_time(),\
                    transaction.signing_time(), transaction.calc_time_passed()))

def update_travel_times():

        db = MySQLdb.connect(user="root",passwd="w2a88888",db="delivery_status")
        cur = db.cursor()
        TABLE = 'travel_time'
        #cur.execute('DROP TABLE IF EXISTS %s' % TABLE)
        cur.execute('CREATE TABLE IF NOT EXISTS %s(tid bigint(20) PRIMARY KEY, receiver_zip varchar(100), pay_consign int(30), consign_scinbound int(30), scinbound_lhdepart int(30), lhdepart_lharrive int(30), lharrive_ccout int(30), ccout_signed int(30), total_time int(30), finished bit(1));' % (TABLE))
        
        cur.execute('SELECT tid, receiver_zip, pay_time FROM delivery_profile ORDER BY RAND()')
        tids = cur.fetchall()
        for transaction in tids:
            #print(transaction[0])
            newTransaction = Transaction(transaction[0], transaction[1], transaction[2])
            
            cur.execute('SELECT status,statustime FROM delivery_status WHERE tid = %s ORDER BY STATUSTIME' % transaction[0])
            tid_info = cur.fetchall()
            process(newTransaction, tid_info)
            save_info(newTransaction, TABLE, cur)
            db.commit()
            
        cur.close()
        db.close()
       

def train():
        
        db = MySQLdb.connect(user="root",passwd="w2a88888",db="delivery_status")
        cur = db.cursor()
        cur.execute('SELECT total_time from travel_time where finished = 1')
        curr_performance = numpy.array(cur.fetchall())
        curr_performance = reject_outliers(curr_performance)
        median = numpy.median(curr_performance)
        threshold = 1.25 * median
        cur.execute('SELECT pay_consign, receiver_zip, total_time FROM travel_time where finished = 1')
        train = cur.fetchall()
        training_input = [d[0:-1] for d in train]
        training_output = [d[len(d)-1:len(d)] for d in train]
        # setup network (load/start a new one)
        try:
            filehandler = open('save', 'r')
            net = pickle.load(filehandler)
            filehandler.close()            
        except:
            net = buildNetwork(2,3,1)

        # create data set    
        ds = SupervisedDataSet(2,1)
        ds.setField('input', training_input)
        ds.setField('target', training_output)

        # train data
        train = BackpropTrainer(net, ds)
        for i in range(10):
            print train.train()

        # save network into file
        filehandler = open('save', 'w')
        pickle.dump(net, filehandler)
        filehandler.close()
        
        cur.close()
        db.close()

def quick_test():
        db = MySQLdb.connect(user="root",passwd="w2a88888",db="delivery_status")
        cur = db.cursor()
        cur.execute('SELECT total_time from travel_time where finished = 1')
        curr_performance = numpy.array(cur.fetchall())
        curr_performance = reject_outliers(curr_performance)
        median = numpy.median(curr_performance)
        threshold = 1.25 * median
        cur.execute('SELECT pay_consign, receiver_zip, total_time < %d FROM travel_time where finished = 1' %threshold)
        train = cur.fetchall()
        testing_input = [d[0:-1] for d in train]
        testing_output = [d[len(d)-1:len(d)] for d in train]
        try:
            filehandler = open('save', 'r')
            net = pickle.load(filehandler)
            filehandler.close()
        except:
            return
        print(len(testing_input))
        print(net.activate([-1000,400]))
        cur.close()
        db.close()
        

def main():
        # creates/updates calculations on the tables
        update_travel_times()
        #quick_test()
        #train()
main()
        
