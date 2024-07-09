
import hashlib
from flask import Blueprint
from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
import re
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth' , __name__)


@auth.route('/login', methods =['GET','POST']) 
def login(): # call the def the same name as route
    if request.method =='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password==hashlib.sha256(password.encode()).hexdigest():
                flash("Logged in successfully",category="success")
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, Try again",category="error")
        else:
            flash("Email does not exist.",category="error")

    return render_template("login.html",user = current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        Currency = request.form.get('country-selector')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("This email already exists", category="error")
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 2 character.', category='error')
        elif bool(re.match(r'^[a-zA-Z0-9_]*$', first_name)) == False:
            flash('First name can\'t have special characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            import hashlib

            hashed_password = hashlib.sha256(password1.encode()).hexdigest()

            new_user = User(email=email, first_name=first_name, password=hashed_password,Country=Currency)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)  # Use new_user here instead of user
            flash("Account was created successfully!", category="success")
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

