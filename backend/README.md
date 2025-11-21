# Shamrock Day Spa - Backend API

Python Flask backend with appointment scheduling, customer management, and newsletter functionality.

## 🚀 Features

### Core Functionality
- **Appointment Booking System**: Book, view, update, and cancel appointments
- **Customer Management**: Track customer information and appointment history
- **Newsletter Subscriptions**: Manage email newsletter subscribers
- **Contact Form**: Handle customer inquiries
- **Service Management**: Configure and manage spa services
- **Scheduling**: Smart time slot availability checking
- **Email Notifications**: Automated confirmation and reminder emails

### API Endpoints

#### Appointments
- `POST /api/appointments` - Create new appointment
- `GET /api/appointments/<id>` - Get appointment details
- `PUT /api/appointments/<id>` - Update appointment
- `DELETE /api/appointments/<id>` - Cancel appointment
- `GET /api/appointments/customer/<email>` - Get customer's appointments
- `GET /api/appointments/available-slots` - Get available time slots

#### Newsletter
- `POST /api/newsletter/subscribe` - Subscribe to newsletter
- `POST /api/newsletter/unsubscribe` - Unsubscribe from newsletter
- `GET /api/newsletter/subscribers` - Get all subscribers (admin)

#### Contact
- `POST /api/contact/submit` - Submit contact form
- `GET /api/contact/messages` - Get all messages (admin)
- `PUT /api/contact/messages/<id>` - Update message status (admin)

#### Services
- `GET /api/services` - Get all active services

#### Admin
- `GET /api/admin/dashboard` - Get dashboard statistics
- `GET /api/admin/appointments` - Get all appointments with filters
- `GET /api/admin/customers` - Get all customers
- `GET /api/admin/services` - Manage services
- `POST /api/admin/services` - Create new service
- `PUT /api/admin/services/<id>` - Update service
- `DELETE /api/admin/services/<id>` - Delete/deactivate service

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Configure Environment (Optional)

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` to configure:
- Secret key for Flask sessions
- Email SMTP settings (for sending emails)
- Database connection (default: SQLite)

### Step 3: Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## 🗄️ Database

### SQLite (Default)
The application uses SQLite by default, which requires no setup. The database file `spa.db` will be created automatically on first run.

### PostgreSQL (Production)
To use PostgreSQL in production, update your `.env`:

```
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/spa_db
```

Then install the PostgreSQL adapter:
```bash
pip install psycopg2-binary
```

## 📧 Email Configuration

The application can send emails for:
- Appointment confirmations
- Newsletter welcome messages
- Contact form notifications
- Appointment reminders

### Gmail Setup Example

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to Google Account → Security → 2-Step Verification
   - Scroll to "App passwords"
   - Generate password for "Mail"
3. Update your `.env` file:

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password-here
FROM_EMAIL=noreply@shamrockspa.com
FROM_NAME=Shamrock Day Spa
ADMIN_EMAIL=admin@shamrockspa.com
```

**Note**: If email is not configured, the app will still work but will only log email messages to console.

## 🏗️ Database Schema

### Customer
- id, first_name, last_name, email, phone
- created_at, updated_at

### Service
- id, name, description, duration_minutes, price, category, active
- created_at

### Appointment
- id, customer_id, service_id
- appointment_date, appointment_time
- status (pending, confirmed, completed, cancelled, no-show)
- notes, reminder_sent
- created_at, updated_at

### NewsletterSubscriber
- id, email, is_active
- subscribed_at, unsubscribed_at

### ContactMessage
- id, name, email, phone, subject, message
- status (new, read, responded)
- created_at

## 🔐 Security Notes

### For Development
- Default secret key is used
- Debug mode is enabled
- CORS is wide open
- No authentication on admin endpoints

### For Production
1. **Set a strong SECRET_KEY** in environment variables
2. **Disable DEBUG mode**: Set `FLASK_ENV=production`
3. **Configure CORS**: Restrict to your domain only
4. **Add authentication**: Implement JWT or session-based auth for admin endpoints
5. **Use HTTPS**: Deploy behind a reverse proxy with SSL
6. **Input validation**: Already included, but review for your use case
7. **Rate limiting**: Add rate limiting middleware
8. **Database**: Use PostgreSQL instead of SQLite

## 🎯 Default Services

The application initializes with these default services:
- Swedish Massage ($75, 60 min)
- Deep Tissue Massage ($85, 60 min)
- Hot Stone Massage ($120, 90 min)
- Classic Facial ($65, 60 min)
- Anti-Aging Facial ($95, 75 min)
- Body Scrub ($80, 45 min)
- Manicure ($35, 45 min)
- Pedicure ($45, 60 min)
- Deluxe Spa Package ($250, 180 min)

You can modify these through the admin API.

## 📊 API Response Format

### Success Response
```json
{
  "message": "Success message",
  "data": {...}
}
```

### Error Response
```json
{
  "error": "Error message description"
}
```

## 🧪 Testing the API

### Using curl

**Book an appointment:**
```bash
curl -X POST http://localhost:5000/api/appointments \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "555-1234",
    "service_id": 1,
    "date": "2024-12-25",
    "time": "10:00",
    "notes": "First time visit"
  }'
```

**Subscribe to newsletter:**
```bash
curl -X POST http://localhost:5000/api/newsletter/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email": "subscriber@example.com"}'
```

**Get available time slots:**
```bash
curl "http://localhost:5000/api/appointments/available-slots?date=2024-12-25&service_id=1"
```

## 🔄 Appointment Scheduling Logic

- Business hours: 9 AM to 8 PM (configurable in app.py)
- Time slots: 30-minute intervals
- Appointments cannot overlap
- Minimum booking time: Current time
- Automatic conflict detection

## 📝 Development

### Project Structure
```
backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── models/
│   └── models.py         # Database models
├── routes/
│   ├── appointments.py   # Appointment endpoints
│   ├── newsletter.py     # Newsletter endpoints
│   ├── contact.py        # Contact form endpoints
│   └── admin.py          # Admin dashboard endpoints
├── utils/
│   └── email_service.py  # Email functionality
└── templates/            # Email templates (future)
```

### Adding New Features

1. **New database model**: Add to `models/models.py`
2. **New API endpoint**: Create route file in `routes/`
3. **Register blueprint**: Import and register in `app.py`
4. **Update frontend**: Add API calls in `../js/script.js`

## 🐛 Troubleshooting

**Import errors**: Make sure you're in the backend directory when running
```bash
cd backend
python app.py
```

**Database errors**: Delete `spa.db` and restart to recreate:
```bash
rm spa.db
python app.py
```

**Port already in use**: Change port in `app.py`:
```python
app.run(debug=True, port=5001)  # Change from 5000
```

**CORS errors**: Check that frontend is accessing `http://localhost:5000/api`

## 🚀 Deployment

### Heroku
1. Create `Procfile`: `web: gunicorn app:app`
2. Add `gunicorn` to requirements.txt
3. Set environment variables in Heroku dashboard
4. Push to Heroku

### AWS / DigitalOcean / VPS
1. Install Python and dependencies
2. Use gunicorn or uWSGI as WSGI server
3. Set up Nginx as reverse proxy
4. Configure SSL with Let's Encrypt
5. Use systemd or supervisor for process management

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)

## 🤝 Support

For issues or questions:
1. Check the console output for error messages
2. Verify environment variables are set correctly
3. Check database connection
4. Review API endpoint documentation above

---

Built with Flask, SQLAlchemy, and care for your spa business! 🌿
