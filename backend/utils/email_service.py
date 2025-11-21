"""
Email Service for sending notifications
"""

import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Email configuration (from environment variables)
SMTP_HOST = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
FROM_EMAIL = os.environ.get('FROM_EMAIL', 'noreply@shamrockspa.com')
FROM_NAME = os.environ.get('FROM_NAME', 'Shamrock Day Spa')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@shamrockspa.com')


def send_email(to_email, subject, html_content, text_content=None):
    """
    Send an email using SMTP

    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML version of the email
        text_content: Plain text version (optional)
    """

    # Skip if no SMTP credentials configured
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        print(f"📧 Email would be sent to {to_email}")
        print(f"   Subject: {subject}")
        print(f"   (SMTP not configured - set environment variables to enable email)")
        return True

    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f'{FROM_NAME} <{FROM_EMAIL}>'
        msg['To'] = to_email
        msg['Subject'] = subject

        # Add plain text and HTML parts
        if text_content:
            part1 = MIMEText(text_content, 'plain')
            msg.attach(part1)

        part2 = MIMEText(html_content, 'html')
        msg.attach(part2)

        # Send email
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        print(f"✓ Email sent successfully to {to_email}")
        return True

    except Exception as e:
        print(f"✗ Failed to send email to {to_email}: {str(e)}")
        return False


