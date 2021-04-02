from . import db, ma
from datetime import datetime


class UsersAddressModel(db.Model):
    __tablename__ = 'users_address'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    street = db.Column(db.String(150), nullable=False)
    number = db.Column(db.String(30), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(9), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    def __repr__(self):
        return f"<Address: {self.street}, {self.number} - {self.district}>"


class UsersAddressSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UsersAddressModel

    id = ma.auto_field()
    street = ma.auto_field()
    number = ma.auto_field()
    district = ma.auto_field()
    zipcode = ma.auto_field()
    city = ma.auto_field()
    state = ma.auto_field()
