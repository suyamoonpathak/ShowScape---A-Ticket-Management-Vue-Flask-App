from flask import Blueprint, request, jsonify, current_app
from . import db
from .models import Booking, Show, User, Theatre

booking_management = Blueprint('booking_management', __name__)

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
        return jsonify({'error': e.name}), 500


