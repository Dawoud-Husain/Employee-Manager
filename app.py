from flask import Flask, url_for, request, session, g
from flask.templating import render_template

from werkzeug.utils import redirect
from database import get_database

from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3

app = Flask(__name__)

#store the user into a session 
app.config['SECRET_KEY'] = os.urandom(24)

#Disconnects from the database (used for logging out)
@app.teardown_appcontext
def close_database(error):
    if hasattr(g, 'employeeapplication.db'):
        g.employeeapplicatoin_db.close()

# Gets the username from the sessoin
def get_current_user ():
    user = None 

    if 'user' in session:
        user = session['user']
        db = get_database()
        user_cur = db.execute('select * from users where name = ?', [user])
        user = user_cur.fetchone()

    return user 

#Starting Page
@app.route('/')
def index():
    user = get_current_user()
    return render_template('home.html', user = user)

#Login User By Verifying Entered Username and Password
@app.route('/login',  methods = ["POST", "GET"] )
def login():
    user = get_current_user()
    error = ""
    db  = get_database()

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        user_cursor = db.execute('select * from users where name = ?', [name])
        user = user_cursor.fetchone()

        #check if username and password matches 
        if user:
            if check_password_hash(user['password'], password):
                session['user'] = user['name']
                return redirect(url_for('dashboard'))

            else:
                error = "Username or Password did not match, try again"

        else:
            error = "Username or Password did not match, try again"

    return render_template('login.html', loginerror = error, user = user)

#Register Meathod
#Receives the entered username and password and update the database with a hashed password
@app.route('/register', methods = ["POST", "GET"])
def register():
    
    db = get_database() 
    user = get_current_user()
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        dbuser_cur = db.execute('select * from users where name = ?', [name])
        existing_username = dbuser_cur.fetchone()
        if existing_username:
            return render_template('register.html ', registererror = 'username already taken, try a differnrent username')

        db.execute('insert into users ( name, password) values (?, ?)', [name, hashed_password])
        db.commit()
     
        return redirect(url_for('index'))

    return render_template('register.html', user = user )

# Fetch and show all employees in the dashboard for the current user session 
@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    db = get_database()
   
    emp_cur = db.execute ('select * from emp')
    allemp = emp_cur.fetchall()
    return render_template('dashboard.html', user = user, allemp = allemp)

#Retreive the information from the addnewemployee page and update the database
@app.route('/addnewemployee', methods = ["POST", "GET"]) 
def addnewemployee():
    user = get_current_user()

    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        db = get_database()
        db.execute('insert into emp (name, email, phone, address) values (?,?,?,?)', [name, email, phone, address])
        db.commit()

        return redirect(url_for('dashboard'))

    return render_template('addnewemployee.html', user = user) 

#Fetches employee from database 
@app.route('/singleemployee/<int:empid>')
def singleemployee(empid):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp where empid = ?', [empid])
    single_emp = emp_cur.fetchone()


    return render_template('singleemployee.html', user = user, single_emp = single_emp) 


@app.route('/fetchone/<int:empid>')
def fetchone(empid):
    user = get_current_user()
    db = get_database()
    emp_cur = db.execute('select * from emp where empid = ?', [empid])
    single_emp = emp_cur.fetchone()
    return render_template('updateemployee.html', user = user, single_emp = single_emp)


@app.route('/updateemployee', methods = ["POST", "GET"])
def updateemployee():
    user = get_current_user()
    if request.method == 'POST':
        empid = request.form['empid']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        db = get_database()
        db.execute('update emp set name = ?, email = ?, phone = ?, address = ?, where empid = ?', [name, email, phone, address, empid])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('updateemployee.html', user = user) 

#Deletes empployee from database
@app.route('/deleteemp/<int:empid>', methods = ["GET", "POST"])
def deleteemp(empid):

    user = get_current_user()
    if request.method == 'GET':
        db = get_database()
        db.execute('delete from emp where empid = ?', [empid])
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('dashboard.html', user = user)
    
#Logs out of user session
@app.route('/logout')
def logout():
    session.pop('user', None)
    render_template('home.html')

#Run App
if __name__ == '__main__':
    app.run(debug=True) 

