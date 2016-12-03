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
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route('/')
def index():
    get_db()
    return app.send_static_file('index.html')

@app.route('/data/singleyear')
def single_year():
    return ""
    
@app.route('/data/y2y')
def year_to_year():
    return ""

if __name__ == '__main__':
    app.run()
