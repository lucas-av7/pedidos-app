import os
from flask import Flask, abort, jsonify
from .blueprints.users_blueprint import users_bp
from .blueprints.users_address_blueprint import users_address_bp
from .models import configure_db
from dotenv import load_dotenv
load_dotenv()


pg_user = os.getenv('POSTGRES_USER')
pg_password = os.getenv('POSTGRES_PASSWORD')
pg_database = os.getenv('POSTGRES_DB')


app = Flask(__name__)
app.url_map.strict_slashes = False

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{pg_user}:{pg_password}@localhost:5432/{pg_database}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

configure_db(app)

app.register_blueprint(users_bp, url_prefix='/api')
app.register_blueprint(users_address_bp, url_prefix='/api')


# Custom error response for all api endpoints
@app.errorhandler(405)
def not_allowed(e):
    return jsonify({
        "status": "Error",
        "status_code": 405,
        "message": "Method not allowed"
    }), 405


@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "status": "Error",
        "status_code": 404,
        "message": "API endpoint not found"
    }), 404
