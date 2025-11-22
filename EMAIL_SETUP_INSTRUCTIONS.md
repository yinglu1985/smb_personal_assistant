# Gmail App Password Setup Instructions

To enable email notifications for your spa booking system, you need to create a Gmail App Password.

## Step 1: Enable 2-Step Verification

1. Go to your Google Account: https://myaccount.google.com
2. Click on **Security** in the left menu
3. Under "Signing in to Google", click on **2-Step Verification**
4. Follow the prompts to set up 2-Step Verification if not already enabled

## Step 2: Create an App Password

1. Go to https://myaccount.google.com/apppasswords
   - Or: Google Account → Security → 2-Step Verification → App passwords (at the bottom)

2. You may need to sign in again

3. Under "Select app", choose **Mail**

4. Under "Select device", choose **Other (Custom name)**
   - Enter: "Shamrock Day Spa Website"

5. Click **Generate**

6. Google will display a 16-character password (like: `abcd efgh ijkl mnop`)

7. **Copy this password immediately** - you won't be able to see it again

## Step 3: Update app.yaml

1. Open `/Users/luying/Documents/cloud9/shamrock-spa-website/app.yaml`

2. Find the line:
   ```yaml
   SMTP_PASSWORD: 'GMAIL_APP_PASSWORD_NEEDED_HERE'
   ```

3. Replace `GMAIL_APP_PASSWORD_NEEDED_HERE` with your generated app password:
   ```yaml
   SMTP_PASSWORD: 'abcdefghijklmnop'
   ```

   **Important:** Remove all spaces from the app password when pasting it

## Step 4: Redeploy

```bash
cd /Users/luying/Documents/cloud9/shamrock-spa-website
gcloud app deploy app.yaml --quiet
```

## Email Configuration Details

The following emails are configured:

- **FROM_EMAIL:** yinglu08fall@gmail.com (sender address for all emails)
- **ADMIN_EMAIL:** yinglu1985.shanghai@gmail.com (receives booking notifications)

When a customer books an appointment:
1. Customer receives a confirmation email at their provided email address
2. Admin (yinglu1985.shanghai@gmail.com) receives a booking notification

## Testing Emails

After deploying, test the email system:

1. Go to your deployed site: https://smb-personal-agent.uc.r.appspot.com
2. Book a test appointment
3. Check both:
   - Customer's email inbox for confirmation
   - yinglu1985.shanghai@gmail.com for admin notification

## Troubleshooting

**If emails don't send:**

1. Verify 2-Step Verification is enabled on yinglu08fall@gmail.com
2. Double-check the app password was copied correctly (no spaces)
3. Check Google Cloud logs: `gcloud app logs tail -s default`
4. Look for error messages in the logs related to SMTP

**Security Note:**
- App passwords are safer than using your main Gmail password
- If compromised, you can revoke the app password without changing your main password
- Never commit real passwords to git repositories

## Alternative: Using SendGrid or Gmail API

For production, consider:
- **SendGrid:** Free tier allows 100 emails/day
- **Gmail API:** Better for high-volume email sending
- **Mailgun:** Developer-friendly email service

---

**Current Status:** Email configuration is ready except for the Gmail App Password. Once you add it and redeploy, all email notifications will work.
