import json
import MySQLdb

def find_tids(cursor):
    cursor.execute("""SELECT DISTINCT tid FROM delivery_statuses
                            WHERE  status = "SIGNED" ORDER BY RAND();""")
    ids = cursor.fetchall()
    return ids[:15000], ids[15000:45000], ids[45000:]

db = MySQLdb.connect(
        user="root",
         passwd="w2a88888",
         db="delivery_status2")
cur = db.cursor()
training1, training2, test = find_tids(cur)
with open('training1.json', 'w') as outfile:
            json.dump(training1, outfile)
with open('training2.json', 'w') as outfile:
            json.dump(training2, outfile)
with open('test.json', 'w') as outfile:
            json.dump(test, outfile)
