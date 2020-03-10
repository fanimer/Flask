from flask import *
import os
import random
import pymysql

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if select_db('SELECT password FROM userinfo where username=%s',
                     [request.form.get('username')])['password'][0] == request.form.get('password'):
            response = make_response(redirect(url_for('key', name=request.form['username'])))
            response.set_cookie('user', request.form['username'], max_age=60)
            return response
        else:
            error = 'Invalid username/password'
            flash(error)
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    error = None
    if request.method == 'POST':
        if insert_db('insert into userinfo(username, password) value (%s, %s) '
                     'where not exist (select username form userinfo where username=%s)',
                     [request.form.get('username'), request.form.get('password'), request.form.get('username')]):
            response = make_response(redirect(url_for('key', name=request.form['username'])))
            response.set_cookie('user', request.form['username'], max_age=60)
            return response
        else:
            error = 'Sign Up Fails, Please try again'
            flash(error)
    return render_template('sign_up.html')


@app.route('/key/', methods=['GET'])
@app.route('/key/<name>', methods=['GET'])
def key(name=None):
    if(request.method == 'GET'):
        name = request.cookies.get('user')
        if name is None:
            return redirect(url_for('login'))
    return render_template("key.html", name=name)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = pymysql.connect\
            (host='localhost', user='root', password='123456', db='account')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def select_db(select_sql, args=()):
    cur = get_db().cursor()
    cur.execute(select_sql, args)
    rv = cur.fetchall()
    cur.close()
    return dict((cur.description[idx][0], value)
                for idx, value in enumerate(rv))

def insert_db(insert_sql, args=()):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(insert_sql, args)
        db.commit()
        return True
    except:
        db.rollback()
        return False


if __name__ == '__main__':
    app.run()
