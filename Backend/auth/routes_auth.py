# auth/routes_auth.py

from flask import Blueprint, render_template, redirect, flash, url_for, request
from .forms import SignUpForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'danger')
            return redirect(url_for('auth.login'))

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()

        flash(f"Account created for {form.username.data} as {form.role.data}!", "success")
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for('auth.login'))  # Update this as needed
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('./login.html', form=form)
