# project/models.py

from views import db


# Contact model
class Contact(db.Model):

    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    tenant_id = db.Column(db.String, nullable=False)

    def __init__(self, name, email, username, tenant_id):
        self.name = name
        self.email = email
        self.username = username
        self.tenant_id = tenant_id
