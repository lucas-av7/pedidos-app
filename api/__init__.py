import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from .blueprints.user_blueprint import user_bp


pg_user = os.getenv('PG_USER')
pg_password = os.getenv('PG_PASSWORD')
pg_database = os.getenv('PG_DATABASE')


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{pg_user}:{pg_password}@localhost:5432/{pg_database}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)

app.register_blueprint(user_bp, url_prefix='/api/user')
