from app import DB as db


class Order(db.Model):

    id =  db.Column(db.Integer , primary_key=True , autoincrement=True)
    customer_username = db.Column(db.String(80), unique=False, nullable=False)
    customer_email = db.Column(db.String(120), unique=True, nullable=False)
    custromer_mobile = db.Column(db.String(40), unique=True, nullable=False)
    status = db.Column(db.String(20), default='CREATED') # “CREATED, PAYED, REJECTED” 
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, default=None)
    
