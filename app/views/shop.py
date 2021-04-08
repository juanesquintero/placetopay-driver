from flask import Blueprint, render_template, flash, request
from app.forms.shop_forms import OrderForm
from app.utils.http_client import HttpClient
from app.models import Order

from app.utils.mixins import insert_row_from_form

Shop = Blueprint('Shop', __name__)

api_client = HttpClient.get_instance()

PRODUCT = dict(name='Xiaomi QiCYCLE', price=500, warranty=3)


@Shop.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            # Create and save user
            saved = insert_row_from_form(Order, form)
            if saved:
                flash(f'Check your order carefully before go to pay, {form.customer_name.data}! ', 'info')
            else:
                flash(f'Your order could not be saved, {form.customer_name.data}! ', 'danger')
        else:
            form = None
            flash('There is an error on the order form', 'danger')
        return render_template('resume.html', resume=form, product=PRODUCT if form else None)

    return render_template('index.html', form=form)


@Shop.route('/orders', methods=['GET'])
def orders_list():
    orders = Order().query.all()
    if not orders:
        flash('There are not orders yet :(', 'alert')
    return render_template('list.html', orders_list=orders)


@Shop.route('/status', methods=['GET'])
def order_detail():
    order_id = request.args.get('id')
    order = Order().query.filter_by(id=order_id).first()
    if not order:
        flash('This order does not exist', 'alert')
    return render_template('detail.html', order=order, product=PRODUCT if order else None)


@Shop.route('/pay', methods=['POST'])
def payment():
    return render_template('index.html')
