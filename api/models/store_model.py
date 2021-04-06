from . import db, ma
from datetime import datetime


class StoreModel(db.Model):
    __tablename__ = 'store'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    street = db.Column(db.String(150), nullable=False)
    number = db.Column(db.String(30), nullable=False)
    district = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    state = db.Column(db.String(30), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    def __repr__(self):
        return f"<Store: {self.name}>"


class StoreSchema(ma.SQLAlchemySchema):
    class Meta:
        model = StoreModel

    id = ma.auto_field()
    name = ma.auto_field()
    phone = ma.auto_field()
    street = ma.auto_field()
    number = ma.auto_field()
    district = ma.auto_field()
    city = ma.auto_field()
    state = ma.auto_field()
