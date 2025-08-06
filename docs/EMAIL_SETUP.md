# Email Notifications Setup Guide

## Overview
Your SPRO Plumbing website now has a complete email notification system that sends:
- **Booking confirmations** to customers
- **Contact form confirmations** to customers  
- **Admin notifications** for new bookings and contact messages

## 🆓 FREE Setup Option (Recommended to Start)

### Using Gmail/Google Workspace

1. **Create/Use a business Gmail account**:
   - Example: `booking@sproplumbing.com` or `info@sproplumbing.com`

2. **Enable 2-Factor Authentication** on the Gmail account

3. **Generate an App Password**:
   - Go to Google Account Settings → Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
   - Copy the 16-character password (no spaces)

4. **Create a `.env` file** in your project root:
   ```bash
   # Copy .env.example to .env first
   cp .env.example .env
   ```

5. **Add these email settings to your `.env` file**:
   ```env
   # Email Configuration
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-business-email@gmail.com
   EMAIL_HOST_PASSWORD=your-16-char-app-password
   EMAIL_USE_TLS=True
   DEFAULT_FROM_EMAIL=SPRO Plumbing <your-business-email@gmail.com>
   ADMIN_EMAIL=admin@sproplumbing.com
   ```

6. **Replace the example values**:
   - `your-business-email@gmail.com` → Your actual Gmail address
   - `your-16-char-app-password` → The app password from step 3
   - `admin@sproplumbing.com` → Email where you want to receive booking notifications

## 📧 What Emails Are Sent

### Customer Confirmation Emails
- **Booking Confirmation**: Professional HTML email with all booking details
- **Contact Confirmation**: Acknowledgment of their message with your contact info

### Admin Notification Emails  
- **New Booking Alert**: Immediate notification with customer details and action items
- **Emergency Booking**: Special urgent formatting for emergency services
- **Contact Message**: Summary of new contact form submissions

## 🧪 Testing the System

### Option 1: Quick Test (Console Backend)
For testing without sending real emails:

1. **Temporarily change email backend** in `settings.py`:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```

2. **Submit a test booking** - emails will print to console

3. **Change back to SMTP** when ready for real emails

### Option 2: Test with Real Emails
1. Set up the Gmail configuration above
2. Submit a test booking with your own email
3. Check that you receive the confirmation email
4. Check that admin receives the notification

## 📊 Monitoring Email Delivery

### Free Gmail Limits
- **Gmail Personal**: 500 emails/day
- **Google Workspace**: 2000 emails/day

### When to Upgrade to Paid Service
Consider upgrading when you reach:
- 50+ bookings per day
- Need delivery tracking/analytics
- Want professional "from" addresses without Gmail

## 🔧 Troubleshooting

### Common Issues

**"SMTPAuthenticationError"**
- Check that 2FA is enabled
- Verify the app password is correct (16 characters, no spaces)
- Make sure you're using the app password, not your regular Gmail password

**"Connection refused"**
- Check EMAIL_HOST and EMAIL_PORT settings
- Verify internet connection
- Try EMAIL_PORT=465 with EMAIL_USE_SSL=True instead of TLS

**Emails not being received**
- Check spam/junk folders
- Verify the recipient email addresses are correct
- Test with console backend first to see if emails are being generated

**Gmail blocks sign-in**
- Ensure 2FA is enabled
- Use app passwords instead of regular password
- Check Google security alerts

## 💰 Upgrade Options (Future)

### Professional Email Services
When you're ready to scale:

**SendGrid** (Recommended)
- Free: 100 emails/day
- Paid: $15/month for 50,000 emails
- Professional deliverability

**Mailgun**
- Free: 5,000 emails/month  
- Paid: $35/month for 50,000 emails
- Good for developers

**AWS SES**
- $0.10 per 1,000 emails
- Most cost-effective for high volume

## 🚀 Next Steps

1. **Set up Gmail configuration** using steps above
2. **Test with a real booking** 
3. **Monitor email delivery** for first few days
4. **Consider upgrading** when volume increases

The system is designed to gracefully handle email failures - if emails can't be sent, the booking/contact still works normally, just without email notifications.
