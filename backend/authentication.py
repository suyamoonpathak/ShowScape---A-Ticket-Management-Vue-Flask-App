from flask import Blueprint, request, jsonify
from .models import User
from . import db
authentication = Blueprint("authentication", __name__)

@authentication.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Username, email, and password are required.'}), 400

    # Check if the email is already taken
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email address already registered. Please use a different email.'}), 400

    # Create a new user and save it to the database
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User signup successful.'}), 201

@authentication.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if user.password== password:
                 return jsonify({'message': 'logged in'}), 200
            else:
                return jsonify({'message': 'wrong credentials'}), 400
        else:
            return jsonify({'message': 'username doesnt exist'}), 400