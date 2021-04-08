# Add your own utility classes and functions here.
# Remember separete the logic of the views and use_cases
import logging
import hashlib
import base64
import secrets
from random import randint
from datetime import datetime

from wtforms.validators import DataRequired
from app import DB


error_logger = logging.getLogger('error_logger')

def sha1_encode(word):
    word_encoded = word.encode()
    digest = hashlib.sha1(word_encoded)
    return digest

def  base64_encode(word):
    word_encoded = word.encode()
    base_64 = base64.b64encode(word_encoded)
    return base_64.decode()

def sha1_and_base64_encode(word):
    sha1_digest = hashlib.sha1(word.encode()).digest()
    base64_encode_sha1 = base64.b64encode(sha1_digest)
    return base64_encode_sha1.decode()

def generate_auth_webcheckout(login, secretkey):
    nonce = secrets.token_hex(nbytes=randint(0, 10))
    seed = datetime.now().strftime('%Y-%m-%dT%H:%M:%S-5:00')
    tran_key = sha1_and_base64_encode(nonce + seed + secretkey)
    auth = dict(
        login=login,
        tranKey=tran_key,
        nonce=base64_encode(nonce),
        seed=seed
    )

    return auth

def please_enter(field_name='value', connector='a', valid=False):
    if valid:
        connector = connector + 'valid'
    return DataRequired(f'Please enter {connector} {field_name}')

def insert_row_from_form(db_model, form):
    data = form.data
    try:
        del data['csrf_token']
        obj = db_model(**data)
        DB.session.add(obj)
        DB.session.commit()
        return True
    except Exception as e:
        error_logger.error('EXCEPTION: '+str(e), exc_info=True)
        return False
