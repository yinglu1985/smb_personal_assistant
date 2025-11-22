"""
Shamrock Day Spa - Backend API
Flask application with scheduling, booking, and newsletter functionality
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize Flask app
app = Flask(__name__,
            template_folder='templates',
            static_folder='../.',
            static_url_path='')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration - use /tmp for App Engine (ephemeral but works for demo)
# For production, use Cloud SQL instead
db_path = os.environ.get('DATABASE_PATH', 'spa.db')
if os.environ.get('GAE_ENV', '').startswith('standard'):
    # Running on App Engine
    db_path = '/tmp/spa.db'

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for frontend communication
CORS(app)

# Initialize scheduler for appointment reminders
scheduler = BackgroundScheduler()
scheduler.start()

# Import db from models
from models.models import db, Customer, Appointment, NewsletterSubscriber, Service, ContactMessage, Therapist

# Initialize database with app
db.init_app(app)

# Import routes after db initialization
from routes.appointments import appointments_bp
from routes.newsletter import newsletter_bp
from routes.contact import contact_bp
from routes.admin import admin_bp

# Register blueprints
app.register_blueprint(appointments_bp, url_prefix='/api/appointments')
app.register_blueprint(newsletter_bp, url_prefix='/api/newsletter')
app.register_blueprint(contact_bp, url_prefix='/api/contact')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# Serve frontend
@app.route('/')
def index():
    return app.send_static_file('index.html')

# API health check
@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

# Get available services
@app.route('/api/services', methods=['GET'])
def get_services():
    services = Service.query.filter_by(active=True).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'description': s.description,
        'duration': s.duration_minutes,
        'price': s.price
    } for s in services])

# Get available therapists
@app.route('/api/therapists', methods=['GET'])
def get_therapists():
    therapists = Therapist.query.filter_by(active=True).all()
    return jsonify([t.to_dict() for t in therapists])

# Get available time slots for a specific date
@app.route('/api/appointments/available-slots', methods=['GET'])
def get_available_slots():
    date_str = request.args.get('date')
    service_id = request.args.get('service_id')

    if not date_str:
        return jsonify({'error': 'Date is required'}), 400

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Get service duration
    service = Service.query.get(service_id) if service_id else None
    duration = service.duration_minutes if service else 60

    # Business hours: 9 AM to 8 PM
    available_slots = []
    start_hour = 9
    end_hour = 20

    # Generate time slots
    current_time = datetime.combine(date, datetime.min.time()).replace(hour=start_hour)
    end_time = datetime.combine(date, datetime.min.time()).replace(hour=end_hour)

    while current_time < end_time:
        # Check if slot is available (not booked)
        existing_appointment = Appointment.query.filter(
            Appointment.appointment_date == date,
            Appointment.appointment_time == current_time.time(),
            Appointment.status.in_(['confirmed', 'pending'])
        ).first()

        if not existing_appointment:
            available_slots.append({
                'time': current_time.strftime('%H:%M'),
                'display': current_time.strftime('%I:%M %p')
            })

        current_time += timedelta(minutes=30)  # 30-minute intervals

    return jsonify({
        'date': date_str,
        'slots': available_slots
    })

# Initialize database with default services
def init_db():
    with app.app_context():
        db.create_all()

        # Add default services if none exist
        if Service.query.count() == 0:
            default_services = [
                # Massage Services
                Service(name='Swedish Massage (30 min)', description='Relaxing full-body Swedish massage', duration_minutes=30, price=50.00, category='massage'),
                Service(name='Swedish Massage (60 min)', description='Relaxing full-body Swedish massage', duration_minutes=60, price=70.00, category='massage'),
                Service(name='Swedish Massage (90 min)', description='Relaxing full-body Swedish massage', duration_minutes=90, price=100.00, category='massage'),
                Service(name='Deep Tissue Massage (30 min)', description='Therapeutic deep pressure massage', duration_minutes=30, price=55.00, category='massage'),
                Service(name='Deep Tissue Massage (60 min)', description='Therapeutic deep pressure massage', duration_minutes=60, price=75.00, category='massage'),
                Service(name='Deep Tissue Massage (90 min)', description='Therapeutic deep pressure massage', duration_minutes=90, price=105.00, category='massage'),
                Service(name='Hot Stone Massage (60 min)', description='Massage with heated stones', duration_minutes=60, price=80.00, category='massage'),
                Service(name='Hot Stone Massage (90 min)', description='Massage with heated stones', duration_minutes=90, price=110.00, category='massage'),
                Service(name='Body Scrub Massage (60 min)', description='Exfoliating body scrub with massage', duration_minutes=60, price=80.00, category='massage'),
                Service(name='Body Scrub Massage (90 min)', description='Exfoliating body scrub with massage', duration_minutes=90, price=100.00, category='massage'),
                # Facial Services
                Service(name='Mini Facial', description='Quick refreshing facial treatment', duration_minutes=30, price=40.00, category='facial'),
                Service(name='Basic Facial', description='Classic cleansing and rejuvenating facial', duration_minutes=60, price=80.00, category='facial'),
                Service(name='Deluxe Facial', description='Comprehensive luxury facial treatment', duration_minutes=90, price=120.00, category='facial'),
                # Special Packages
                Service(name='Special Combo (Mini Facial + Swedish 60min)', description='Mini facial combined with 60-minute Swedish massage', duration_minutes=90, price=89.00, category='package'),
            ]

            for service in default_services:
                db.session.add(service)

            db.session.commit()
            print("✓ Default services added to database")

        # Add default therapists if none exist
        if Therapist.query.count() == 0:
            default_therapists = [
                Therapist(name='Lily', specialty='Swedish & Deep Tissue Massage', bio='Certified massage therapist with 8+ years experience specializing in relaxation and therapeutic techniques.'),
                Therapist(name='Wendy', specialty='Hot Stone & Body Treatments', bio='Expert in hot stone therapy and body scrubs. Known for her gentle, healing touch.'),
                Therapist(name='Elaine', specialty='All Massage Types', bio='Versatile therapist skilled in all massage modalities. Great for first-time spa guests.'),
            ]

            for therapist in default_therapists:
                db.session.add(therapist)

            db.session.commit()
            print("✓ Default therapists added to database")

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    init_db()
    print("=" * 50)
    print("🌿 Shamrock Day Spa Backend Starting...")
    print("=" * 50)
    print("📍 Server: http://localhost:5001")
    print("📍 Frontend: http://localhost:5001")
    print("📍 API Docs: http://localhost:5001/api/health")
    print("=" * 50)
    app.run(debug=True, port=5001, host='0.0.0.0')
