"""
Admin Dashboard API Routes
"""

from flask import Blueprint, request, jsonify, render_template
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.models import db, Appointment, Customer, Service, NewsletterSubscriber, ContactMessage, Therapist

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """Get dashboard statistics"""
    # In production, add authentication here

    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Get statistics
    stats = {
        'total_customers': Customer.query.count(),
        'total_appointments': Appointment.query.count(),
        'appointments_today': Appointment.query.filter(
            Appointment.appointment_date == today
        ).count(),
        'appointments_this_week': Appointment.query.filter(
            Appointment.appointment_date >= week_ago
        ).count(),
        'appointments_this_month': Appointment.query.filter(
            Appointment.appointment_date >= month_ago
        ).count(),
        'pending_appointments': Appointment.query.filter_by(status='pending').count(),
        'confirmed_appointments': Appointment.query.filter_by(status='confirmed').count(),
        'newsletter_subscribers': NewsletterSubscriber.query.filter_by(is_active=True).count(),
        'unread_messages': ContactMessage.query.filter_by(status='new').count()
    }

    # Get upcoming appointments (next 7 days)
    upcoming = Appointment.query.filter(
        Appointment.appointment_date >= today,
        Appointment.appointment_date <= today + timedelta(days=7),
        Appointment.status.in_(['pending', 'confirmed'])
    ).order_by(
        Appointment.appointment_date.asc(),
        Appointment.appointment_time.asc()
    ).limit(10).all()

    # Get recent customers
    recent_customers = Customer.query.order_by(
        Customer.created_at.desc()
    ).limit(5).all()

    return jsonify({
        'stats': stats,
        'upcoming_appointments': [apt.to_dict() for apt in upcoming],
        'recent_customers': [cust.to_dict() for cust in recent_customers]
    })


@admin_bp.route('/appointments', methods=['GET'])
def get_all_appointments():
    """Get all appointments with filters"""
    # In production, add authentication here

    # Parse query parameters
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    status = request.args.get('status')
    therapist_id = request.args.get('therapist_id')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    query = Appointment.query

    # Apply filters
    if date_from:
        try:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Appointment.appointment_date >= date_from_obj)
        except ValueError:
            return jsonify({'error': 'Invalid date_from format'}), 400

    if date_to:
        try:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Appointment.appointment_date <= date_to_obj)
        except ValueError:
            return jsonify({'error': 'Invalid date_to format'}), 400

    if status:
        query = query.filter(Appointment.status == status)

    if therapist_id:
        query = query.filter(Appointment.therapist_id == therapist_id)

    # Order and paginate
    query = query.order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'appointments': [apt.to_dict() for apt in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@admin_bp.route('/customers', methods=['GET'])
def get_all_customers():
    """Get all customers"""
    # In production, add authentication here

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)

    pagination = Customer.query.order_by(
        Customer.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'customers': [cust.to_dict() for cust in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@admin_bp.route('/services', methods=['GET', 'POST'])
def manage_services():
    """Get all services or create a new one"""
    # In production, add authentication here

    if request.method == 'GET':
        services = Service.query.all()
        return jsonify({
            'services': [svc.to_dict() for svc in services]
        })

    elif request.method == 'POST':
        data = request.get_json()

        required_fields = ['name', 'duration_minutes', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        try:
            service = Service(
                name=data['name'],
                description=data.get('description', ''),
                duration_minutes=data['duration_minutes'],
                price=data['price'],
                category=data.get('category', ''),
                active=data.get('active', True)
            )

            db.session.add(service)
            db.session.commit()

            return jsonify({
                'message': 'Service created successfully',
                'service': service.to_dict()
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create service: {str(e)}'}), 500


@admin_bp.route('/services/<int:service_id>', methods=['PUT', 'DELETE'])
def update_or_delete_service(service_id):
    """Update or delete a service"""
    # In production, add authentication here

    service = Service.query.get(service_id)

    if not service:
        return jsonify({'error': 'Service not found'}), 404

    if request.method == 'PUT':
        data = request.get_json()

        try:
            if 'name' in data:
                service.name = data['name']
            if 'description' in data:
                service.description = data['description']
            if 'duration_minutes' in data:
                service.duration_minutes = data['duration_minutes']
            if 'price' in data:
                service.price = data['price']
            if 'category' in data:
                service.category = data['category']
            if 'active' in data:
                service.active = data['active']

            db.session.commit()

            return jsonify({
                'message': 'Service updated successfully',
                'service': service.to_dict()
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update service: {str(e)}'}), 500

    elif request.method == 'DELETE':
        try:
            # Soft delete - just deactivate
            service.active = False
            db.session.commit()

            return jsonify({'message': 'Service deactivated successfully'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to delete service: {str(e)}'}), 500
