from flask import Blueprint, render_template, request, redirect, session, flash
from models.user import register_user, login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return redirect('/login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email    = request.form['email']
        password = request.form['password']
        success  = register_user(username, email, password)
        if success:
            flash('Account created! Please login.', 'success')
            return redirect('/login')
        else:
            flash('Email already exists. Try another.', 'danger')
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        user     = login_user(email, password)
        if user:
            session['user_id']  = user['id']
            session['username'] = user['username']
            return redirect('/dashboard')
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')