import MySQLdb

db = MySQLdb.connect(
        user="root",
        passwd="w2a88888",
        db="delivery_status2")
cur = db.cursor()
# Retrieve data and randomly split into a training and test set (total number of values used indicated by LIMIT)
# A late parcel shipment is defined as total time being greater than or equal to the average total shipment time
# X-values include the all columns selected before the late column, Y-value (1 or 0) defines late given above condition
cur.execute('select consign_scinbound/30000, scinbound_lhdepart/30000, lhdepart_lharrive/30000, lharrive_ccout/30000,(select avg(total_time) from time_diff)-total_time > 0 as slow from time_diff where consign_scinbound + scinbound_lhdepart + lhdepart_lharrive + lharrive_ccout + ccout_signed - total_time = 0 ORDER BY RAND() LIMIT 15000;')
dataset = cur.fetchall()
# training set is marked off at certain point (convert to ratio later)
training_set = dataset[:10000]
# test set; picks up on where data was split to training point until end
test_set = dataset[-10000:]

parcelTrainingData = open('datasets/parcel-training.txt', 'w')

for row in training_set:
    row = ','.join(map(str, row))
    parcelTrainingData.write(row+"\n")
parcelTrainingData.close()

parcelTestData = open('datasets/parcel-test.txt', 'w')

for row in test_set:
    row = ','.join(map(str, row))
    parcelTestData.write(row+"\n")
parcelTestData.close()
