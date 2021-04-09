from flask import Blueprint, render_template, flash, request, current_app, session
from app.forms.shop_forms import OrderForm

from app.models import Order
from app.utils.mixins import insert_row_from_form, update_record, auth_webcheckout, buyer_webcheckout, payment_webcheckout

order = Blueprint('order', __name__)

api_client = api_client = current_app.config['API_CLIENT']
APP_CONFIG = current_app.config


@order.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            flash(
                f'Check your order carefully before go to pay, {form.customer_name.data}! ',
                'info')
        else:
            form = None
            flash('There is an error on the order form', 'danger')
        return render_template('orders/resume.html', resume=form, product=APP_CONFIG['PRODUCT'] if form else None)

    return render_template('index.html', form=form)


@order.route('/orders', methods=['GET'])
def orders_list():
    orders = Order().query.all()
    if not orders:
        flash('There are not orders yet :(', 'dark ')
    return render_template('orders/list.html', orders_list=orders)


@order.route('/order-detail', methods=['GET'])
def order_detail():
    order_id = request.args.get('id')
    order = Order().query.filter_by(id=order_id).first()
    if not order:
        flash('This order does not exist', 'warning')
    return render_template('orders/detail.html', order=order, product=APP_CONFIG['PRODUCT'] if order else None)
