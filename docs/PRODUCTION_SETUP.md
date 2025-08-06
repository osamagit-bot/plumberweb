# Production Deployment Guide

## Security Fixes Applied ✅
- Fixed path traversal vulnerabilities
- Added XSS protection with input escaping
- Implemented rate limiting on forms
- Added proper error handling for email operations
- Removed hardcoded credentials

## Database Setup (MySQL)

1. Install MySQL:
```bash
sudo apt update
sudo apt install mysql-server
```

2. Create database and user:
```sql
CREATE DATABASE plumber_production;
CREATE USER 'plumber_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON plumber_production.* TO 'plumber_user'@'localhost';
FLUSH PRIVILEGES;
```

## Redis Setup

```bash
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

## Application Setup

1. Copy `.env.production` to `.env` and update values
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Collect static files: `python manage.py collectstatic`
5. Create superuser: `python manage.py createsuperuser`

## Web Server Setup

1. Install Nginx: `sudo apt install nginx`
2. Copy `nginx.conf` to `/etc/nginx/sites-available/plumber`
3. Enable site: `sudo ln -s /etc/nginx/sites-available/plumber /etc/nginx/sites-enabled/`
4. Test config: `sudo nginx -t`
5. Restart Nginx: `sudo systemctl restart nginx`

## SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

## Gunicorn Service

Create `/etc/systemd/system/gunicorn.service`:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/project
ExecStart=/path/to/venv/bin/gunicorn --config gunicorn.conf.py plumber_site.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

## Automated Backups

Add to crontab (`crontab -e`):
```bash
# Daily database backup at 2 AM
0 2 * * * /path/to/venv/bin/python /path/to/project/scripts/backup_database.py
```

## Monitoring Endpoints

- Health check: `https://yourdomain.com/monitoring/health/`
- System status: `https://yourdomain.com/monitoring/status/`

## CDN Setup (Optional)

For static files, consider using:
- AWS CloudFront
- Cloudflare
- MaxCDN

Update `STATIC_URL` in settings to CDN URL.

## Rate Limiting Applied

- Booking form: 5 requests/minute per IP
- Contact form: 5 requests/minute per IP  
- Feedback form: 3 requests/minute per IP
- Monitoring endpoints: 10 requests/second per IP

## Logging

Logs are stored in:
- `logs/django.log` - Application logs
- `logs/security.log` - Security events
- `logs/gunicorn_access.log` - Access logs
- `logs/gunicorn_error.log` - Error logs

## Performance Optimizations

- Redis caching enabled
- Database query optimization
- Static file compression
- CDN ready configuration

## Security Features

- HTTPS redirect
- Security headers
- Rate limiting
- Input validation
- SQL injection protection
- XSS protection