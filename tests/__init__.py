from api import app
import os

app.testing = True
app_context = app.test_request_context()
app_context.push()

pg_user = os.getenv('PG_USER')
pg_password = os.getenv('PG_PASSWORD')
pg_database = os.getenv('PG_DATABASE')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{pg_user}:{pg_password}@localhost:5432/test"
