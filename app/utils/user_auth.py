from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):

    def __init__(self, username=None, name=None, password=None, is_admin=False):
        self.username = username
        self.name = name
        self.password = generate_password_hash(password) if password else None
        self.is_admin = is_admin

    def get_id(self):
        return (self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username
