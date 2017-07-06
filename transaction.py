# Transaction class to model a transaction and its paths. Allows for the adding of paths and will try
# to calculate the differences in time between different statuses.

# This class operates under the assumption that information being read through is in the format
# [TID, Status, Statustime]. The fullresponse column is removed because it couldn't fit on the pi.

import datetime

class  Transaction(object):
           
    def __init__(self, tid, zipcode,pay_time):
        self.statuses = [] # format of a status [[status, statustime], [status, statustime], etc.....]
        self.tid = int(tid)
        self.zipcode = zipcode
        self.pay_time = pay_time

    # return tid of the transaction
    def get_tid(self):
        return self.tid

    def get_zipcode(self):
        return self.zipcode

    # return the total time passed for the transaction
    def get_pay_time(self):
        return self.pay_time

    # adds a new key status to the transaction
    def add(self, item):
        self.statuses.append(item)

    # return the consign time (should be the starting time)
    def consign_time(self):
        for i in self.statuses:
            if i[0] == "OM_CONSIGN":
                return i[1]
        return -1

    # return the time for the parel arriving at the Germany warehouse
    def scinbound_time(self):
        for i in self.statuses:
            if i[0] == "SC_INBOUND_SUCCESS":
                return i[1]
        return -1

    # return the time for leaving the London airport
    def lhdepart_time(self):
        for i in self.statuses:
            if i[0] == "LH_DEPART":
                return i[1]
        return -1

    # return the time for arriving at China from the London airport
    def lharrive_time(self):
        last = -1
        for i in self.statuses:
            if i[0] == "LH_ARRIVE":
                last = i[1]
        return last

    # return the time the China customs clear process began?
    def ccin_time(self):
        for i in self.statuses:
            if i[0] == "CC_HO_IN_SUCCESS":
                return i[1]
        return -1

    # return the time China customs clear process finished?
    def ccout_time(self):
        for i in self.statuses:
            if i[0] == "CC_HO_OUT_SUCCESS":
                return i[1]
        return -1

    # return the time the package was signed (should be when the transaction is over?)
    def signed_time(self):
        for i in self.statuses:
            if i[0] == "SIGNED":
                return i[1]
        return -1

    # return whether the package has reachd its final destination
    def is_finished(self):
        return self.signed_time() != -1

    #-------------------------------TIME CALCULATIONS-----------------------------------------------------------

    # calculate the total time of the transaction's journey
    def calc_time_passed(self):
        if self.is_finished():
            return (self.signed_time() - self.get_pay_time()).total_seconds()
        else:
            return (datetime.datetime.now() - self.get_pay_time()).total_seconds()

    def pay_om_time(self):
        try:
            return (self.consign_time() - self.get_pay_time()).total_seconds()
        except:
            return 'NULL'

    # return the time from starting the parcel shipment to arriving at the German warehouse
    def om_sc_time(self):
        try:
            return (self.scinbound_time() - self.consign_time()).total_seconds()
        except:
            return 'NULL'

    # return the time from the Germany warehouse to London(London airport leaving?)
    def sc_lh_time(self):
        try:
            return (self.lhdepart_time() - self.scinbound_time()).total_seconds()
        except:
            return 'NULL'

    # return the time from leaving London airpot to arriving in China
    def lh_china_time(self):
        try:
            return (self.lharrive_time() - self.lhdepart_time()).total_seconds()
        except:
            return 'NULL'

    # return the time delayed between package arriving in China and finishing customs clearance
    def china_ccclear_time(self):
        try:
            return (self.ccout_time() - self.lharrive_time()).total_seconds()
        except:
            return 'NULL'

    # return the time it took to clear China customs
    def china_customs_time(self):
        try:
            return (self.ccout_time() - self.ccin_time()).total_seconds()
        except:
            return 'NULL'

    # return the time between finishing customs clearance and being signed
    def signing_time(self):
        try:
            return (self.signed_time() - self.ccout_time()).total_seconds()
        except:
            return 'NULL'
        
    # information on the transaction with each status on a different line
    def __str__(self):
        aStr = str(self.tid) + ' ' + str(self.zipcode) +'\n'
        for i in self.statuses:
            aStr += (str(i) + '\n')
        return aStr
