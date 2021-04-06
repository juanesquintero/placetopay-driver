from flask import Blueprint, render_template, flash, request
from app.forms.shop_forms import OrderForm
from app.utils.http_client import HttpClient
from app.models import Order


Home = Blueprint('Home', __name__)

api_client = HttpClient.get_instance()

product = dict(name='Xiaomi QiCYCLE', price=500, warranty=3)

@Home.route('/', methods=('GET', 'POST'))
def index():
    form = OrderForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            flash(f'Check your order carefully before go to pay, {form.customer_name.data}! ', 'info')
        else:
            product = None
            flash('There is an error on the order form', 'danger')
        return render_template('resume.html', resume=form, product=product)

    return render_template('index.html', form=form)

@Home.route('/status', methods=('GET'))
def order_detail():
    id = request.params.get('id')
    order = Order().query.filter_by(id=id).first()
    if not order:
        flash('This order does not exist', 'danger')
    return render_template('detail.html', order=order, product=product)
