from flask import Flask
from flask import Response
from flask import render_template
from flask import abort
from flask import request, jsonify
from flask_cors import CORS
from .config import app_config
from .models import db, bcrypt
from .views.UserView import user_api as user_blueprint
from .views.ActivityView import activity_api as activity_blueprint
from .views.IncidentsView import incident_api as incident_blueprint
from .views.MainView import main_web as main_blueprint
from .views.LoginView import login_web as login_blueprint
from datetime import datetime
from flask_login import LoginManager 
from .models.UserModel import UserModel, UserSchema
from time import sleep

def create_app(env_name):

    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(app_config[env_name])

    login_manager = LoginManager()
    login_manager.login_view = 'login_web.login'
    login_manager.init_app(app)

    db.init_app(app)

    # print('SECRET_KEY',app.config['SECRET_KEY'])


    # app.config['UPLOAD_FOLDER'] = 'uploads'
    # app.config['TEMPLATES_FOLDER'] = 'templates_data'
    # app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    # app.secret_key = 'your_secret_key'  # Needed for flashing messages

    # Initialize the DocumentProcessor with the directories of YAML templates
    # template_dirs = [
    #     'templates_data/invoices/', 
    #     'templates_data/receipts/', 
    #     'templates_data/credit_notes/'
    # ]
    # processor = DocumentProcessor(template_dirs=template_dirs)

    app.register_blueprint(user_blueprint, url_prefix='/api/auth')
    app.register_blueprint(activity_blueprint, url_prefix='/api/activity')
    app.register_blueprint(incident_blueprint, url_prefix='/api/incident')
    app.register_blueprint(login_blueprint)
    app.register_blueprint(main_blueprint)
    

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return UserModel.get_one_user(int(user_id))
    

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    return app
