import json
from flask import Blueprint, request, jsonify, current_app
from . import db, redis_client
from .models import Show, Theatre, Booking
import uuid
from werkzeug.utils import secure_filename
import os
from datetime import datetime, date
from sqlalchemy import or_
from . import stripe

show_management = Blueprint('show_management', __name__)

@show_management.route('/api/shows', methods=['GET'])
def get_all_shows():
    try:
        cached_data = redis_client.get('all_shows')
        if cached_data:
            return cached_data, 200

        shows = Show.query.all()
        show_data = []
        for show in shows:
            show_info = {
                'id': show.id,
                'name': show.name,
                'rating': show.rating,
                'tags': show.tags,
                'ticket_price': show.ticket_price,
                'theatre_id': show.theatre_id,
                'start_time': show.start_time,
                'end_time': show.end_time,
                'date': show.date,
                'trailer_url': show.trailer_url,
                'poster': show.poster,
                'available_seats': show.available_seats,
                'theatre_name': show.theatre.name,
                'theatre_place': show.theatre.place,
            }
            show_data.append(show_info)

        show_data_json = jsonify(show_data)
        redis_client.setex('all_shows', 10, show_data_json.data)

        return show_data_json, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


#Get all shows
@show_management.route('/api/shows/theatre/<int:theatre_id>', methods=['GET'])
def get_shows_for_theatre(theatre_id):
    try:
        cached_data = redis_client.get(f'shows_for_theatre_{theatre_id}')
        if cached_data:
            return cached_data, 200

        theatre = Theatre.query.get(theatre_id)
        if not theatre:
            return jsonify({'message': 'Theatre with given ID does not exist.'}), 404

        shows = Show.query.filter_by(theatre_id=theatre_id).all()

        shows_data = []
        for show in shows:
            shows_data.append({
                'id': show.id,
                'name': show.name,
                'rating': show.rating,
                'tags': show.tags,
                'ticket_price': show.ticket_price,
                'theatre_id': show.theatre_id,
                'start_time': show.start_time,
                'end_time': show.end_time,
                'date': show.date,
                'trailer_url': show.trailer_url,
                'poster': show.poster,
                'available_seats': show.available_seats
            })

        shows_data_json = jsonify(shows_data)
        redis_client.setex(f'shows_for_theatre_{theatre_id}', 10, shows_data_json.data)

        return shows_data_json, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API to get a single show by ID
@show_management.route('/api/shows/<int:show_id>', methods=['GET'])
def get_show_by_id(show_id):
    cached_data = redis_client.get(f'show_{show_id}')
    if cached_data:
        return cached_data,200
    
    show = Show.query.get(show_id)
    if not show:
        return jsonify({'message': 'Show with given ID does not exist.'}), 404

    show_data = {
        'id': show.id,
        'name': show.name,
        'rating': show.rating,
        'tags': show.tags,
        'ticket_price': show.ticket_price,
        'theatre_id': show.theatre_id,
        'start_time': show.start_time,
        'end_time': show.end_time,
        'date': show.date,
        'trailer_url': show.trailer_url,
        'poster': show.poster,
        'available_seats': show.available_seats
    }
    show_data_json = jsonify(show_data)
    redis_client.setex(f'show_{show_id}', 10, show_data_json.data)

    return jsonify(show_data), 200


def saveImg(file, fileName):
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], fileName))

