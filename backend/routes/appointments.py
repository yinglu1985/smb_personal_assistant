"""
Appointment Booking API Routes
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import sys
import os
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.models import db, Appointment, Customer, Service, Therapist
from utils.email_service import send_appointment_confirmation, send_admin_booking_notification

appointments_bp = Blueprint('appointments', __name__)


@appointments_bp.route('', methods=['POST'])
def create_appointment():
    """Create a new appointment"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['first_name', 'last_name', 'email', 'phone', 'service_id', 'date', 'time']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    try:
        # Parse date and time
        appointment_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        appointment_time = datetime.strptime(data['time'], '%H:%M').time()

        # Check if appointment time is in the past
        appointment_datetime = datetime.combine(appointment_date, appointment_time)
        if appointment_datetime < datetime.now():
            return jsonify({'error': 'Cannot book appointments in the past'}), 400

        # Check if service exists
        service = Service.query.get(data['service_id'])
        if not service or not service.active:
            return jsonify({'error': 'Invalid service selected'}), 400

        # Validate therapist if provided
        therapist_id = data.get('therapist_id')
        therapist = None
        if therapist_id:
            therapist = Therapist.query.get(therapist_id)
            if not therapist or not therapist.active:
                return jsonify({'error': 'Invalid therapist selected'}), 400

        # Check if time slot is available
        # If therapist is selected, check their availability specifically
        # Otherwise, check general availability
        if therapist_id:
            existing_appointment = Appointment.query.filter(
                Appointment.therapist_id == therapist_id,
                Appointment.appointment_date == appointment_date,
                Appointment.appointment_time == appointment_time,
                Appointment.status.in_(['confirmed', 'pending'])
            ).first()

            if existing_appointment:
                return jsonify({'error': f'{therapist.name} is not available at this time'}), 409
        else:
            existing_appointment = Appointment.query.filter(
                Appointment.appointment_date == appointment_date,
                Appointment.appointment_time == appointment_time,
                Appointment.status.in_(['confirmed', 'pending'])
            ).first()

            if existing_appointment:
                return jsonify({'error': 'This time slot is no longer available'}), 409

        # Find or create customer
        customer = Customer.query.filter_by(email=data['email'].lower()).first()

        if not customer:
            customer = Customer(
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'].lower(),
                phone=data['phone']
            )
            db.session.add(customer)
            db.session.flush()  # Get customer ID without committing

        # Create appointment
        appointment = Appointment(
            customer_id=customer.id,
            service_id=service.id,
            therapist_id=therapist_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status='pending',
            notes=data.get('notes', '')
        )

        db.session.add(appointment)
        db.session.commit()

        # Get the response data before starting background thread
        response_data = {
            'message': 'Appointment booked successfully!',
            'appointment': appointment.to_dict()
        }

        # Send emails asynchronously in background to avoid blocking the response
        # Pass only IDs to background thread (not DB objects)
        app = current_app._get_current_object()
        customer_id = customer.id
        appointment_id = appointment.id
        service_id = service.id

        def send_emails_async():
            with app.app_context():
                try:
                    # Query objects fresh in this thread
                    customer_obj = Customer.query.get(customer_id)
                    appointment_obj = Appointment.query.get(appointment_id)
                    service_obj = Service.query.get(service_id)

                    if customer_obj and appointment_obj and service_obj:
                        send_appointment_confirmation(customer_obj, appointment_obj, service_obj)
                        send_admin_booking_notification(customer_obj, appointment_obj, service_obj)
                except Exception as e:
                    print(f"Warning: Could not send emails: {e}")

        # Start email sending in background thread
        email_thread = threading.Thread(target=send_emails_async, daemon=True)
        email_thread.start()

        return jsonify(response_data), 201

    except ValueError as e:
        return jsonify({'error': f'Invalid date/time format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create appointment: {str(e)}'}), 500


@appointments_bp.route('/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """Get appointment details"""
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    return jsonify(appointment.to_dict())


@appointments_bp.route('/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    """Update an existing appointment"""
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    data = request.get_json()

    try:
        # Update allowed fields
        if 'date' in data:
            appointment.appointment_date = datetime.strptime(data['date'], '%Y-%m-%d').date()

        if 'time' in data:
            appointment.appointment_time = datetime.strptime(data['time'], '%H:%M').time()

        if 'status' in data:
            if data['status'] in ['pending', 'confirmed', 'completed', 'cancelled', 'no-show']:
                appointment.status = data['status']

        if 'notes' in data:
            appointment.notes = data['notes']

        db.session.commit()

        return jsonify({
            'message': 'Appointment updated successfully',
            'appointment': appointment.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update appointment: {str(e)}'}), 500


@appointments_bp.route('/<int:appointment_id>', methods=['DELETE'])
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    try:
        appointment.status = 'cancelled'
        db.session.commit()

        return jsonify({'message': 'Appointment cancelled successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to cancel appointment: {str(e)}'}), 500


@appointments_bp.route('/customer/<email>', methods=['GET'])
def get_customer_appointments(email):
    """Get all appointments for a customer by email"""
    customer = Customer.query.filter_by(email=email.lower()).first()

    if not customer:
        return jsonify({'appointments': []})

    appointments = Appointment.query.filter_by(customer_id=customer.id).order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()

    return jsonify({
        'customer': customer.to_dict(),
        'appointments': [apt.to_dict() for apt in appointments]
    })
