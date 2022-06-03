from flask import flash, render_template, current_app as app, request, redirect, url_for
from .models import User
from flask_login import login_user, logout_user
from app import db

@app.route('/user')
def user_single():
    return render_template('users/single')

@app.route('/users/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_data = request.form
        # cross referencing emails with database

        user = User.query.filter_by(email=form_data.get('email')).first()
        
        # check validity of password and email
        if user is None or not user.check_password(form_data.get('password')):
            flash('The email or password is incorrect, please try again', 'danger')
            return redirect(url_for('login'))
        
        # log in user
        login_user(user, remember=form_data.get('remember_me'))
        flash('Logged in successful', 'success')
        return redirect(url_for('home'))
        
    return render_template('users/login.html')

@app.route('/users/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = request.form

        email = User.query.filter_by(email=form_data.get('email')).first()
        if email is not None:
            flash('That email addres is already in use. Please enter a different email', 'warning')
            return redirect(url_for('register'))
    
        if form_data.get('password') == form_data.get('confirm_password'):

        # creating a new user
            user = User(
                first_name=form_data.get('first_name'),
                last_name=form_data.get('last_name'),
                email=form_data.get('email')
            )
            user.generate_password(form_data.get('password'))
            db.session.add(user)
            db.session.commit()

            # log user in after being registered
            login_user(user, remember=True)
            flash('You are now registered!', 'success')
            return redirect(url_for('home'))
        else:
            flash('You\'re passwords don\'t match, try again', 'warning')
            return redirect(url_for('register'))
    return render_template('users/register.html')

@app.route('/users/logout')
def logout():
    logout_user()
    flash('You\'ve been logged out', 'info')
    return redirect(url_for('login'))

