#!/usr/bin/env python
import os
import sys
import subprocess
import shutil
import tarfile
from datetime import datetime
from pathlib import Path

# Add the project directory to Python path
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')

import django
django.setup()

from django.conf import settings

def create_full_backup():
    """Create comprehensive backup including database, media, and config files"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = Path(__file__).parent.parent / 'backups'
    backup_dir.mkdir(exist_ok=True)
    
    backup_name = f"full_backup_{timestamp}"
    temp_backup_dir = backup_dir / backup_name
    temp_backup_dir.mkdir(exist_ok=True)
    
    success = True
    
    try:
        # 1. Database backup
        print("📊 Backing up database...")
        db_success = backup_database(temp_backup_dir)
        if not db_success:
            success = False
        
        # 2. Media files backup
        print("🖼️ Backing up media files...")
        media_success = backup_media_files(temp_backup_dir)
        if not media_success:
            success = False
        
        # 3. Configuration files backup
        print("⚙️ Backing up configuration files...")
        config_success = backup_config_files(temp_backup_dir)
        if not config_success:
            success = False
        
        # 4. Static files backup (optional)
        print("📁 Backing up static files...")
        static_success = backup_static_files(temp_backup_dir)
        
        # 5. Create backup info file
        create_backup_info(temp_backup_dir, timestamp)
        
        # 6. Compress everything
        print("🗜️ Compressing backup...")
        archive_path = backup_dir / f"{backup_name}.tar.gz"
        with tarfile.open(archive_path, 'w:gz') as tar:
            tar.add(temp_backup_dir, arcname=backup_name)
        
        # 7. Clean up temp directory
        shutil.rmtree(temp_backup_dir)
        
        # 8. Clean old backups
        cleanup_old_backups(backup_dir)
        
        if success:
            print(f"✅ Full backup completed: {archive_path}")
            print(f"📦 Backup size: {archive_path.stat().st_size / (1024*1024):.1f} MB")
        else:
            print("⚠️ Backup completed with some errors")
        
        return success
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        if temp_backup_dir.exists():
            shutil.rmtree(temp_backup_dir)
        return False

def backup_database(backup_dir):
    """Backup database"""
    db_config = settings.DATABASES['default']
    
    if db_config['ENGINE'] == 'django.db.backends.mysql':
        return backup_mysql(backup_dir, db_config)
    elif db_config['ENGINE'] == 'django.db.backends.sqlite3':
        return backup_sqlite(backup_dir, db_config)
    else:
        print(f"Unsupported database engine: {db_config['ENGINE']}")
        return False

def backup_mysql(backup_dir, db_config):
    """Backup MySQL database"""
    try:
        backup_file = backup_dir / "database.sql"
        cmd = [
            'mysqldump',
            f"--host={db_config['HOST']}",
            f"--port={db_config['PORT']}",
            f"--user={db_config['USER']}",
            f"--password={db_config['PASSWORD']}",
            '--single-transaction',
            '--routines',
            '--triggers',
            '--add-drop-table',
            '--complete-insert',
            db_config['NAME']
        ]
        
        with open(backup_file, 'w') as f:
            subprocess.run(cmd, stdout=f, check=True)
        
        print(f"  ✅ MySQL database backed up")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ MySQL backup failed: {e}")
        return False

def backup_sqlite(backup_dir, db_config):
    """Backup SQLite database"""
    try:
        db_path = Path(db_config['NAME'])
        if db_path.exists():
            backup_file = backup_dir / "database.sqlite3"
            shutil.copy2(db_path, backup_file)
            print(f"  ✅ SQLite database backed up")
            return True
        else:
            print(f"  ⚠️ SQLite database not found: {db_path}")
            return False
    except Exception as e:
        print(f"  ❌ SQLite backup failed: {e}")
        return False

def backup_media_files(backup_dir):
    """Backup media files (user uploads)"""
    try:
        media_root = Path(settings.MEDIA_ROOT)
        if media_root.exists() and any(media_root.iterdir()):
            media_backup_dir = backup_dir / "media"
            shutil.copytree(media_root, media_backup_dir)
            file_count = sum(1 for _ in media_backup_dir.rglob('*') if _.is_file())
            print(f"  ✅ Media files backed up ({file_count} files)")
            return True
        else:
            print(f"  ⚠️ No media files to backup")
            return True
    except Exception as e:
        print(f"  ❌ Media backup failed: {e}")
        return False

def backup_config_files(backup_dir):
    """Backup important configuration files"""
    try:
        config_dir = backup_dir / "config"
        config_dir.mkdir(exist_ok=True)
        
        project_root = Path(__file__).parent.parent
        
        # Important files to backup
        important_files = [
            '.env',
            'requirements.txt',
            'gunicorn.conf.py',
            'nginx.conf',
            'deploy.sh',
            'plumber_site/settings.py',
            'plumber_site/urls.py',
        ]
        
        backed_up = 0
        for file_path in important_files:
            source = project_root / file_path
            if source.exists():
                dest = config_dir / file_path.replace('/', '_')
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
                backed_up += 1
        
        print(f"  ✅ Configuration files backed up ({backed_up} files)")
        return True
    except Exception as e:
        print(f"  ❌ Config backup failed: {e}")
        return False

def backup_static_files(backup_dir):
    """Backup static files (optional - can be regenerated)"""
    try:
        static_root = Path(settings.STATIC_ROOT) if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT else None
        if static_root and static_root.exists():
            static_backup_dir = backup_dir / "static"
            shutil.copytree(static_root, static_backup_dir)
            print(f"  ✅ Static files backed up")
        else:
            print(f"  ⚠️ No static files to backup (run collectstatic first)")
        return True
    except Exception as e:
        print(f"  ❌ Static backup failed: {e}")
        return False

def create_backup_info(backup_dir, timestamp):
    """Create backup information file"""
    info_file = backup_dir / "backup_info.txt"
    
    with open(info_file, 'w') as f:
        f.write(f"Plumber Website Backup\n")
        f.write(f"=====================\n\n")
        f.write(f"Backup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Django Version: {django.get_version()}\n")
        f.write(f"Database Engine: {settings.DATABASES['default']['ENGINE']}\n")
        f.write(f"Database Name: {settings.DATABASES['default']['NAME']}\n")
        f.write(f"Debug Mode: {settings.DEBUG}\n\n")
        
        f.write("Backup Contents:\n")
        f.write("- Database dump (database.sql or database.sqlite3)\n")
        f.write("- Media files (user uploads)\n")
        f.write("- Configuration files (.env, settings.py, etc.)\n")
        f.write("- Static files (if available)\n\n")
        
        f.write("Restore Instructions:\n")
        f.write("1. Extract backup: tar -xzf backup_file.tar.gz\n")
        f.write("2. Run restore script: python scripts/restore_backup.py backup_folder\n")

def cleanup_old_backups(backup_dir, days_to_keep=7):
    """Remove backups older than specified days"""
    import time
    cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)
    
    removed = 0
    for backup_file in backup_dir.glob('full_backup_*.tar.gz'):
        if backup_file.stat().st_mtime < cutoff_time:
            backup_file.unlink()
            removed += 1
    
    if removed > 0:
        print(f"🧹 Cleaned up {removed} old backups")

if __name__ == '__main__':
    create_full_backup()