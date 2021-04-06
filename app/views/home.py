from flask import Blueprint, render_template, flash
from app.forms.shop_forms import OrderForm
from app.utils.http_client import HttpClient

Home = Blueprint('Home', __name__)

api_client = HttpClient.get_instance()

@Home.route('/', methods=('GET', 'POST'))
def index():
    form = OrderForm()
    if form.validate_on_submit():
        flash(
            f'Your order was sended successfully, {form.name.data}! ',
            'success'
        )
    return render_template('index.html', form=form)
