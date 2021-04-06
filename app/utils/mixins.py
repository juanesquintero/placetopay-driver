# Add your own utility classes and functions here.
from wtforms.validators import DataRequired
# Rember separete the logic of the views and use_cases

def please_enter(field_name='value', connector='a', valid=False):
    if valid:
        connector = connector + 'valid'
    return DataRequired(f'Please enter {connector} {field_name}')
