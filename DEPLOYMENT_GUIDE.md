# Google Cloud Deployment Guide

## 🎯 Current Status

✅ **Completed:**
- Google Cloud project created: `smb-personal-agent`
- Production configuration files created
- Code committed and pushed to GitHub
- Account configured: yinglu08fall@gmail.com

⚠️ **Requires Manual Action:**
- Enable billing on the Google Cloud project
- Complete deployment

---

## 📋 Step-by-Step Deployment

### Step 1: Enable Billing (REQUIRED)

Google Cloud requires a billing account to deploy applications.

1. Go to the Google Cloud Console: https://console.cloud.google.com
2. Select project: **smb-personal-agent**
3. Navigate to **Billing** in the left menu
4. Click **Link a billing account**
5. Create a new billing account or select an existing one
6. **Note:** Google offers $300 free credit for new accounts

### Step 2: Deploy to App Engine

Once billing is enabled, run these commands:

```bash
cd /Users/luying/Documents/cloud9/shamrock-spa-website

# Enable required APIs
gcloud services enable appengine.googleapis.com cloudbuild.googleapis.com

# Create App Engine application (choose region when prompted)
gcloud app create --region=us-central

# Deploy the application
gcloud app deploy app.yaml

# Open the deployed application
gcloud app browse
```

### Step 3: Configure Environment Variables (Production)

For production, update the `app.yaml` file with secure values:

```yaml
env_variables:
  FLASK_ENV: 'production'
  SECRET_KEY: 'GENERATE-A-STRONG-SECRET-KEY-HERE'
  SMTP_HOST: 'smtp.gmail.com'
  SMTP_PORT: '587'
  SMTP_USERNAME: 'your-email@gmail.com'
  SMTP_PASSWORD: 'your-app-password'
  FROM_EMAIL: 'noreply@shamrockdayspa.com'
  ADMIN_EMAIL: 'yinglu1985.shanghai@gmail.com'
```

Then deploy again:
```bash
gcloud app deploy app.yaml
```

---

## 🔧 Production Configuration

### Files Created:

1. **`requirements.txt`** - Python dependencies
2. **`app.yaml`** - App Engine configuration
3. **`main.py`** - Application entry point
4. **`.gcloudignore`** - Files to exclude from deployment

### App Engine Configuration:

- **Runtime:** Python 3.12
- **Instance Class:** F2 (256MB RAM, 1.2GHz CPU)
- **Scaling:** Auto-scaling (1-10 instances)
- **HTTPS:** Enforced on all routes
- **Database:** SQLite in /tmp (ephemeral - recreates on restart)

---

## 📊 Monitoring & Management

### View Application Logs:
```bash
gcloud app logs tail -s default
```

### View in Cloud Console:
- **App Engine Dashboard:** https://console.cloud.google.com/appengine
- **Logs:** https://console.cloud.google.com/logs
- **Billing:** https://console.cloud.google.com/billing

### Update Application:
```bash
# Make changes to code
git add .
git commit -m "Your changes"
git push origin main

# Deploy updates
gcloud app deploy app.yaml
```

---

## 🔐 Security Recommendations

1. **Generate a strong SECRET_KEY:**
   ```python
   import secrets
   secrets.token_hex(32)
   ```

2. **Enable Cloud Armor** for DDoS protection

3. **Set up Cloud IAM** for access control

4. **Use Cloud SQL** instead of SQLite for production data persistence

5. **Enable HTTPS only** (already configured in app.yaml)

---

## 💰 Cost Estimate

**App Engine Standard (F2 Instance):**
- Free tier: 28 instance hours/day
- Beyond free tier: ~$0.05/hour

**Estimated monthly cost:**
- Light usage (free tier): **$0/month**
- Moderate usage (100 hours): **~$5/month**
- Heavy usage (24/7): **~$36/month**

**Note:** First-time users get $300 free credit (12 months)

---

## 🌐 Custom Domain (Optional)

To use your own domain (e.g., shamrockdayspa.com):

1. Go to App Engine > Settings > Custom domains
2. Add your domain
3. Verify ownership
4. Update DNS records as instructed
5. Enable SSL (automatic with App Engine)

---

## 📝 Database Upgrade (Recommended for Production)

Current setup uses SQLite in `/tmp` which is **ephemeral** (data resets on instance restart).

For persistent data, migrate to Cloud SQL:

```bash
# Create Cloud SQL instance
gcloud sql instances create spa-db \
    --database-version=POSTGRES_14 \
    --tier=db-f1-micro \
    --region=us-central1

# Create database
gcloud sql databases create spadb --instance=spa-db

# Update app.yaml with Cloud SQL connection
```

---

## 🚀 Quick Deploy Commands

Once billing is enabled:

```bash
# One-time setup
gcloud app create --region=us-central
gcloud services enable appengine.googleapis.com cloudbuild.googleapis.com

# Deploy
gcloud app deploy app.yaml

# View application
gcloud app browse
```

---

## 📞 Support

- **Google Cloud Documentation:** https://cloud.google.com/appengine/docs
- **Billing Support:** https://cloud.google.com/billing/docs
- **GitHub Repository:** https://github.com/yinglu1985/smb_personal_assistant

---

## ✅ Post-Deployment Checklist

- [ ] Billing enabled
- [ ] App deployed successfully
- [ ] Application accessible via URL
- [ ] SECRET_KEY updated to secure value
- [ ] Email configuration tested
- [ ] Database initialized with therapists and services
- [ ] Admin portal accessible
- [ ] Booking system tested
- [ ] SSL certificate active (automatic)
- [ ] Monitoring set up

---

**Need help? The application is ready to deploy once billing is enabled!**
