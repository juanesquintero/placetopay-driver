import socket
import logging
from datetime import datetime, timedelta

from flask import Blueprint, render_template, flash, request, current_app, redirect, session
from app.forms.shop_forms import OrderForm
from app.utils.http_client import HttpClient

from app.models import Order
from app.utils.mixins import insert_row_from_form, auth_webcheckout, buyer_webcheckout, payment_webcheckout

error_logger = logging.getLogger('error_logger')
Shop = Blueprint('Shop', __name__)

api_client = api_client = current_app.config['API_CLIENT']
APP_CONFIG = current_app.config


@Shop.route('/', methods=['GET', 'POST'])
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


@Shop.route('/orders', methods=['GET'])
def orders_list():
    orders = Order().query.all()
    if not orders:
        flash('There are not orders yet :(', 'alert')
    return render_template('orders/list.html', orders_list=orders)


@Shop.route('/status', methods=['GET'])
def order_detail():
    order_id = request.args.get('id')
    order = Order().query.filter_by(id=order_id).first()
    if not order:
        flash('This order does not exist', 'warning')
    return render_template('orders/detail.html', order=order, product=PRODUCT if order else None)


@Shop.route('/create-request', methods=['POST'])
def create_request():
    order = OrderForm()
    form = request.form

    res = api_client.post('session', create_request_body(order, form))
    if res:
        # Create and save user
        saved = insert_row_from_form(Order, order)
        if saved:
            session['requestId'] = res['requestId']
            return redirect(res['processUrl'])
        else:
            flash(
                f'Your order could not be saved, {order.customer_name.data}! ',
                'danger')
    
    return render_template('index.html')


@Shop.route('/answer-transaction', methods=['GET'])
def answer_transaction():
    if 'requestId' in session.keys():
       flash('This is your webcheckout requestId is: {}'.format(session['requestId']), 'info')
       del session['requestId']
    else:
        flash('There is none order-payment in progress', 'danger')
    return render_template('index.html')


def create_request_body(order, form):
    try:
        auth = auth_webcheckout(
            APP_CONFIG['WEB_CHECKOUT_LOGIN'],
            APP_CONFIG['WEB_CHECKOUT_SECRET_KEY']
        )
        buyer = buyer_webcheckout(order)
        payment = payment_webcheckout(form, APP_CONFIG['CURRENCY'])
        body = dict(
            auth=auth,
            buyer=buyer,
            payment=payment,
            expiration=(datetime.now() + timedelta(minutes=10)).strftime('%Y-%m-%dT%H:%M:%S-5:00'),
            returnUrl=APP_CONFIG['APP_RETURN_URL'],
            ipAddress=socket.gethostbyname(socket.getfqdn()),
            userAgent='PlacetoPay Sandbox'
        )
    except Exception as e:
        error_logger.error('EXCEPTION: '+str(e), exc_info=True)
        body = None
    return body
