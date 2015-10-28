from datetime import datetime
from app import db


# Contact model
class Contact(db.Model):

    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.String, nullable=False)
    tenant_id = db.Column(db.String, nullable=False)

    def __init__(self, name, email, phone, user_id, tenant_id):
        self.name = name
        self.email = email
        self.phone = phone
        self.user_id = user_id
        self.tenant_id = tenant_id
