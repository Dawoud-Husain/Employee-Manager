from flask import Flask, url_for, request, redirect, session, g
from flask.templating import render_template
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

@app.route('/login',  methods = ["POST", "GET"] )
def login():
    user = get_current_user()
    error = ""
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        db  = get_database()

        
        user_cursor = db.execute('select * from users where name = ?', [name])
        user = user_cursor.fetchone()

        #check if username and password matches 
        if user:
            if check_password_hash(user['password'], password):
                session['user'] = user['name']
                return redirect(url_for('dashboard'))

            else:
                error = "Password did not match"

        else:
            error = "Username did not match"

    return render_template('login.html', loginerror = error, user = user)

#Register Meathod
#Gets the username and password and update the database with the hashed password

@app.route('/register', methods = ["POST", "GET"])
def register():
    
    user = get_current_user()
    if request.method == 'POST':
        db = get_database() 
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

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    return render_template('dashboard.html', user = user)

@app.route('/addnewemployee') 
def addnewemployee():
    user = get_current_user()
    return render_template('addnewemployee.html', user = user) 

@app.route('/singleemployee')
def singleemployeeprofile():
    user = get_current_user()
    return render_template('singleemployee.html', user = user) 

@app.route('/update')
def update():
    user = get_current_user()
    return render_template('update.html', user = user) 

#Logs out of user session

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template('home.html')

#Run App
if __name__ == '__main__':
    app.run(debug=True) 

