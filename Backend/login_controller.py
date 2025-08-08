from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from model import db, AllUsers,Hospital,VaccinationRecord


main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template("home/home.html")

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('pwda', '').strip()
        email = request.form.get('email', '').strip()
     
        import re
        errors = []

        if not re.match(r'^[a-zA-Z0-9_.]+$', user_id):
            errors.append("Username should not contain special characters.")
        if AllUsers.query.filter_by(user_id=user_id).first():
            errors.append("Username already exists!")
        if AllUsers.query.filter_by(email=email).first():
            errors.append("An account with this email already exists!")
        if '@' not in email:
            errors.append("Invalid email address! '@' is missing.")
        if password != confirm_password:
            errors.append("Passwords do not match!")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")

        if errors:
            for err in errors:
                flash(err, 'error')
            return render_template("home/register.html", form=request.form)  

        new_user = AllUsers(
            email=email,
            user_id=user_id,
            password=generate_password_hash(password),
            role="user"
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('main.dashboard', username=new_user.username, role=new_user.role))

    return render_template("home/register.html", form={}) 

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['username']
        password_input = request.form['password']

        user = AllUsers.query.filter_by(user_id=user_id).first()
        email= AllUsers.query.filter_by(email=user_id).first()
        print(user, email)
        if user and check_password_hash(user.password, password_input):
            login_user(user)
            return redirect(url_for('main.dashboard',username=user.user_id,role=user.role))
        elif email and check_password_hash(email.password, password_input):
            login_user(email)
            return redirect(url_for('main.dashboard',username=email.user_id,role=email.role))
        else:
            flash("User does not exists.")
            return redirect(url_for('main.login'))
    return render_template('home/login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/dashboard/<role>/<username>')
@login_required
def dashboard(role,username):
    if(role=="admin"):

        return render_template(
            "admin/dashboard.html",
            role=role,
            username=username
        )
    elif(role=="user"):
        hospital_data = VaccinationRecord.query.filter_by(user_id=username).all()
        print(hospital_data)
        return render_template("home/dashboard.html",role=role,username=username,
            hospitals=hospital_data)
    else:
        
        return render_template("worker/dashboard.html",role=role)

