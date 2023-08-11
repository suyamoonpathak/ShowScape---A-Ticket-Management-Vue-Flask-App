from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from os import path
from .secrets import DATABASE_PATH, JWT_SECRET, STRIPE_SECRET_KEY, MAILTRAP_USERNAME, MAILTRAP_PASSWORD
import stripe
from flask_mail import Mail, Message
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta
from celery import Celery
import redis
import asyncio
import os
import csv

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = JWT_SECRET

celery = Celery(app.name, broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
celery.conf.update(app.config)
redis_client=redis.Redis(host='localhost',port=6379, db=0)

UPLOAD_FOLDER = path.join(path.dirname(
    path.realpath(__file__)), 'static/images/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
jwt = JWTManager(app)
stripe.api_key = STRIPE_SECRET_KEY

from .authentication import authentication
from .theatre_management import theatre_management
from .show_management import show_management
from .booking_management import booking_management

app.register_blueprint(authentication, url_prefix="/")
app.register_blueprint(theatre_management, url_prefix="/")
app.register_blueprint(show_management, url_prefix="/")
app.register_blueprint(booking_management,url_prefix="/")

# Set up email configuration
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = MAILTRAP_USERNAME
app.config['MAIL_PASSWORD'] = MAILTRAP_PASSWORD
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

# Create a Flask-Mail instance
mail = Mail(app)


scheduler = APScheduler()

def generate_monthly_report(user_id):
    # Calculate the date range for the previous month
    print(user_id)
    today = datetime.today()
    first_day_of_previous_month = datetime(today.year, today.month - 1, 1)
    last_day_of_previous_month = first_day_of_previous_month.replace(day=28) + timedelta(days=4)
    last_day_of_previous_month = last_day_of_previous_month - timedelta(days=last_day_of_previous_month.day)

    # Query user bookings for the previous month
    bookings = Booking.query.filter(
        Booking.user_id == user_id,
        Booking.date_of_booking.between(first_day_of_previous_month, last_day_of_previous_month)
    ).all()
    print(bookings)
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


    print(booking_list)
    total_price = sum(booking['num_tickets'] * booking['show']['ticket_price'] for booking in booking_list)
    report_html = render_template('monthly_report.html', booking_list=booking_list,total_price=total_price)
    return report_html

from .models import reminder_recipients,all_users
def send_daily_reminders():
    with app.app_context():
        if(len(reminder_recipients())):
            subject = "We miss youuuuu | Showscape"
            body = f"Hey buddy!\n\nDon't forget to catch up with the new shows!\n\nShowscape"
            msg = Message(subject=subject, recipients=reminder_recipients(), body=body, sender="suyamoonpathak@gmail.com")
            try:
                print(msg)
                mail.send(msg)
                print(f"Reminder sent successfully")
            except Exception as e:
                print(f"Error sending reminder: {e}")
        else:
            print("All users have visited the site today!")

def send_entertainment_report():
    with app.app_context():
        subject = "Your Monthly Entertainment Report"
        for user in all_users():
            print(user.email)
            report_html = generate_monthly_report(user.id)
            msg = Message(subject=subject, recipients=[user.email], html=report_html, sender="suyamoonpathak@gmail.com")
            try:
                mail.send(msg)
                print(f"Report sent successfully")
            except Exception as e:
                print(f"Error sending report: {e}")

hour_of_schedule = 22
minute_of_schedule = 52

scheduler.add_job(id="reminder-job", func=send_daily_reminders, trigger='cron', hour=hour_of_schedule, minute=minute_of_schedule)
scheduler.add_job(id="entertainment-report-job", func=send_entertainment_report, trigger='cron', day=11, hour=hour_of_schedule, minute=minute_of_schedule) #need to make it first of every month

scheduler.start()

@app.route('/test',methods=['GET'])
def helloWorld():
    return ("Backend Server running!")

@app.route('/api/export-csv/<int:theatreId>', methods=['GET'])
def export_csv(theatreId):
    try:
        theatre = Theatre.query.filter(Theatre.id == theatreId).first()

        if theatre is None:
            return jsonify({'message': 'Theatre not found'}), 404

        # Get the admin_id from the theatre object
        admin_id = theatre.admin_id

        # Fetch the Admin object using the admin_id
        admin = User.query.get(admin_id)

        if admin is None:
            return jsonify({'message': 'Admin not found'}), 404

        # Get the email address of the admin
        admin_email = admin.email
        current_directory = os.getcwd()
        subdirectory_path = 'backend/static/csv'
        file_path = os.path.join(current_directory, subdirectory_path, f'Theatre_{theatre.id}_Report.csv')

        # Write CSV data to file
        with open(file_path, 'w') as csv_buffer:
            csv_writer = csv.writer(csv_buffer)
            csv_writer.writerow(['Show ID', 'Show Name', 'Show Rating', 'Show Tags', 'Show Duration', 'Show Date', 'Number of Tickets Booked', 'Ticket Price', 'Total Revenue'])
            shows = Show.query.filter(Show.theatre_id == theatreId).all()
            for show in shows:
                bookings = Booking.query.filter_by(show_id=show.id).all()
                num_tickets_booked = sum(booking.num_tickets for booking in bookings)
                total_revenue = num_tickets_booked * show.ticket_price
                csv_writer.writerow([show.id, show.name, show.rating, show.tags, "2", show.date, num_tickets_booked, show.ticket_price, total_revenue])

        # Send the email asynchronously using asyncio and aiohttp
        asyncio.run(send_email_async(admin_email, file_path,theatreId))

        # Create a response with success message
        return jsonify({'message': 'Email sending in progress!'})

    except Exception as e:
        return jsonify({'message': 'Error exporting CSV and sending email: ' + str(e)}), 500

async def send_email_async(recipient_email, file_path, theatreId):
    subject = f'Theatre {theatreId} Report'
    body = 'Please find the attached report for the theatre.'

    message = Message(subject=subject, body=body, recipients=[recipient_email], sender="suyamoonpathak@gmail.com")
    with open(file_path, 'rb') as file:
        message.attach(f'Theatre_{theatreId}_Report.csv', 'text/csv', file.read())

    mail.send(message)



from .models import User, Theatre, Show, Booking
with app.app_context():
    db.create_all()

