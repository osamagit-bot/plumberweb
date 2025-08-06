#!/bin/bash

# Production deployment script
set -e

echo "Starting deployment..."

# Create full backup BEFORE any changes
echo "📦 Creating pre-deployment backup..."
python scripts/full_backup.py

if [ $? -ne 0 ]; then
    echo "❌ Backup failed! Aborting deployment."
    exit 1
fi

echo "✅ Backup completed successfully"

# Update code
git pull origin main

# Install/update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl restart redis

echo "Deployment completed successfully!"

# Run health check
curl -f http://localhost/monitoring/health/ || echo "Health check failed!"