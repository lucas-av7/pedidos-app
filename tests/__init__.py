from api import app
from api.models import db
from flask import url_for
import os
from dotenv import load_dotenv
load_dotenv()

app.testing = True
app_context = app.test_request_context()
app_context.push()
client = app.test_client()

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
db.drop_all()
db.create_all()

# Creating user for testing
client.post(url_for('users_bp.users_create'), json={
    "name": "Lucas Vasconcelos",
    "email": "lucas@email.com",
    "phone": "(85) 90000-0000",
    "password": "password123"
})
