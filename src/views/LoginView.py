# auth.py

from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from ..models.UserModel import UserModel, UserSchema
from marshmallow import ValidationError
from ..models.EventModel import EventModel, EventSchema
import datetime

app = Flask(__name__)
login_web = Blueprint('login_web', __name__)
user_schema = UserSchema()
event_schema = EventSchema()

@login_web.route('/login')
def login():
    return render_template('login.html')

@login_web.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    remember = False

    user_in_db = UserModel.get_user_by_email(email)
        
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user_in_db: 
        flash('Please check your login details and try again.')
        return redirect(url_for('login_web.login')) # if user doesn't exist or password is wrong, reload the page
    if not user_in_db.check_hash(password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login_web.login')) # if user doesn't exist or password is wrong, reload the page
    
    # if the above check passes, then we know the user has the right credentials
    login_user(user_in_db, remember=remember)
    return redirect(url_for('main_web.dashboard'))

# @login_web.route('/signup')
# def signup():
#     return render_template('signup.html')

# @login_web.route('/signup', methods=['POST'])
# def signup_post():

#     email = request.form.get('email')
#     name = request.form.get('name')
#     password = request.form.get('password')

#     user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

#     if user: # if a user is found, we want to redirect back to signup page so user can try again  
#         flash('Email address already exists')
#         return redirect(url_for('auth.signup'))

#     # create new user with the form data. Hash the password so plaintext version isn't saved.
#     new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

#     # add the new user to the database
#     db.session.add(new_user)
#     db.session.commit()

#     return redirect(url_for('auth.login'))

@login_web.route('/logout')
@login_required
def logout():

    # try:
    #     event_data_json = {
    #         "datetime" : datetime.datetime.now(datetime.timezone.utc).isoformat(),
    #         "source" : "dds_web_admin",
    #         "eventtype" : "Activity",
    #         "info" : 'Logout System',
    #         "details" : current_user.email,
    #     }
    #     event_data = event_schema.load(event_data_json)
    #     eventModel = EventModel(event_data)
    #     eventModel.save()
    #     data = event_schema.dump(eventModel)

    # except Exception as e:
    #     print('Error create event', e)
    #     pass

    logout_user()
    return redirect(url_for('main_web.index'))