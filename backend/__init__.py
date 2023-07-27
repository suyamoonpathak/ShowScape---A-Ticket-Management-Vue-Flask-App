from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)

app.config.from_object(__name__)
CORS(app,resources={r"/*":{'origins':'*'}})

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


from .authentication import authentication
app.register_blueprint(authentication, url_prefix="/")

@app.route('/',methods=['GET'])
def helloWorld():
    return ("Hello Worlds!")

from .models import User, Theatre, Show, Booking
with app.app_context():
    db.create_all()

