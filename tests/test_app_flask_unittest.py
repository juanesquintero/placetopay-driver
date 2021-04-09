import sys
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir.replace('tests', ''))

import secrets
from random import randint

import flask.globals
from flask_unittest import ClientTestCase

from app import create_app
from app.forms.auth_forms import LoginForm, RegisterForm
from app.forms.shop_forms import OrderForm


random_name = secrets.token_hex(nbytes=randint(0, 10))
test_register_user = dict(
    name='Pepe '+random_name,
    username=random_name,
    password=random_name,
    confirm_password=random_name
)
test_login_user = dict(
    username=random_name,
    password=random_name,
)
product_keys = ['product_name', 'product_price', 'product_warranty']

class TestFoo(ClientTestCase):

    app = create_app()
    context = None

    def setUp(self, client):
        with self.app.app_context():
            self.app.config['TESTING'] = True
            self.app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
            from app.models import Order
            from app import DB
            self.models = dict(Order=Order)
            self.app_db = DB
        self.context = self.app.test_request_context()

    # def tearDown(self, client):
    #     pass

    def test_auth_routes(self, client):
        self.assertStatus(client.get('/login'), 200)
        self.assertStatus(client.get('/register'), 200)
        self.assertStatus(client.get('/logout'), 401)

    def test_register_form(self, client):
        with self.context:
            form = RegisterForm(**test_register_user)
        res = client.post(
            '/register',
            data=form.data,
            follow_redirects=True
        )
        self.assertStatus(res, 200)

    def test_login_form(self, client):
        with self.context:
            form = LoginForm(**test_login_user)
        res = client.post('/login', data=form.data)
        self.assertStatus(res, 200)

    def test_order_routes(self, client):
        self.assertStatus(client.get('/'), 200)
        self.assertStatus(client.get('/orders'), 200)
        
        order_ids = list(self.app_db.session.query(self.models['Order'].id).all())
        for ord_id in order_ids:
            path = f'/order-detail?id={ord_id[0]}'
            self.assertStatus(client.get(path), 200)

    def test_transaction_routes(self, client):
        with self.context:
            order = OrderForm(
                customer_name=random_name,
                customer_address='Cra56#5-45', 
                customer_mobile='123131312',
                customer_email=f'{random_name}@mail.com',
            )
            product = dict(zip(product_keys, self.app.config['PRODUCT'].values()))
            res = client.post('/create-request', data={**order.data, **product})
        self.assertStatus(res, 200)
        res = client.get('/answer-transaction')
        self.assertStatus(res, 200)
