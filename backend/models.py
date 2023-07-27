from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # To differentiate between admin and normal users
    # Add other user fields as needed

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    place = db.Column(db.String(120), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    # Add other theatre fields as needed

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    tags = db.Column(db.String(120))  # Tags can be stored as a comma-separated string
    ticket_price = db.Column(db.Float, nullable=False)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'), nullable=False)
    theatre = db.relationship('Theatre', backref=db.backref('shows', lazy=True))
    # Add other show fields as needed

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    show = db.relationship('Show', backref=db.backref('bookings', lazy=True))
    num_tickets = db.Column(db.Integer, nullable=False)
    # Add other booking fields as needed
