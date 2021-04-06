# Add your own utility classes and functions here.
# Remember separete the logic of the views and use_cases
import logging
from wtforms.validators import DataRequired
from app import DB

error_logger = logging.getLogger('error_logger')

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
