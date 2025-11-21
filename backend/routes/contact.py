"""
Contact Form API Routes
"""

from flask import Blueprint, request, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.models import db, ContactMessage
from utils.email_service import send_contact_notification

contact_bp = Blueprint('contact', __name__)


@contact_bp.route('/submit', methods=['POST'])
def submit_contact():
    """Submit a contact form message"""
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'email', 'message']
    for field in required_fields:
        if field not in data or not data[field].strip():
            return jsonify({'error': f'Missing required field: {field}'}), 400

    try:
        # Create contact message
        message = ContactMessage(
            name=data['name'].strip(),
            email=data['email'].strip().lower(),
            phone=data.get('phone', '').strip(),
            subject=data.get('subject', 'General Inquiry').strip(),
            message=data['message'].strip(),
            status='new'
        )

        db.session.add(message)
        db.session.commit()

        # Send notification email to spa
        try:
            send_contact_notification(message)
        except Exception as e:
            print(f"Warning: Could not send notification email: {e}")

        return jsonify({
            'message': 'Thank you for contacting us! We will respond shortly.',
            'message_id': message.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to submit message: {str(e)}'}), 500


@contact_bp.route('/messages', methods=['GET'])
def get_messages():
    """Get all contact messages (admin only)"""
    # In production, add authentication here
    status = request.args.get('status', None)

    if status:
        messages = ContactMessage.query.filter_by(status=status).order_by(
            ContactMessage.created_at.desc()
        ).all()
    else:
        messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()

    return jsonify({
        'count': len(messages),
        'messages': [msg.to_dict() for msg in messages]
    })


@contact_bp.route('/messages/<int:message_id>', methods=['PUT'])
def update_message_status(message_id):
    """Update contact message status (admin only)"""
    # In production, add authentication here
    message = ContactMessage.query.get(message_id)

    if not message:
        return jsonify({'error': 'Message not found'}), 404

    data = request.get_json()

    if 'status' in data and data['status'] in ['new', 'read', 'responded']:
        message.status = data['status']
        db.session.commit()

        return jsonify({
            'message': 'Status updated successfully',
            'contact_message': message.to_dict()
        })

    return jsonify({'error': 'Invalid status'}), 400
