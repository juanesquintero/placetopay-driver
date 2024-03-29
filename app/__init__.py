'''
Initial Module for start and set up the Flask Appliaction
'''
import logging
from datetime import timedelta
from flask import Flask, render_template, session
from werkzeug.exceptions import HTTPException
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .utils.http_client import HttpClient

error_logger = logging.getLogger('error_logger')
DB = None


def create_app():
    # Instantiate app.
    app = Flask(__name__)

    # Set app configuration
    config(app)

    # Handle app errors
    handle_errors(app)

    # Define app db
    set_db(app)

    # Define login manager
    login_manager(app)

    # Define API CLient
    api_client(app)

    # Register app routes.
    register_routes(app)

    global DB
    DB.create_all()

    return app


def config(app):

    # Define app config
    app.config.from_object('config')

    # Forms csrf security
    csrf = CSRFProtect()
    csrf.init_app(app)

    # Secure Coockie Session  
    @app.before_request
    def make_session_permanent():
        session.modified = True
        session.permanent = True
        app.permanent_session_lifetime = timedelta(hours=2)


def set_db(app):
    global DB
    DB = SQLAlchemy(app)
    DB.init_app(app)


def login_manager(app):
    with app.app_context():
        from app.models import User
        # Set login manager
        login_manager = LoginManager()
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            return User().query.get(user_id)


def api_client(app):
    api = HttpClient(app.config['WEB_CHECKOUT_URL'], {'Content-type': 'application/json'})
    app.config['API_CLIENT'] = api


def register_routes(app):
    with app.app_context():
        # Import views as blueprints
        from .views import order, transaction, auth
        # Register blueprints.
        app.register_blueprint(auth)
        app.register_blueprint(order)
        app.register_blueprint(transaction)
    

def handle_errors(app):
    # Error handlers.
    error_template = 'error.html'

    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template(error_template, error=exc), exc.code

    @app.errorhandler(Exception)
    def handle_exception(e):
        error_logger.error('EXCEPTION: '+str(e), exc_info=True)
        err = {
            'code': 500,
            'name': 'Internal Server Error',
            'description': 'An Error has occurred on the application server, you might contact the administrator for more information'
        }
        return render_template(error_template, error=err, exception=True), 500
