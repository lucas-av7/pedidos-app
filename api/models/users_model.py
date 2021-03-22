from . import db, ma
from datetime import datetime
from .users_address_model import UsersAddressModel


class UsersModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    address = db.relationship('UsersAddressModel', backref='users', lazy=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    def __repr__(self):
        return f"<User: {self.name}>"


class UsersSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UsersModel

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
