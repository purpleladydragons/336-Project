import sys
import csv
import sqlite3

assert len(sys.argv) == 3

table = sys.argv[1]
file_name = sys.argv[2]

conn = sqlite3.connect("/Users/austin/code/prininfo/project/db.sqlite")
cur = conn.cursor()

with open(file_name, 'rb') as f:
    reader = csv.reader(f)
    cols = next(reader)

col_names = ','.join([col.replace(',', '').replace(' ', '_').replace('-', '_') for col in cols])

cur.execute("CREATE TABLE " + table + " ("+ col_names + ");")

with open(file_name, 'rb') as f:
    dr = csv.DictReader(f)
    to_db = []
    for i in dr:
        tup = tuple(i[col].replace(',', '') for col in cols)
        to_db.append(tup)

for row in to_db:
    print row

qs = []
cur.executemany("INSERT INTO " + table + " (" + col_names + ") VALUES (" + "?, "*(len(cols)-1) + "?);", to_db)
conn.commit()
conn.close()
