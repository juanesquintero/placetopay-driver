import socket
import logging
from datetime import datetime, timedelta

from flask import Blueprint, render_template, flash, request, current_app, redirect, session
from app.forms.shop_forms import OrderForm

from app.models import Order
from app.utils.mixins import insert_row_from_form, update_record, auth_webcheckout, buyer_webcheckout, payment_webcheckout

error_logger = logging.getLogger('error_logger')
transaction = Blueprint('transaction', __name__)

api_client = api_client = current_app.config['API_CLIENT']
APP_CONFIG = current_app.config

@transaction.route('/create-request', methods=['POST'])
def create_request():
    order = OrderForm()
    form = request.form

    res = api_client.post('session', create_request_body(order, form))
    if res:
        # Create and save user
        saved = insert_row_from_form(Order, order)
        if saved:
            session['request_id'] = res['requestId']
            session['current_order'] = saved.id
            session['process_url'] = res['processUrl']
            update_record(saved, 'payment_request_id', res['requestId'])
            return redirect(res['processUrl'])
        
        flash(
            f'Your order could not be saved, {order.customer_name.data}! ',
            'danger')
    return render_template('index.html')


@transaction.route('/answer-transaction', methods=['GET'])
def answer_transaction():
    status, info = '', {}
    if 'request_id' in session.keys():
        res = api_client.post(
            'session/{}'.format(session['request_id']),
            dict(
                auth=auth_webcheckout(
                    APP_CONFIG['WEB_CHECKOUT_LOGIN'],
                    APP_CONFIG['WEB_CHECKOUT_SECRET_KEY'])
            )
        )
        if res:
            status = set_order_status(res)
            info = dict(
                status=res['status']['status'],
                message=res['status']['message']
            )
        del session['request_id']
    else:
        flash('There is none order-payment in progress', 'danger')
    return render_template(
        'transactions/status.html',
        status=status,
        info=info
    )


def set_order_status(res):
    transaction_status = res['status']
    if 'fields' in res['request']:
        session['state_process_url'] = res['request']['fields'][0]['value']

    current_order = Order().query.filter_by(id=session['current_order']).first()
    if current_order:
        if transaction_status['status'] == 'APPROVED':
            update_record(current_order, 'status', 'PAYED')
        elif transaction_status['status'] == 'REJECTED':
            update_record(current_order, 'status', 'REJECTED')

    return transaction_status['status']

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
            expiration=(datetime.now() + timedelta(minutes=10)
                        ).strftime('%Y-%m-%dT%H:%M:%S-5:00'),
            returnUrl=APP_CONFIG['APP_RETURN_URL'],
            ipAddress=socket.gethostbyname(socket.getfqdn()),
            userAgent='PlacetoPay Sandbox'
        )
    except Exception as e:
        error_logger.error('EXCEPTION: '+str(e), exc_info=True)
        body = None
    return body
