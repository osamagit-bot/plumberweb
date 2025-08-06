#!/usr/bin/env python
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Add the project directory to Python path
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')

import django
django.setup()

from django.conf import settings

def backup_mysql_database():
    """Create MySQL database backup"""
    db_config = settings.DATABASES['default']
    
    if db_config['ENGINE'] != 'django.db.backends.mysql':
        print("Not a MySQL database")
        return False
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path(__file__).parent.parent / 'backups'
    backup_dir.mkdir(exist_ok=True)
    
    backup_file = backup_dir / f"backup_{timestamp}.sql"
    
    cmd = [
        'mysqldump',
        f"--host={db_config['HOST']}",
        f"--port={db_config['PORT']}",
        f"--user={db_config['USER']}",
        f"--password={db_config['PASSWORD']}",
        '--single-transaction',
        '--routines',
        '--triggers',
        db_config['NAME']
    ]
    
    try:
        with open(backup_file, 'w') as f:
            subprocess.run(cmd, stdout=f, check=True)
        
        print(f"Backup created: {backup_file}")
        
        # Compress backup
        subprocess.run(['gzip', str(backup_file)], check=True)
        print(f"Backup compressed: {backup_file}.gz")
        
        # Clean old backups (keep last 7 days)
        cleanup_old_backups(backup_dir)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")
        return False

def cleanup_old_backups(backup_dir, days_to_keep=7):
    """Remove backups older than specified days"""
    import time
    cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)
    
    for backup_file in backup_dir.glob('backup_*.sql.gz'):
        if backup_file.stat().st_mtime < cutoff_time:
            backup_file.unlink()
            print(f"Removed old backup: {backup_file}")

if __name__ == '__main__':
    backup_mysql_database()