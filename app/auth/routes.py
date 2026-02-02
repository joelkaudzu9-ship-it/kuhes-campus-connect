
# app/auth/routes.py - FIXED
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import db

# Import auth_bp from the auth package
from app.auth import auth_bp

# ... rest of your auth routes code ...


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=True)

            # Store user info in session (for backward compatibility)
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.get_full_name()
            session['email'] = user.email
            session['role'] = user.role

            flash('Login successful! Welcome back.', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('auth/login.html', title='Sign In')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        faculty = request.form.get('faculty')
        program = request.form.get('program')
        year = request.form.get('year')

        # Basic validation
        errors = []

        if not all([username, email, password, confirm_password, first_name, last_name, faculty, program, year]):
            errors.append('All fields are required')

        if password != confirm_password:
            errors.append('Passwords do not match')

        if User.query.filter_by(username=username).first():
            errors.append('Username already exists')

        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')

        if errors:
            for error in errors:
                flash(error, 'danger')
        else:
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                faculty=faculty,
                program=program,
                year=year
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            # Auto login after registration
            login_user(user)

            # Store user info in session
            session['user_id'] = user.id
            session['username'] = user.username
            session['full_name'] = user.get_full_name()
            session['email'] = user.email
            session['role'] = user.role

            flash('Registration successful! Welcome to KUHES Campus Connect.', 'success')
            return redirect(url_for('main.home'))

    return render_template('auth/register.html', title='Register')


@auth_bp.route('/logout')
def logout():
    """Logout user - removed @login_required to ensure it always works"""
    # Store username for message before logging out
    username = None
    if current_user.is_authenticated:
        username = current_user.username

    # Clear Flask-Login session
    logout_user()

    # IMPORTANT: Also clear Flask's session cookie
    session.clear()

    # Optional: Force session to be deleted
    session.permanent = False

    # Create redirect response
    response = redirect(url_for('main.home'))

    # Clear the session cookie explicitly
    response.delete_cookie('session')
    response.delete_cookie('remember_token')

    # Flash message
    if username:
        flash(f'{username} has been logged out.', 'info')
    else:
        flash('You have been logged out.', 'info')

    return response