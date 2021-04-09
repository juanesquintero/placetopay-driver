from app import DB as db
from flask_login import UserMixin
from app.utils.user_auth import User as UserAuth
class User( UserAuth, db.Model):

    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(150), unique=False, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
