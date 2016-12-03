import sys
import csv
import sqlite3

assert len(sys.argv) == 2

file_name = sys.argv[1]

conn = sqlite3.connect("/Users/austin/code/prininfo/project/db.sqlite")
cur = conn.cursor()

with open(file_name, 'rb') as f:
    reader = csv.reader(f)
    cols = next(reader)


col_names = ','.join([col[:col.index(',')] for col in cols])

try:
    cur.execute("CREATE TABLE t2004 ("+ col_names + ");")
except sqlite3.OperationalError:
    pass

with open(file_name, 'rb') as f:
    dr = csv.DictReader(f)
    to_db = []
    for i in dr:
        tup = tuple(i[col] for col in cols)
        to_db.append(tup)

for row in to_db:
    print row

qs = []
cur.executemany("INSERT INTO t2004 (" + col_names + ") VALUES (" + "?, "*(len(cols)-1) + "?);", to_db)
conn.commit()
conn.close()