def send_appointment_confirmation(customer, appointment, service):
    """Send appointment confirmation email to customer"""

    appointment_datetime = datetime.combine(
        appointment.appointment_date,
        appointment.appointment_time
    )

    subject = f"Appointment Confirmation - {service.name}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #1B5971; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background: #f9f9f9; }}
            .details {{ background: white; padding: 15px; margin: 20px 0; border-left: 4px solid #FBBD48; }}
            .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
            .button {{ background: #FBBD48; color: #333; padding: 12px 30px; text-decoration: none; display: inline-block; margin: 10px 0; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌿 Shamrock Day Spa</h1>
                <p>Your Wellness Sanctuary</p>
            </div>
            <div class="content">
                <h2>Appointment Confirmed!</h2>
                <p>Dear {customer.first_name},</p>
                <p>Thank you for booking with Shamrock Day Spa. Your appointment has been confirmed.</p>

                <div class="details">
                    <h3>Appointment Details:</h3>
                    <p><strong>Service:</strong> {service.name}</p>
                    <p><strong>Date:</strong> {appointment_datetime.strftime('%A, %B %d, %Y')}</p>
                    <p><strong>Time:</strong> {appointment_datetime.strftime('%I:%M %p')}</p>
                    <p><strong>Duration:</strong> {service.duration_minutes} minutes</p>
                    <p><strong>Price:</strong> ${service.price:.2f}</p>
                </div>

                <p><strong>What to bring:</strong></p>
                <ul>
                    <li>Please arrive 10 minutes early</li>
                    <li>Comfortable clothing recommended</li>
                    <li>Inform us of any allergies or health concerns</li>
                </ul>

                <p><strong>Location:</strong><br>
                123 Wellness Avenue, Suite 100<br>
                Your City, ST 12345<br>
                Phone: (555) 123-4567</p>

                <p>If you need to reschedule or cancel, please contact us at least 24 hours in advance.</p>

                <p>We look forward to seeing you!</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 Shamrock Day Spa. All rights reserved.</p>
                <p>123 Wellness Avenue, Suite 100 | (555) 123-4567 | info@shamrockspa.com</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
    Shamrock Day Spa - Appointment Confirmation

    Dear {customer.first_name},

    Thank you for booking with Shamrock Day Spa. Your appointment has been confirmed.

    Appointment Details:
    Service: {service.name}
    Date: {appointment_datetime.strftime('%A, %B %d, %Y')}
    Time: {appointment_datetime.strftime('%I:%M %p')}
    Duration: {service.duration_minutes} minutes
    Price: ${service.price:.2f}

    Location:
    123 Wellness Avenue, Suite 100
    Your City, ST 12345
    Phone: (555) 123-4567

    Please arrive 10 minutes early.

    If you need to reschedule or cancel, please contact us at least 24 hours in advance.

    We look forward to seeing you!

    Shamrock Day Spa
    """

    return send_email(customer.email, subject, html_content, text_content)


def send_newsletter_welcome(email):
    """Send welcome email to new newsletter subscriber"""

    subject = "Welcome to Shamrock Day Spa Newsletter!"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #1B5971; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background: #f9f9f9; }}
            .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌿 Welcome to Shamrock Day Spa!</h1>
            </div>
            <div class="content">
                <p>Thank you for subscribing to our newsletter!</p>
                <p>You'll now receive:</p>
                <ul>
                    <li>✨ Exclusive special offers and promotions</li>
                    <li>💆 Wellness tips and self-care advice</li>
                    <li>📅 Updates on new services</li>
                    <li>🎁 Birthday surprises</li>
                </ul>
                <p>Stay tuned for your first newsletter coming soon!</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 Shamrock Day Spa. All rights reserved.</p>
                <p><a href="#">Unsubscribe</a></p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = """
    Welcome to Shamrock Day Spa Newsletter!

    Thank you for subscribing! You'll now receive exclusive special offers,
    wellness tips, updates on new services, and birthday surprises.

    Stay tuned for your first newsletter coming soon!

    Shamrock Day Spa
    """

    return send_email(email, subject, html_content, text_content)


def send_contact_notification(contact_message):
    """Send notification to admin about new contact message"""

    subject = f"New Contact Message from {contact_message.name}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #1B5971; color: white; padding: 20px; }}
            .content {{ padding: 20px; background: #f9f9f9; }}
            .message-box {{ background: white; padding: 15px; margin: 20px 0; border-left: 4px solid #FBBD48; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>New Contact Form Submission</h2>
            </div>
            <div class="content">
                <p><strong>From:</strong> {contact_message.name}</p>
                <p><strong>Email:</strong> {contact_message.email}</p>
                <p><strong>Phone:</strong> {contact_message.phone or 'Not provided'}</p>
                <p><strong>Subject:</strong> {contact_message.subject}</p>

                <div class="message-box">
                    <h3>Message:</h3>
                    <p>{contact_message.message}</p>
                </div>

                <p><strong>Received:</strong> {contact_message.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
    New Contact Form Submission

    From: {contact_message.name}
    Email: {contact_message.email}
    Phone: {contact_message.phone or 'Not provided'}
    Subject: {contact_message.subject}

    Message:
    {contact_message.message}

    Received: {contact_message.created_at.strftime('%B %d, %Y at %I:%M %p')}
    """

    return send_email(ADMIN_EMAIL, subject, html_content, text_content)


def send_appointment_reminder(customer, appointment, service):
    """Send appointment reminder email (24 hours before)"""

    appointment_datetime = datetime.combine(
        appointment.appointment_date,
        appointment.appointment_time
    )

    subject = f"Reminder: Your appointment tomorrow at {appointment_datetime.strftime('%I:%M %p')}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #1B5971; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; background: #f9f9f9; }}
            .reminder-box {{ background: #FFF9E6; padding: 15px; margin: 20px 0; border-left: 4px solid #FBBD48; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌿 Appointment Reminder</h1>
            </div>
            <div class="content">
                <p>Hi {customer.first_name},</p>

                <div class="reminder-box">
                    <h3>Your appointment is tomorrow!</h3>
                    <p><strong>Service:</strong> {service.name}</p>
                    <p><strong>Date:</strong> {appointment_datetime.strftime('%A, %B %d, %Y')}</p>
                    <p><strong>Time:</strong> {appointment_datetime.strftime('%I:%M %p')}</p>
                </div>

                <p>We look forward to seeing you tomorrow!</p>
                <p>Please arrive 10 minutes early.</p>

                <p>If you need to reschedule, please call us at (555) 123-4567.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return send_email(customer.email, subject, html_content)
