from flask import Blueprint, request, jsonify
from . import db
from .models import Show, Theatre

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
                'date':show.date
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
            'date':show.date
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
        'date':show.date
    }

    return jsonify(show_data), 200

# API to create a new show
from datetime import datetime
@show_management.route('/api/shows', methods=['POST'])
def create_show():
    data = request.get_json()
    name = data.get('name')
    rating = data.get('rating')
    tags = data.get('tags')
    ticket_price = data.get('ticket_price')
    theatre_id = data.get('theatre_id')
    start_time=datetime.strptime(data.get('start_time'),'%H:%M')
    end_time=datetime.strptime(data.get('end_time'),'%H:%M')
    date=datetime.strptime(data.get('date'), '%Y-%m-%d')
    user_id=data.get('user_id')

    if not name or not rating or not ticket_price or not theatre_id or not start_time or not end_time or not date or not user_id:
        return jsonify({'message': 'Name, rating, ticket price, start time, end time, date, user id and theatre ID are required.'}), 400

    # Check if the theatre with given ID exists
    if not Theatre.query.filter_by(id=theatre_id).first():
        return jsonify({'message': 'Theatre with given ID does not exist.'}), 404

    # Create a new show and save it to the database
    new_show = Show(name=name, rating=rating, tags=tags, ticket_price=ticket_price, theatre_id=theatre_id, start_time=start_time, end_time=end_time, date=date, user_id=user_id)
    db.session.add(new_show)
    db.session.commit()

    return jsonify({'message': 'Show created successfully.', 'show_id': new_show.id}), 201

# API to update an existing show
@show_management.route('/api/shows/<int:show_id>', methods=['PUT'])
def update_show(show_id):
    data = request.get_json()
    name = data.get('name')
    rating = data.get('rating')
    tags = data.get('tags')
    ticket_price = data.get('ticket_price')
    theatre_id = data.get('theatre_id')
    start_time=datetime.strptime(data.get('start_time'),'%H:%M')
    end_time=datetime.strptime(data.get('end_time'),'%H:%M')
    date=datetime.strptime(data.get('date'), '%Y-%m-%d')
    user_id=data.get('user_id')

    if not name or not rating or not ticket_price or not theatre_id:
        return jsonify({'message': 'Name, rating, ticket price, user id and theatre ID are required.'}), 400

    # Check if the show with given ID exists
    show = Show.query.get(show_id)
    if not show:
        return jsonify({'message': 'Show with given ID does not exist.'}), 404

    # Check if the theatre with given ID exists
    if not Theatre.query.filter_by(id=theatre_id).first():
        return jsonify({'message': 'Theatre with given ID does not exist.'}), 404

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
