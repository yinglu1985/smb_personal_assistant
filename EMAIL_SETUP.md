# Email Setup Guide for Shamrock Day Spa

## 📧 Current Email Flow

### When a Customer Books an Appointment:

**Two emails are sent:**

1. **✅ TO CUSTOMER** (`customer.email`)
   - **Subject:** "Appointment Confirmation - [Service Name]"
   - **Contains:**
     - Service details (name, duration, price)
     - Appointment date and time
     - Business location and phone
     - What to bring / arrival instructions
   - **Purpose:** Confirm their booking

2. **✅ TO BUSINESS OWNER** (`info@shamrockdayspa.com`)
   - **Subject:** "New Booking: [Customer Name] - [Service Name]"
   - **Contains:**
     - Customer name, email, phone
     - Service details
     - Appointment date and time
     - Special notes/requests from customer
     - Booking timestamp
   - **Purpose:** Notify owner of new appointment

### Other Emails:

3. **Newsletter Subscription** → Sends welcome email to subscriber
4. **Contact Form** → Sends message to `info@shamrockdayspa.com`
5. **Appointment Reminders** → 24 hours before appointment (requires scheduler setup)

---

## ⚙️ Current Configuration

### Email Addresses:
```
FROM_EMAIL = "noreply@shamrockdayspa.com"
FROM_NAME = "Shamrock Day Spa"
ADMIN_EMAIL = "info@shamrockdayspa.com"  ← Receives booking notifications
```

### SMTP Status:
```
❌ NOT CONFIGURED
```

**What this means:**
- Emails are **NOT actually sent**
- Instead, they are **printed to the console**
- You'll see: "📧 Email would be sent to..."

---

## 🔧 How to Enable Email Sending

To actually send emails, you need to configure SMTP credentials.

### Option 1: Gmail (Recommended for Testing)

1. **Enable 2-Factor Authentication** on your Gmail account

2. **Generate an App Password:**
   - Go to Google Account → Security → 2-Step Verification
   - Scroll to "App passwords"
   - Generate password for "Mail"
   - Copy the 16-character password

3. **Create `.env` file in backend folder:**
   ```bash
   cd backend
   cp .env.example .env
   ```

4. **Edit `.env` file with your credentials:**
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   FROM_EMAIL=noreply@shamrockdayspa.com
   FROM_NAME=Shamrock Day Spa
   ADMIN_EMAIL=actual-owner-email@example.com
   ```

5. **Restart the server:**
   ```bash
   cd backend
   python app.py
   ```

6. **Test booking** - emails will now actually send!

### Option 2: Custom Email Provider

If you have a business email (like `@shamrockdayspa.com`):

```env
SMTP_HOST=mail.your-provider.com
SMTP_PORT=587
SMTP_USERNAME=noreply@shamrockdayspa.com
SMTP_PASSWORD=your-password
FROM_EMAIL=noreply@shamrockdayspa.com
ADMIN_EMAIL=owner@shamrockdayspa.com
```

**Common SMTP Settings:**
- **Office 365:** `smtp.office365.com`, port 587
- **Outlook:** `smtp-mail.outlook.com`, port 587
- **Yahoo:** `smtp.mail.yahoo.com`, port 587
- **Custom Domain:** Check with your hosting provider

---

## 🧪 Testing Email Flow

### Test Without SMTP (Current Setup):

Book an appointment and check the **terminal/console** where Flask is running. You'll see:

```
📧 Email would be sent to customer@email.com
   Subject: Appointment Confirmation - Swedish Massage
   (SMTP not configured - set environment variables to enable email)

📧 Email would be sent to info@shamrockdayspa.com
   Subject: New Booking: John Doe - Swedish Massage
   (SMTP not configured - set environment variables to enable email)
```

### Test With SMTP Configured:

Book an appointment and check:
1. **Customer email inbox** - should receive confirmation
2. **Admin email inbox** (`info@shamrockdayspa.com`) - should receive booking notification
3. **Server console** - should show: "✓ Email sent successfully to..."

---

## 📋 Email Templates Location

All email templates are in:
```
backend/utils/email_service.py
```

Functions:
- `send_appointment_confirmation()` - Customer confirmation
- `send_admin_booking_notification()` - Owner notification ← NEW!
- `send_newsletter_welcome()` - Newsletter welcome
- `send_contact_notification()` - Contact form notification
- `send_appointment_reminder()` - 24-hour reminder

---

## 🎯 Recommended Setup for Production

1. **Use a dedicated email service:**
   - SendGrid (free tier: 100 emails/day)
   - Amazon SES (very cheap)
   - Mailgun (good for transactional emails)

2. **Set up proper domain email:**
   - `noreply@shamrockdayspaservice.com` for sending
   - `info@shamrockdayspaservice.com` for receiving

3. **Add email validation:**
   - SPF records
   - DKIM signing
   - DMARC policy

4. **Monitor delivery:**
   - Check spam folder during testing
   - Add domain to customer contacts
   - Use professional email service

---

## 🔐 Security Notes

- **Never commit `.env` file to git** (it's in .gitignore)
- **Use App Passwords** for Gmail, not your main password
- **Rotate passwords regularly**
- **Use environment variables in production**

---

## 📞 Support

If emails aren't working:

1. Check console for error messages
2. Verify SMTP credentials are correct
3. Check if port 587 is blocked by firewall
4. Try port 465 (SSL) if 587 doesn't work
5. Check email provider's SMTP documentation

---

**Current Status:** ✅ Code ready, ❌ SMTP not configured

To enable email sending, create `backend/.env` file with SMTP credentials!
