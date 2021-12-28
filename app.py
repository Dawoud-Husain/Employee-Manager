from flask import Flask, url_for, request, redirect
from flask.templating import render_template
from database import get_database

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

#Starting Page
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

#Register Meathod
#Gets the username and password and update the database with the hashed password

@app.route('/register', methods = ["POST", "GET"])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        db = get_database() 
        db.execute('insert into users ( name, password) values (?, ?)', [name, hashed_password])
        db.commit()

        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
     return render_template('dashboard.html')

@app.route('/addnewemployee')
def addnewemployee():
     return render_template('addnewemployee.html') 

@app.route('/singleemployee')
def singleemployeeprofile():
     return render_template('singleemployee.html') 

@app.route('/update')
def update():
     return render_template('update.html') 

def logout():
    return render_template('home.html')

#Run App
if __name__ == '__main__':
    app.run(debug=True) 

