from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def configure_db(app):
    db.init_app(app)
    ma.init_app(app)

    migrate.init_app(app, db)

    app.db = db
    app.ma = ma
