from flask import Blueprint, request, jsonify, current_app
from . import db
from .models import Booking, Show, User, Theatre

booking_management = Blueprint('booking_management', __name__)

#to create a new booking
@booking_management.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()

    user_id = data.get('user_id')
    show_id = data.get('show_id')
    num_tickets = data.get('num_tickets')

    if not user_id or not show_id or not num_tickets:
        return jsonify({'error': 'Invalid request. Missing required data.'}), 400

    # Check if the show exists and has enough available seats
    show = Show.query.get(show_id)
    if not show or show.available_seats < num_tickets:
        return jsonify({'error': 'Show not found or not enough available seats.'}), 400

    try:
        # Create a new booking entry
        booking = Booking(user_id=user_id, show_id=show_id, num_tickets=num_tickets)
        db.session.add(booking)

        show.available_seats -= num_tickets

        db.session.commit()

        # Return a success response
        return jsonify({'message': 'Booking created successfully.'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create booking.'}), 500


#to fetch all the bookings made by a specific user
@booking_management.route('/api/users/<int:user_id>/bookings', methods=['GET'])
def get_user_bookings(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Fetch the bookings for the user and include the related show and theatre details
        bookings = Booking.query.filter_by(user_id=user_id).all()

        # Create a list to hold the booking details with show and theatre information
        booking_list = []
        for booking in bookings:
            show = Show.query.get(booking.show_id)
            theatre = Theatre.query.get(show.theatre_id)

            booking_info = {
                'id': booking.id,
                'show': {
                    'id':show.id,
                    'name': show.name,
                    'tags': show.tags,
                    'rating': show.rating,
                    'date': show.date,
                    'start_time': show.start_time,
                    'ticket_price': show.ticket_price,
                    'poster':show.poster
                },
                'theatre': {
                    'name': theatre.name,
                    'place': theatre.place,
                },
                'num_tickets': booking.num_tickets,
            }
            booking_list.append(booking_info)

        return jsonify(booking_list), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500


