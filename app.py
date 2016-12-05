import sqlite3
from flask import Flask, jsonify, g, request

DATABASE = 'db.sqlite'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    print query, args
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/data/singleyear')
def single_year():
    cur = get_db().cursor()
    year = int(request.args.get("year"))
    county_filter = request.args.get("counties")
    # TODO income filter

    result = execute_query(
        """SELECT fips, ?
            FROM  
        
        """
    )

    str_rows = [','.join(map(str, row)) for row in result]
    cur.close()
    header = 'fips,difference\n'
    return header + '\n'.join(str_rows)

@app.route('/data/y2y')
def year_to_year():
    cur = get_db().cursor()

    # TODO join voting and finance into one table so that vX and fX are conjoined together and so are vY and fY. 

    start_year = request.args.get("startYear")
    end_year = request.args.get("endYear")
    attr = request.args.get("attr")

    result = execute_query("""SELECT DISTINCT t1.FIPS, t1.COUNTY, t1.STATE, t2.{} - t1.{} as difference
        FROM (v{} JOIN f{} on v{}.FIPS = f{}.FIPS) as t1
            JOIN 
                (v{} JOIN f{} on v{}.FIPS = f{}.FIPS) as t2 on t1.FIPS = t2.FIPS; 
    """.format(attr, attr, 
                start_year, start_year, start_year, start_year,
                end_year, end_year, end_year, end_year)
    )
                
    str_rows = []
    for row in result:
        row = list(map(str,row))
        for i,t in enumerate(row):
            row[i] = t.replace(',', ' ')
        print row
        str_rows.append(','.join(row))

    cur.close()
    header = 'fips,county,state,difference\n'
    return header + '\n'.join(str_rows)

if __name__ == '__main__':
    app.run(debug=True)
