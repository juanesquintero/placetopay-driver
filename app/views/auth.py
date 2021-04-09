from flask import Blueprint, render_template, redirect, flash, url_for, current_app
from app.forms.auth_forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required

from app.models import User
from app.utils.http_client import HttpClient
from app import DB

auth = Blueprint('auth', __name__)

api_client = current_app.config['API_CLIENT']

@auth.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('order.index'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User().query.filter_by(username=form.username.data).first()
        valid_password = user.check_password(form.password.data) if user else False

        if user and valid_password:
            login_current_user(user)
            flash(f'Welcome {form.username.data}! ', 'info')
            return redirect(url_for('order.index'))

        flash('Invalid credentials! ', 'danger')

    return render_template('auth/login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('order.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Create and save user
        user = User(
            username=form.username.data,
            name=form.name.data,
            password=form.password.data,
            is_admin=True
        )
        # Send msg
        try:
            DB.session.add(user)
            DB.session.commit()
        except Exception as e:
            flash('Your are already singed up! Please login!', 'danger')
            return redirect(url_for('order.index'))

        login_current_user(user)
        flash(f'Your are now singed up! {form.name.data} ({form.username.data})', 'success')
        return render_template('index.html')

        
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    api_client.set_headers(None)
    return redirect(url_for('order.index'))


def login_current_user(user):
    login_user(user)
    api_client.set_headers({})
