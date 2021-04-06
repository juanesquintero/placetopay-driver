from flask import Blueprint, render_template, flash
from app.forms.home_forms import HomeForm
from app.utils.http_client import HttpClient

Home = Blueprint('Home', __name__)

api_client = HttpClient.get_instance()

@Home.route('/', methods=('GET', 'POST'))
def index():
    form = HomeForm()
    if form.validate_on_submit():
        flash(
            f'Your info was sended successfully, {form.name.data}! ',
            'success'
        )
    return render_template('index.html', form=form)

@Home.route('/api')
def api_call():
    res = api_client.get('')
    return render_template('index.html', response=res)

@Home.route('/apifail')
def api_call_fail():
    res = api_client.get('sdfsdf')
    return render_template('index.html', response=res)