# API to create a new show
@show_management.route('/api/shows', methods=['POST'])
def create_show():
    data = request.form
    name = data.get('name')
    rating = data.get('rating')
    tags = data.get('tags')
    ticket_price = data.get('ticket_price')
    start_time = datetime.strptime(data.get('start_time'), '%H:%M')
    end_time = datetime.strptime(data.get('end_time'), '%H:%M')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d')
    user_id = data.get('user_id')
    trailer_url = data.get('trailer_url')
    posterImg = request.files.get('poster')

    theatre = Theatre.query.get(data.get('theatre_id'))
    if not theatre:
        return jsonify({'message': 'Theatre with given ID does not exist.'}), 404
    theatre_id = theatre.id
    available_seats = theatre.capacity

    if not name or not rating or not ticket_price or not theatre_id or not start_time or not end_time or not date or not user_id or not trailer_url or not posterImg:
        return jsonify({'message': 'Name, rating, ticket price, start time, end time, date, trailer url, poster, user id and theatre ID are required.'}), 400

    # Save the uploaded poster image to the server
    filename = str(uuid.uuid1()) + "_" + secure_filename(posterImg.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    posterImg.save(filepath)

    new_show = Show(name=name, rating=rating, tags=tags, ticket_price=ticket_price, theatre_id=theatre_id, start_time=start_time,
                    end_time=end_time, date=date, user_id=user_id, trailer_url=trailer_url, poster=filename, available_seats=available_seats)
    db.session.add(new_show)
    db.session.commit()

    return jsonify({'message': 'Show created successfully.', 'show_id': new_show.id}), 201

# API to update an existing show
@show_management.route('/api/shows/<int:show_id>', methods=['PUT'])
def update_show(show_id):
    data = request.form
    name = data.get('name')
    rating = data.get('rating')
    tags = data.get('tags')
    ticket_price = data.get('ticket_price')
    theatre_id = data.get('theatre_id')
    start_time = datetime.strptime(data.get('start_time'), '%H:%M')
    end_time = datetime.strptime(data.get('end_time'), '%H:%M')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d')
    user_id = data.get('user_id')
    trailer_url = data.get('trailer_url')
    posterImg = request.files.get('poster')

    if not name or not rating or not ticket_price or not theatre_id or not start_time or not end_time or not date or not user_id or not trailer_url:
        return jsonify({'message': 'Name, rating, ticket price, start time, end time, date, trailer url, poster, user id and theatre ID are required.'}), 400

    show = Show.query.get(show_id)
    if not show:
        return jsonify({'message': 'Show with given ID does not exist.'}), 404

    if not Theatre.query.filter_by(id=theatre_id).first():
        return jsonify({'message': 'Theatre with given ID does not exist.'}), 404
    
    if posterImg:
        filename = str(uuid.uuid1()) + "_" + secure_filename(posterImg.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        posterImg.save(filepath)
        show.poster = filename

    show.name = name
    show.rating = rating
    show.tags = tags
    show.ticket_price = ticket_price
    show.theatre_id = theatre_id
    show.start_time = start_time
    show.end_time = end_time
    show.date = date
    show.user_id = user_id
    show.trailer_url = trailer_url
    db.session.commit()

    return jsonify({'message': 'Show updated successfully.'}), 200

# API to delete a show
@show_management.route('/api/shows/<int:show_id>', methods=['DELETE'])
def delete_show(show_id):
    show = Show.query.get(show_id)
    if not show:
        return jsonify({'message': 'Show with given ID does not exist.'}), 404

    bookings = Booking.query.filter_by(show_id=show_id).all()

    for booking in bookings:
        db.session.delete(booking)

    db.session.delete(show)
    db.session.commit()

    return jsonify({'message': 'Show deleted successfully.'}), 200

# API to search shows based on a single query parameter
@show_management.route('/api/shows/search', methods=['GET'])
def search_shows():
    cached_data = redis_client.get('search_results')
    if cached_data:
        return cached_data,200

    # Get the search query from query parameters
    search_query = request.args.get('q')

    # Perform a database query to filter shows based on the search query
    shows = Show.query.filter(
        or_(
            Show.name.ilike(f'%{search_query}%'),
            Show.tags.ilike(f'%{search_query}%'),
            Show.theatre.has(Theatre.name.ilike(f'%{search_query}%')),
            Show.theatre.has(Theatre.place.ilike(f'%{search_query}%')),
        )
    ).all()

    shows_data = []
    for show in shows:
        shows_data.append({
            'id': show.id,
            'name': show.name,
            'rating': show.rating,
            'tags': show.tags,
            'ticket_price': show.ticket_price,
            'theatre_id': show.theatre_id,
            'start_time': show.start_time,
            'end_time': show.end_time,
            'date': show.date,
            'trailer_url': show.trailer_url,
            'poster': show.poster,
            'available_seats': show.available_seats
        })

    search_results_json = jsonify(shows_data)
    redis_client.setex('search_results',10,search_results_json.data)

    return jsonify(shows_data), 200


@show_management.route("/api/checkout", methods=["POST"])
def stripeCheckout():
    data = request.get_json()
    user_id = data.get('user_id')
    show_name = data.get('show_name')
    ticket_price = str(round(data.get('ticket_price')*100,2))
    num_tickets = data.get('num_tickets')
    show_id = data.get('show_id')

    
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'unit_amount_decimal': ticket_price,
                'currency': 'usd',
                'product_data': {
                    'name': show_name
                },
            },
            'quantity': num_tickets,
        },
        ],
        mode='payment',
        success_url='http://localhost:8080/booking-success',
        cancel_url='http://localhost:8080/booking-failed',
        metadata={
            'user_id':user_id,
            'show_name':show_name,
            'ticket_price':ticket_price,
            'num_tickets':num_tickets,
            'show_id':show_id
        }
    )
    return jsonify({"sessionId":session['id'],"metadata":session.metadata}),200

# Endpoint to handle Stripe webhook events
@show_management.route("/api/webhooks/stripe", methods=["POST"])
def handle_stripe_webhook():
    payload = request.data
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return jsonify({"error": "Invalid payload"}), 400

    if event.type == "checkout.session.completed":
        # A payment has been successfully completed
        session = event.data.object
        user_id = int(session.metadata.get("user_id"))
        show_id = int(session.metadata.get("show_id"))
        num_tickets = int(session.metadata.get("num_tickets"))

        # Create the booking and update available_tickets
        create_and_update_booking(user_id, show_id, num_tickets)

    return jsonify({"status": "success"}), 200

def create_and_update_booking(user_id, show_id, num_tickets):
    try:
        booking = Booking(user_id=user_id, show_id=show_id, num_tickets=num_tickets, date_of_booking=date.today())
        db.session.add(booking)

        show = Show.query.get(show_id)
        show.available_seats -= num_tickets

        db.session.commit()

    except Exception as e:
        db.session.rollback()