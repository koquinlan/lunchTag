# Heroku Email Setup for Password Reset

## Option 1: SendGrid (Recommended)

### Step 1: Add SendGrid Add-on
```bash
# Replace 'your-app-name' with your actual Heroku app name
heroku addons:create sendgrid:starter --app your-app-name
```

### Step 2: Verify Environment Variables
```bash
# Check that SENDGRID_API_KEY is set
heroku config --app your-app-name | grep SENDGRID
```

### Step 3: Deploy Your Code
```bash
git add .
git commit -m "Add password reset functionality"
git push heroku main
```

## Option 2: Gmail (Alternative)

If you prefer to use Gmail instead of SendGrid:

### Step 1: Create Gmail App Password
1. Go to your Google Account settings
2. Enable 2-factor authentication
3. Generate an "App Password" for your Django app

### Step 2: Set Environment Variables
```bash
# Set your Gmail credentials
heroku config:set GMAIL_USER=your-email@gmail.com --app your-app-name
heroku config:set GMAIL_APP_PASSWORD=your-16-char-app-password --app your-app-name
```

### Step 3: Update Production Settings
Uncomment the Gmail configuration in `config/settings/production.py` and comment out the SendGrid configuration.

## Testing Email Functionality

### Test on Heroku
1. Deploy your app: `git push heroku main`
2. Go to your app's login page
3. Click "Forgot your password?"
4. Enter a valid email address
5. Check the email inbox for the reset link

### Check Heroku Logs
```bash
# Monitor logs for email sending
heroku logs --tail --app your-app-name
```

## Troubleshooting

### Common Issues:
1. **"No module named 'dotenv'"** - Make sure you have `python-dotenv` in requirements.txt
2. **Email not sending** - Check Heroku logs for SMTP errors
3. **"Invalid credentials"** - Verify your SendGrid API key or Gmail app password

### SendGrid Free Tier Limits:
- 100 emails/day
- Perfect for development and small apps

### Gmail Limits:
- 500 emails/day for regular accounts
- Requires app password (not regular password)

## Environment Variables Summary

### Required for SendGrid:
- `SENDGRID_API_KEY` (automatically set by Heroku addon)

### Required for Gmail:
- `GMAIL_USER` (your Gmail address)
- `GMAIL_APP_PASSWORD` (16-character app password)

### Already Configured:
- `LUNCH_TAG_SECRET_KEY`
- `API_KEY` (Cloudinary)
- `API_SECRET` (Cloudinary)
