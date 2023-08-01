from flask import Blueprint, request, jsonify, current_app
from . import db
from .models import Show, Theatre
import uuid
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from sqlalchemy import or_
from . import stripe

show_management = Blueprint('show_management', __name__)

#display all shows
@show_management.route('/api/shows', methods=['GET'])
def get_all_shows():
    try:
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
                'end_time':show.end_time,
                'date':show.date,
                'trailer_url':show.trailer_url,
                'poster':show.poster,
                'available_seats':show.available_seats,
                'theatre_name': show.theatre.name,  # Include theatre name
                'theatre_place': show.theatre.place,  # Include theatre location
            }
            show_data.append(show_info)
        return jsonify(show_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API to get all shows for a theatre
@show_management.route('/api/shows/theatre/<int:theatre_id>', methods=['GET'])
def get_shows_for_theatre(theatre_id):
    # Check if the theatre with given ID exists
    theatre = Theatre.query.get(theatre_id)
    if not theatre:
        return jsonify({'message': 'Theatre with given ID does not exist.'}), 404

    # Get all shows for the theatre
    shows = Show.query.filter_by(theatre_id=theatre_id).all()

    # Serialize the shows data and return as JSON
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
            'end_time':show.end_time,
            'date':show.date,
            'trailer_url':show.trailer_url,
            'poster':show.poster,
            'available_seats':show.available_seats
        })

    return jsonify(shows_data), 200

# API to get a single show by ID
@show_management.route('/api/shows/<int:show_id>', methods=['GET'])
def get_show_by_id(show_id):
    # Check if the show with given ID exists
    show = Show.query.get(show_id)
    if not show:
        return jsonify({'message': 'Show with given ID does not exist.'}), 404

    # Serialize the show data and return as JSON
    show_data = {
        'id': show.id,
        'name': show.name,
        'rating': show.rating,
        'tags': show.tags,
        'ticket_price': show.ticket_price,
        'theatre_id': show.theatre_id,
        'start_time': show.start_time,
        'end_time':show.end_time,
        'date':show.date,
        'trailer_url':show.trailer_url,
        'poster':show.poster,
        'available_seats':show.available_seats
    }

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
    posterImg = request.files.get('poster')  # Get the uploaded file

    theatre = Theatre.query.get(data.get('theatre_id'))
    if not theatre:
        return jsonify({'message': 'Theatre with given ID does not exist.'}), 404
    theatre_id = theatre.id
    available_seats = theatre.capacity


    if not name or not rating or not ticket_price or not theatre_id or not start_time or not end_time or not date or not user_id or not trailer_url or not posterImg:
        return jsonify({'message': 'Name, rating, ticket price, start time, end time, date, trailer url, poster, user id and theatre ID are required.'}), 400

    # Check if the theatre with given ID exists


    # Save the uploaded poster image to the server
    filename = str(uuid.uuid1()) + "_" + secure_filename(posterImg.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    posterImg.save(filepath)

    # Create a new show and save it to the database
    new_show = Show(name=name, rating=rating, tags=tags, ticket_price=ticket_price, theatre_id=theatre_id, start_time=start_time, end_time=end_time, date=date, user_id=user_id, trailer_url=trailer_url, poster=filename,available_seats=available_seats)
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
    start_time=datetime.strptime(data.get('start_time'),'%H:%M')
    end_time=datetime.strptime(data.get('end_time'),'%H:%M')
    date=datetime.strptime(data.get('date'), '%Y-%m-%d')
    user_id=data.get('user_id')
    trailer_url = data.get('trailer_url')
    posterImg = request.files.get('poster')
    available_seats = data.get('available_seats')


    if not name or not rating or not ticket_price or not theatre_id or not start_time or not end_time or not date or not user_id or not trailer_url or not posterImg or not available_seats:
        return jsonify({'message': 'Name, rating, ticket price, start time, end time, date, trailer url, poster, user id and theatre ID are required.'}), 400

    # Check if the show with given ID exists
    show = Show.query.get(show_id)
    if not show:
        return jsonify({'message': 'Show with given ID does not exist.'}), 404

    # Check if the theatre with given ID exists
    if not Theatre.query.filter_by(id=theatre_id).first():
        return jsonify({'message': 'Theatre with given ID does not exist.'}), 404

    filename = str(uuid.uuid1()) + "_" + secure_filename(posterImg.filename)
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    posterImg.save(filepath)

    # Update the show details and save changes to the database
    show.name = name
    show.rating = rating
    show.tags = tags
    show.ticket_price = ticket_price
    show.theatre_id = theatre_id
    show.start_time = start_time
    show.end_time = end_time
    show.date = date
    show.user_id=user_id
    show.trailer_url=trailer_url
    show.poster=filename
    show.available_seats=available_seats
    db.session.commit()

    return jsonify({'message': 'Show updated successfully.'}), 200

# API to delete a show
@show_management.route('/api/shows/<int:show_id>', methods=['DELETE'])
def delete_show(show_id):
    # Check if the show with given ID exists
    show = Show.query.get(show_id)
    if not show:
        return jsonify({'message': 'Show with given ID does not exist.'}), 404

    # Delete the show from the database
    db.session.delete(show)
    db.session.commit()

    return jsonify({'message': 'Show deleted successfully.'}), 200

# API to search shows based on a single query parameter
@show_management.route('/api/shows/search', methods=['GET'])
def search_shows():
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

    # Serialize the shows data and return as JSON
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
            'available_seats':show.available_seats
        })

    return jsonify(shows_data), 200


@show_management.route("/api/checkout", methods=["POST"])
def checkout():
    try:
        data = request.get_json()
        show_id = data["showId"]
        number_of_tickets = data["numberOfTickets"]

        # Fetch the show details from your database based on show_id
        show = fetch_show_from_database(show_id)

        # Calculate the total amount to charge
        amount = show['ticket_price'] * number_of_tickets

        # Create a payment intent using the Stripe API
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),
            currency="usd",  # Replace with your desired currency
        )

        # Send the client secret back to the frontend
        return jsonify({"clientSecret": intent.client_secret})

    except Exception as e:
        print("Error creating payment intent:", str(e))
        return jsonify({"error": "An error occurred while creating the payment intent."}), 500


def fetch_show_from_database(show_id):
    try:
        # Query the database for the Show record with the specified show_id
        show = Show.query.get(show_id)

        if not show:
            # If the show does not exist, return an appropriate response
            return jsonify({'message': 'Show with given ID does not exist.'}), 404

        # Serialize the show data and return as a dictionary
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
        print(show_data)
        return show_data

    except Exception as e:
        # Handle any exceptions that occur during database query or serialization
        # Return an appropriate error response
        return jsonify({'message': 'Error fetching show details.', 'error': str(e)}), 500