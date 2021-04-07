# Add your own utility classes and functions here.
# Remember separete the logic of the views and use_cases
import logging
import hashlib
import base64
from datetime import datetime
from wtforms.validators import DataRequired
from app import DB


error_logger = logging.getLogger('error_logger')

def convert_to_sha1(word):
    digest = hashlib.sha1(word.encode()).hexdigest()
    return digest

def  convert_to_base64(word):
    base_64 = base64.b64encode(word.encode())
    return base_64.decode()

def generate_auth_webcheckout(login, secretkey):
    seed = datetime.now().strftime('%Y-%m-%dT%H:%M:%S-5:00')
    nonce = 'c9085e82debb82b0955579098be3d7ca'
    tran_key = convert_to_base64(convert_to_sha1(str(nonce + seed + secretkey)))

    auth = dict(
        login=login,
        tranKey=tran_key,
        nonce=convert_to_base64(nonce),
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
