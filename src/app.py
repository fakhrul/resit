from flask import Flask, render_template
from flask import request, jsonify, abort, Response
from flask_cors import CORS
from flask_talisman import Talisman  # Import Flask-Talisman
from .config import app_config
from .models import db, bcrypt
from .views.UserView import user_api as user_blueprint
from .views.ReceiptView import receipt_api as receipt_blueprint
from .views.ActivityView import activity_api as activity_blueprint
from .views.IncidentsView import incident_api as incident_blueprint
from .views.MainView import main_web as main_blueprint
from .views.LoginView import login_web as login_blueprint
from datetime import datetime
from flask_login import LoginManager
from .models.UserModel import UserModel, UserSchema
from time import sleep
import os

def create_app(env_name):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(app_config[env_name])

    # Setup LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'login_web.login'
    login_manager.init_app(app)

    # Initialize the database
    db.init_app(app)

    # Register your blueprints
    app.register_blueprint(user_blueprint, url_prefix='/api/auth')
    app.register_blueprint(activity_blueprint, url_prefix='/api/activity')
    app.register_blueprint(receipt_blueprint, url_prefix='/api/receipts')
    app.register_blueprint(incident_blueprint, url_prefix='/api/incident')
    app.register_blueprint(login_blueprint)
    app.register_blueprint(main_blueprint)

    # Load user for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return UserModel.get_one_user(int(user_id))

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    # Define the Content Security Policy (CSP)
    csp = {
        'default-src': "'self'",  # Default to 'self' (same-origin)
        'style-src': ["'self'", 'https://cdn.jsdelivr.net', "'unsafe-inline'"],  # Allow external styles
        'script-src': ["'self'", 'https://ajax.googleapis.com', 'https://docs.opencv.org', "'unsafe-eval'", "'unsafe-inline'"],  # Allow external scripts
        'connect-src': ["'self'",'https://resit.safa.com.my', 'data:'],  # Allow data: URIs for connections
    }


    # Conditionally enable Flask-Talisman
    # Enable Talisman (force HTTPS) only if USE_TALISMAN is true (for production environments)
    if os.getenv('USE_TALISMAN', 'false').lower() == 'true':
        Talisman(app, content_security_policy=csp)
        print("Talisman enabled: HTTPS will be enforced.")
    else:
        print("Talisman disabled: HTTPS will not be enforced.")

    return app
