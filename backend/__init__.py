from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from os import path
from .secrets import DATABASE_PATH, JWT_SECRET, STRIPE_SECRET_KEY
import stripe

app = Flask(__name__)

app.config.from_object(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})


#change the constants as per your own requirements
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET

UPLOAD_FOLDER = path.join(path.dirname(
    path.realpath(__file__)), 'static/images/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db = SQLAlchemy(app)
jwt = JWTManager(app)
stripe.api_key = STRIPE_SECRET_KEY

from .authentication import authentication
from .theatre_management import theatre_management
from .show_management import show_management
from .booking_management import booking_management

app.register_blueprint(authentication, url_prefix="/")
app.register_blueprint(theatre_management, url_prefix="/")
app.register_blueprint(show_management, url_prefix="/")
app.register_blueprint(booking_management,url_prefix="/")

@app.route('/',methods=['GET'])
def helloWorld():
    return ("Hello Worlds!")

from .models import User, Theatre, Show, Booking
with app.app_context():
    db.create_all()

