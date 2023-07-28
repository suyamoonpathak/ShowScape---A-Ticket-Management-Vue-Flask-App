from . import app
from . import db
from flask import Blueprint,jsonify,request
from .models import Theatre

theatre_management = Blueprint("theatre_management", __name__)

@theatre_management.route('/api/theatres/admin/<int:admin_id>', methods=['GET'])
def get_theatres_for_admin(admin_id):
    theatres = Theatre.query.filter_by(admin_id=admin_id).all()
    return jsonify([theatre.as_dict() for theatre in theatres])

@theatre_management.route('/api/theatres/<int:theatre_id>', methods=['GET'])
def get_theatre_by_id(theatre_id):
    theatre = Theatre.query.get(theatre_id)
    if theatre:
        return jsonify(theatre.as_dict())
    return jsonify({'message': 'Theatre not found'}), 404

@theatre_management.route('/api/theatres', methods=['POST'])
def create_theatre():
    data = request.get_json()
    new_theatre = Theatre(name=data.get('name'), place=data.get('place'), capacity=data.get('capacity'), admin_id=data.get('admin_id'))
    db.session.add(new_theatre)
    db.session.commit()
    return jsonify(new_theatre.as_dict()), 201

@theatre_management.route('/api/theatres/<int:theatre_id>', methods=['PUT'])
def update_theatre(theatre_id):
    theatre = Theatre.query.get(theatre_id)
    if theatre:
        data = request.get_json()
        theatre.name = data.get('name')
        theatre.place = data.get('place')
        theatre.capacity = data.get('capacity')
        db.session.commit()
        return jsonify(theatre.as_dict())
    return jsonify({'message': 'Theatre not found'}), 404

@theatre_management.route('/api/theatres/<int:theatre_id>', methods=['DELETE'])
def delete_theatre(theatre_id):
    theatre = Theatre.query.get(theatre_id)
    if theatre:
        db.session.delete(theatre)
        db.session.commit()
        return jsonify({'message': 'Theatre deleted successfully'}), 200
    return jsonify({'message': 'Theatre not found'}), 404
