from flask import request,render_template, redirect, Blueprint, url_for, flash, session
import mysql.connector 
from db import db,cursor
from werkzeug.security import generate_password_hash,check_password_hash
from functools import wraps

#Blueprint
auth=Blueprint('auth',__name__)

#register
@auth.route('/register')
def register_form():
    return render_template('auth/register.html')

@auth.route('/register',methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        #if password and confirm password wont match
        if password != confirm_password:
            flash('Password does not match','danger')
            return redirect(url_for('auth.register_form'))
        

        #check if the username already exists
        check_user_query = "SELECT username FROM user WHERE name = %s"
        cursor.execute(check_user_query, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('username already exists. Use another username','danger')
            return redirect(url_for('auth.register_form'))
 

        #hash the password before storing it in the database
        hashed_password = generate_password_hash(password, method = 'pbkdf2:sha256')

        #insert the user into database
        insert_user_query = "INSERT INTO user (username,password) VALUES (%s,%s)"
        user_data = (username,hashed_password)

        try:
            cursor.execute(insert_user_query, user_data)
            db.commit()
            flash('Registration successful. You can now login','Success')
            return redirect(url_for('auth.user_login_form'))
        except mysql.connector.Error as e:
            db.rollback()
            flash(f'The registration failed: {e}','danger')

#login
@auth.route('/userlogin')
def user_login_form():
    return render_template('auth/userlogin.html')

@auth.route('/userlogin',methods=['POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #query the database to fetch hashed password
        get_user_query = "SELECT username, password FROM user WHERE username = %s"
        cursor.execute(get_user_query,(username,))
        user_data = cursor.fetchone()
        if user_data and check_password_hash(user_data[1], password):
            #successful login Store the user data in session
            session['username'] = user_data[0]
            flash('Login successful','success')
            return redirect(url_for('auth.dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('auth/userlogin.html')

#logout
@auth.route('/logout')
def logout():
    #Clear the session to logout the user
    session.pop('username',None)
    #flash('You have been logged out','info')
    return render_template('index.html')

#login required for authentication
#the login required function
def login_required(view):
    @wraps(view)
    def wrapped_view(*args,**kwargs):
        if session.get('username'):
            #user is authenticated, execute the original view function
            return view(*args,**kwargs)
        else:
            #user is not authenticated redirect to login page
            flash('You are not logged in! login to perform action')
            return url_for('auth.login_form')
    return wrapped_view

#Dashboard

#Fetch count of tables
cursor.execute("SELECT COUNT(*) FROM reception")
count = cursor.fetchone()


#Route for dashboard
@auth.route('/dashboard')
def dashboard():
    #Check if the user is logged in
    if username in session:
        return render_template('dashboard.html',
                               count = count[0])
    else:
        return redirect(url_for('auth.login_form'))
