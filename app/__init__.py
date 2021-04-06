'''
Modulo que inicia y configura la Aplicación de Flask
'''
from flask import Flask, render_template
from werkzeug.exceptions import HTTPException
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .utils.api_client import APIClient

DB = None

def create_app(testing=False):
    # Instantiate app.
    app = Flask(__name__)

    # Set app configuration
    config(app, testing)

    # Define app db
    set_db(app)

    # Define login manager
    login_manager(app)

    # Define API CLient
    api_client(app)

    # Register app routes.
    register_routes(app)

    # Handle app errors
    handle_errors(app)

    global DB
    DB.create_all()

    return app


def config(app, testing):

    # Define app config
    app.config.from_object('config')
    if testing:
        app.config['TESTING'] = True
        app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False

    # Forms csrf security
    csrf = CSRFProtect()
    csrf.init_app(app)


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
    api = APIClient(app.config['WEB_CHECKOUT_URL'])
    app.config['API_CLIENT'] = api


def register_routes(app):
    # Import views as blueprints
    from .views import Home, Auth

    # Register blueprints.
    app.register_blueprint(Home)
    app.register_blueprint(Auth)


def handle_errors(app):
    # Error handlers.
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template('error.html', error=exc), exc.code
