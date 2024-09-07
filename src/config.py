# /src/config.py

import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

load_dotenv(override=True)  

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    SECRET_KEY = '9OLWxND4o83j4K4iuopO'
    UPLOAD_FOLDER = 'files/uploads'
    TEMPLATES_FOLDER = 'templates_data'
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    APP_VERSION='1.0.0.2'
    # MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    # MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')

class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    SECRET_KEY = '9OLWxND4o83j4K4iuopO'
    UPLOAD_FOLDER = 'files/uploads'
    TEMPLATES_FOLDER = 'templates_data'
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    APP_VERSION='1.0.0.2'

app_config = {
    'development': Development,
    'production': Production,
}