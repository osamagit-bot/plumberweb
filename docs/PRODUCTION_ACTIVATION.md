# Production Features Activation Guide

## Current Status
✅ **Development Mode**: All production features are disabled/commented for easy development
✅ **Production Ready**: All features are implemented and ready to activate

## To Enable Production Features

### 1. Environment Configuration
Copy `.env.production` to `.env` and update:
```bash
cp .env.production .env
# Edit .env with your production values
```

### 2. Rate Limiting (Automatic)
Rate limiting is automatically enabled when `DEBUG=False`. The decorators are ready in `main/views.py`:
- Booking form: 5 requests/minute per IP
- Contact form: 5 requests/minute per IP  
- Feedback form: 3 requests/minute per IP

### 3. Monitoring Endpoints (Automatic)
When `DEBUG=False`, monitoring URLs are automatically added:
- `/monitoring/health/` - Health check endpoint
- `/monitoring/status/` - System status endpoint

### 4. Database Migration to MySQL
Update your `.env` file:
```env
DEBUG=False
DB_NAME=plumber_production
DB_USER=plumber_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306
```

### 5. Redis Cache (Automatic)
Redis cache is automatically enabled in production mode. Install Redis:
```bash
# Ubuntu/Debian
sudo apt install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 6. Install Production Dependencies
```bash
pip install -r requirements.txt
```

### 7. Production Apps & Middleware
The following are automatically enabled when `DEBUG=False`:
- `django_ratelimit` app
- `monitoring` app  
- `MonitoringMiddleware`

## Production Checklist

### Before Going Live:
- [ ] Set `DEBUG=False` in `.env`
- [ ] Configure MySQL database
- [ ] Install and start Redis server
- [ ] Install all requirements: `pip install -r requirements.txt`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Set up SSL certificate
- [ ] Configure Nginx (use provided `nginx.conf`)
- [ ] Set up Gunicorn service (use provided `gunicorn.conf.py`)
- [ ] Configure automated backups (use `scripts/backup_database.py`)

### Security Features (Auto-enabled in Production):
- ✅ HTTPS redirect
- ✅ Secure cookies
- ✅ HSTS headers
- ✅ XSS protection
- ✅ Rate limiting
- ✅ Input sanitization
- ✅ SQL injection protection

### Monitoring Features (Auto-enabled in Production):
- ✅ Health check endpoints
- ✅ System metrics
- ✅ Performance monitoring
- ✅ Error logging
- ✅ Security event logging

## Quick Production Switch

To switch to production mode, simply:
1. Update `.env`: `DEBUG=False`
2. Restart your application

All production features will automatically activate!

## Development Mode Return

To return to development:
1. Update `.env`: `DEBUG=True`  
2. Restart your application

All production features will automatically disable for easier development.

## Files Ready for Production

All these files are ready and configured:
- ✅ `gunicorn.conf.py` - Production server config
- ✅ `nginx.conf` - Web server config  
- ✅ `deploy.sh` - Deployment script
- ✅ `scripts/backup_database.py` - Automated backups
- ✅ `monitoring/` - Health checks and monitoring
- ✅ `.env.production` - Production environment template
- ✅ `PRODUCTION_SETUP.md` - Detailed setup guide