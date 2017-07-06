import json
import numpy as np

def checkLate(mydict, val):
    myArray = np.array(mydict.values())
    median = np.median(myArray)
    stdev = np.std(myArray)
    cutoff = median + stdev
    return val > cutoff


def main():

    with open('omconsign_signed.json') as data_file:
        mydict = json.load(data_file)
        assert isinstance(mydict, dict)
    data_file.close()

    allTimesArray = np.array(mydict.values())

    median = np.median(allTimesArray)
    stdev = np.std(allTimesArray)
    cutoff = median + stdev

    lateKeys = []

    for key, value in mydict.iteritems():
        if value > cutoff:
            lateKeys.append(int(key))

    print 'Total late parcels:  ', len(lateKeys)
    #lateKeys = np.random.choice(lateKeys, 400, replace=False)

    # will this be necessary?
    log = open("late_parcel_tids", "w")
    for tid in lateKeys:    
        log.write(str(tid)+'\n')
    log.close()

    with open('ccin_ccout.json') as ccin_ccout_file:
            ccin_ccout_mydict = json.load(ccin_ccout_file)
    ccin_ccout_file.close()
    with open('ccout_signed.json') as ccout_signed_file:
            ccout_signed_mydict = json.load(ccout_signed_file)
    ccout_signed_file.close()
    with open('lhdepart_lharrive.json') as lhdepart_lharrive_file:
            lhdepart_lharrive_mydict = json.load(lhdepart_lharrive_file)
    lhdepart_lharrive_file.close()
    with open('omconsign_scinbound.json') as omconsign_scinbound_file:
            omconsign_scinbound_mydict = json.load(omconsign_scinbound_file)
    omconsign_scinbound_file.close()
    with open('scinbound_lhdepart.json') as scinbound_lhdepart_file:
            scinbound_lhdepart_mydict = json.load(scinbound_lhdepart_file)
    scinbound_lhdepart_file.close()

    ccin_ccout_count = 0
    ccout_signed_count = 0
    lhdepart_lharrive_count = 0
    omconsign_scinbound_count = 0
    scinbound_lhdepart_count = 0

    counter = 1
    for tid in lateKeys:
        print counter
        for key in ccin_ccout_mydict:
            if int(key) == int(tid):
                if checkLate(ccin_ccout_mydict, ccin_ccout_mydict[key]):
                    print 'route:   ccin_ccout; tid:    ', key
                    ccin_ccout_count = ccin_ccout_count + 1

        for key in ccout_signed_mydict:
            if int(key) == int(tid):
                if checkLate(ccout_signed_mydict, ccout_signed_mydict[key]):
                    print 'route:   ccout_signed; tid:    ', key
                    ccout_signed_count = ccout_signed_count + 1

        for key in lhdepart_lharrive_mydict:
            if int(key) == int(tid):
                if checkLate(lhdepart_lharrive_mydict, lhdepart_lharrive_mydict[key]):
                    print 'route:   lhdepart_lharrive; tid:    ', key
                    lhdepart_lharrive_count = lhdepart_lharrive_count + 1


        for key in omconsign_scinbound_mydict:
            if int(key) == int(tid):
                if checkLate(omconsign_scinbound_mydict, omconsign_scinbound_mydict[key]):
                    print 'route:   omconsign_scinbound; tid:    ', key
                    omconsign_scinbound_count = omconsign_scinbound_count + 1


        for key in scinbound_lhdepart_mydict:
            if int(key) == int(tid):
                if checkLate(scinbound_lhdepart_mydict, scinbound_lhdepart_mydict[key]):
                    print 'route:   scinbound_lhdepart; tid:    ', key
                    scinbound_lhdepart_count = scinbound_lhdepart_count + 1


        counter = counter + 1

    print 'ccin_ccout:  ', ccin_ccout_count
    print 'ccout_signed:  ', ccout_signed_count
    print 'lhdepart_lharrive:  ', lhdepart_lharrive_count
    print 'omconsign_scinbound:  ', omconsign_scinbound_count
    print 'scinbound_lhdepart:  ', scinbound_lhdepart_count


if __name__ == "__main__":
    main()

