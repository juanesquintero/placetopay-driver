'''
The main config file for the appliaction,
contains all the important constants for configuration and to make it work just fine 
'''
import logging
import os
from datetime import datetime

base_dir = os.path.abspath(os.path.dirname(__file__))

APP_NAME = 'Virtual Shop - PlaceToPay'
APP_ICON = '/static/img/logo.png'
CURRENT_YEAR = datetime.now().year

# Reloadn on Jinja templates change
TEMPLATES_AUTO_RELOAD = True

DEBUG_TB_ENABLED = False

# Session Encryption key
SECRET_KEY = os.environ.get('SECRET_KEY')

# Security of forms
WTF_CSRF_ENABLED = False
WTF_CSRF_SECRET_KEY='a csrf secret key'

# Recaptcha
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = 'reCAPTCHA_site_key'
RECAPTCHA_PRIVATE_KEY = 'enter_your_private_key'
RECAPTCHA_OPTIONS = {'theme':'black'}

# Folders to save uploads
UPLOAD_URL = '/app/static/uploads/'
UPLOAD_FOLDER = base_dir + UPLOAD_URL
IMG_UPLOAD_FOLDER = base_dir + UPLOAD_URL + '/images'

# SQLALCHEMY DB Config
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'db/app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Custom env vars
API_PATH = os.environ.get('API_PATH')

WEB_CHECKOUT_URL = os.environ.get('WEB_CHECKOUT_URL')
WEB_CHECKOUT_LOGIN = os.environ.get('WEB_CHECKOUT_LOGIN')
WEB_CHECKOUT_SECRET_KEY = os.environ.get('WEB_CHECKOUT_SECRET_KEY')

APP_RETURN_URL = 'http://localhost:5000/answer-transaction'
CURRENCY = 'USD'
PRODUCT = dict(name='Xiaomi QiCYCLE', price=500, warranty=3)

'''LOGGING CONFIG'''
LOG_FORMAT = '%(asctime)s:%(levelname)s:%(name)s:%(message)s'
LOG_DIR = base_dir + '/logs'

# # GENERAL LOGS (ALL)
# logging.getLogger().setLevel(logging.DEBUG)
# logging.basicConfig(filename=LOG_DIR+'/GENERALS.log',level=logging.DEBUG,format=LOG_FORMAT)

# ERROR LOGS
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler(LOG_DIR+'/ERRORS.log')
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
error_logger.addHandler(file_handler)
'''END LOGGING CONFIG'''
