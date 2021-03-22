from api import app
from api.models import db
import os

app.testing = True
app_context = app.test_request_context()
app_context.push()
client = app.test_client()

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
db.drop_all()
db.create_all()
