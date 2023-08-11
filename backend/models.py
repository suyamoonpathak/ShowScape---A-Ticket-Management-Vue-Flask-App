from . import db
from datetime import date

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # To differentiate between admin and normal users
    last_visit = db.Column(db.DateTime)
    theatres=db.relationship('Theatre', backref='user', passive_deletes=True, lazy=True)
    shows=db.relationship('Show', backref='user', passive_deletes=True, lazy=True)
    bookings=db.relationship('Booking', backref='user', passive_deletes=True, lazy=True)

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    place = db.Column(db.String(120), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"), nullable=False)  # New foreign key to link theatre with admin
    shows=db.relationship('Show', backref='theatre', passive_deletes=True, lazy=True)

    def as_dict(self):
        return {
        'id': self.id,
        'name': self.name,
        'place': self.place,
        'capacity': self.capacity,
        'admin_id':self.admin_id
    }

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    tags = db.Column(db.String(120))  # Tags can be stored as a comma-separated string
    ticket_price = db.Column(db.Float, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    poster = db.Column(db.String(200))  # URL or file path of the picture
    trailer_url = db.Column(db.String(200))  # URL of the trailer video
    available_seats = db.Column(db.Integer, nullable=False)
    booking = db.relationship('Booking', backref='show', passive_deletes=True, lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id', ondelete='CASCADE'), nullable=False)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id', ondelete="CASCADE"), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    date_of_booking = db.Column(db.DateTime, nullable=False)

def reminder_recipients():
    today = date.today()
    users_to_notify = User.query.filter(User.last_visit < today).all()
    recipients=[]
    for user in users_to_notify:
        recipients.append(user.email)
    return recipients

def all_users():
    users = User.query.filter(User.is_admin == 0).all()
    print(users)
    return users