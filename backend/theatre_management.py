from . import app
from . import db, redis_client
from flask import Blueprint,jsonify,request
from .models import Theatre,Show,Booking

theatre_management = Blueprint("theatre_management", __name__)

@theatre_management.route('/api/theatres/admin/<int:admin_id>', methods=['GET'])
def get_theatres_for_admin(admin_id):
    try:
        cached_data = redis_client.get(f'theatres_for_admin_{admin_id}')
        if cached_data:
            return cached_data, 200
        theatres = Theatre.query.filter_by(admin_id=admin_id).all()
        theatres_data = [theatre.as_dict() for theatre in theatres]
        theatres_data_json = jsonify(theatres_data)
        redis_client.setex(f'theatres_for_admin_{admin_id}', 5, theatres_data_json.data)
        return theatres_data_json, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@theatre_management.route('/api/theatres/<int:theatre_id>', methods=['GET'])
def get_theatre_by_id(theatre_id):
    cached_data = redis_client.get(f'theatres_by_id_{theatre_id}')
    if cached_data:
        return cached_data, 200
    theatre = Theatre.query.get(theatre_id)
    if theatre:
        theatres_data_json = jsonify(theatre.as_dict())
        redis_client.setex(f'theatres_by_id_{theatre_id}', 5, theatres_data_json.data)
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
    if not theatre:
        return jsonify({'message': 'Theatre not found'}), 404
    try:
        shows = Show.query.filter_by(theatre_id=theatre_id).all()
        for show in shows:
            bookings = Booking.query.filter_by(show_id=show.id).all()
            for booking in bookings:
                db.session.delete(booking)
            db.session.delete(show)
        db.session.delete(theatre)
        db.session.commit()

        return jsonify({'message': 'Theatre, associated shows, and bookings deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while deleting the theatre, associated shows, and bookings'}), 500

