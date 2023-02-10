from app import app
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignUpForm, LoginForm
from app.models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Form Submitted and Validated!')
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(email, username, password)
        check_user = User.query.filter( (User.username == username) | (User.email == email) ).all()
        if check_user:
            flash('A user with that email and/or username already exists.', 'danger')
            return redirect(url_for('signup'))
        new_user = User(email=email, username=username, password=password)
        flash(f'Thank you {new_user.username} for signing up!', 'success')
        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f"{user.username} is now logged in", "warning")
            return redirect(url_for('index'))
        else:
            flash("Incorrect username and/or password", "danger")
            return redirect(url_for('login'))
        
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "warning")
    return redirect(url_for('index'))

