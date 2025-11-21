"""
Newsletter Subscription API Routes
"""

from flask import Blueprint, request, jsonify
import sys
import os
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.models import db, NewsletterSubscriber
from utils.email_service import send_newsletter_welcome

newsletter_bp = Blueprint('newsletter', __name__)


def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@newsletter_bp.route('/subscribe', methods=['POST'])
def subscribe():
    """Subscribe to newsletter"""
    data = request.get_json()

    if not data or 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400

    email = data['email'].strip().lower()

    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    try:
        # Check if already subscribed
        existing_subscriber = NewsletterSubscriber.query.filter_by(email=email).first()

        if existing_subscriber:
            if existing_subscriber.is_active:
                return jsonify({'message': 'You are already subscribed to our newsletter'}), 200
            else:
                # Reactivate subscription
                existing_subscriber.is_active = True
                existing_subscriber.unsubscribed_at = None
                db.session.commit()

                return jsonify({'message': 'Welcome back! Your subscription has been reactivated'}), 200

        # Create new subscriber
        subscriber = NewsletterSubscriber(email=email)
        db.session.add(subscriber)
        db.session.commit()

        # Send welcome email
        try:
            send_newsletter_welcome(email)
        except Exception as e:
            print(f"Warning: Could not send welcome email: {e}")

        return jsonify({
            'message': 'Thank you for subscribing! Check your email for confirmation.',
            'subscriber_id': subscriber.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to subscribe: {str(e)}'}), 500


@newsletter_bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """Unsubscribe from newsletter"""
    data = request.get_json()

    if not data or 'email' not in data:
        return jsonify({'error': 'Email is required'}), 400

    email = data['email'].strip().lower()

    try:
        subscriber = NewsletterSubscriber.query.filter_by(email=email).first()

        if not subscriber:
            return jsonify({'error': 'Email not found in our subscriber list'}), 404

        if not subscriber.is_active:
            return jsonify({'message': 'You are already unsubscribed'}), 200

        # Deactivate subscription
        from datetime import datetime
        subscriber.is_active = False
        subscriber.unsubscribed_at = datetime.utcnow()
        db.session.commit()

        return jsonify({'message': 'You have been successfully unsubscribed'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to unsubscribe: {str(e)}'}), 500


@newsletter_bp.route('/subscribers', methods=['GET'])
def get_subscribers():
    """Get all active subscribers (admin only)"""
    # In production, add authentication here
    subscribers = NewsletterSubscriber.query.filter_by(is_active=True).all()

    return jsonify({
        'count': len(subscribers),
        'subscribers': [s.to_dict() for s in subscribers]
    })
