# 🚀 Deployment Configuration

## Files in this directory:

- **`gunicorn.conf.py`** - Gunicorn WSGI server configuration
- **`nginx.conf`** - Nginx web server configuration  
- **`deploy.sh`** - Automated deployment script
- **`.env.production`** - Production environment template

## Usage:

```bash
# Copy production environment
cp deployment/.env.production .env

# Deploy to production
./deployment/deploy.sh

# Configure web server
sudo cp deployment/nginx.conf /etc/nginx/sites-available/plumber
sudo ln -s /etc/nginx/sites-available/plumber /etc/nginx/sites-enabled/
```