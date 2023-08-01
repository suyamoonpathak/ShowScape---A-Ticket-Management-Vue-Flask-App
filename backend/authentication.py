from flask import Blueprint, request, jsonify
from .models import User
from . import db
authentication = Blueprint("authentication", __name__)
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token

bcrypt = Bcrypt()

@authentication.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    isAdmin = data.get('isAdmin')

    if not username or not email or not password:
        return jsonify({'message': 'Username, email, and password are required.'}), 400

    # Check if the email is already taken
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email address already registered. Please use a different email.'}), 400

    # Create a new user and save it to the database
    new_user = User(username=username, email=email, password=password, is_admin=isAdmin)
    db.session.add(new_user)
    db.session.commit()

    if(new_user.is_admin):
            additional_claims = {
            'username': new_user.username,
            'role': 'admin',
            'admin_id':new_user.id
        }
    else:
            additional_claims = {
            'username': new_user.username,
            'role': 'client',
            'user_id':new_user.id
        }

    access_token = create_access_token(identity=new_user.id, additional_claims=additional_claims)
    return jsonify({'message': 'User signup successful.', 'access_token': access_token}), 201

@authentication.route('/api/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    isAdmin = data.get('isAdmin')

    if not username or not password:
        return jsonify({'message': 'Username and password are required.'}), 400

    # Query the user from the database by username
    user = User.query.filter_by(username=username).first()

    if not user or user.password!=password:
        return jsonify({'message': 'Invalid username or password.'}), 401

    # Generate an access token for the authenticated user
    if user:
        if(user.is_admin):
            additional_claims = {
            'username': user.username,
            'role': 'admin',
            'admin_id':user.id
        }
        else:
            additional_claims = {
            'username': user.username,
            'role': 'client',
            'user_id':user.id
        }

    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    return jsonify({'access_token': access_token}), 200