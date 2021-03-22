import os
from flask import Flask
from .blueprints.user_blueprint import user_bp
from .models import configure_db
from dotenv import load_dotenv
load_dotenv()


pg_user = os.getenv('POSTGRES_USER')
pg_password = os.getenv('POSTGRES_PASSWORD')
pg_database = os.getenv('POSTGRES_DB')


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{pg_user}:{pg_password}@localhost:5432/{pg_database}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

configure_db(app)

app.register_blueprint(user_bp, url_prefix='/api/users')
