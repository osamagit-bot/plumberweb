#!/usr/bin/env python
import os
import sys
import subprocess
import shutil
import tarfile
from pathlib import Path

# Add the project directory to Python path
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')

import django
django.setup()

from django.conf import settings

def restore_backup(backup_path):
    """Restore from backup archive or directory"""
    backup_path = Path(backup_path)
    
    if not backup_path.exists():
        print(f"❌ Backup not found: {backup_path}")
        return False
    
    # Extract if it's an archive
    if backup_path.suffix == '.gz' and backup_path.name.endswith('.tar.gz'):
        print("📦 Extracting backup archive...")
        temp_dir = backup_path.parent / 'temp_restore'
        temp_dir.mkdir(exist_ok=True)
        
        try:
            with tarfile.open(backup_path, 'r:gz') as tar:
                tar.extractall(temp_dir)
            
            # Find the backup directory inside
            backup_dirs = list(temp_dir.glob('full_backup_*'))
            if not backup_dirs:
                print("❌ Invalid backup archive structure")
                shutil.rmtree(temp_dir)
                return False
            
            backup_dir = backup_dirs[0]
        except Exception as e:
            print(f"❌ Failed to extract backup: {e}")
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            return False
    else:
        backup_dir = backup_path
        temp_dir = None
    
    try:
        # Show backup info
        show_backup_info(backup_dir)
        
        # Confirm restore
        if not confirm_restore():
            print("❌ Restore cancelled")
            return False
        
        # Create backup of current state
        print("💾 Creating backup of current state...")
        create_pre_restore_backup()
        
        success = True
        
        # 1. Restore database
        print("📊 Restoring database...")
        if not restore_database(backup_dir):
            success = False
        
        # 2. Restore media files
        print("🖼️ Restoring media files...")
        if not restore_media_files(backup_dir):
            success = False
        
        # 3. Restore configuration files (optional)
        print("⚙️ Configuration files available in backup/config/")
        print("   (Review and manually apply if needed)")
        
        if success:
            print("✅ Restore completed successfully!")
            print("🔄 Run 'python manage.py migrate' if needed")
            print("📁 Run 'python manage.py collectstatic' to regenerate static files")
        else:
            print("⚠️ Restore completed with some errors")
        
        return success
        
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False
    finally:
        # Clean up temp directory
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)

def show_backup_info(backup_dir):
    """Display backup information"""
    info_file = backup_dir / "backup_info.txt"
    if info_file.exists():
        print("📋 Backup Information:")
        print("-" * 50)
        with open(info_file, 'r') as f:
            print(f.read())
        print("-" * 50)
    else:
        print("⚠️ No backup info file found")

def confirm_restore():
    """Ask user to confirm restore operation"""
    print("⚠️  WARNING: This will overwrite your current data!")
    print("   - Database will be replaced")
    print("   - Media files will be replaced")
    print("   - Current data will be backed up first")
    
    response = input("\nDo you want to continue? (yes/no): ").lower().strip()
    return response in ['yes', 'y']

def create_pre_restore_backup():
    """Create backup of current state before restore"""
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = Path(__file__).parent.parent / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        pre_restore_dir = backup_dir / f"pre_restore_{timestamp}"
        pre_restore_dir.mkdir(exist_ok=True)
        
        # Backup current database
        db_config = settings.DATABASES['default']
        if db_config['ENGINE'] == 'django.db.backends.sqlite3':
            db_path = Path(db_config['NAME'])
            if db_path.exists():
                shutil.copy2(db_path, pre_restore_dir / "database.sqlite3")
        
        # Backup current media
        media_root = Path(settings.MEDIA_ROOT)
        if media_root.exists():
            shutil.copytree(media_root, pre_restore_dir / "media")
        
        print(f"  ✅ Current state backed up to: {pre_restore_dir}")
    except Exception as e:
        print(f"  ⚠️ Failed to backup current state: {e}")

def restore_database(backup_dir):
    """Restore database from backup"""
    db_config = settings.DATABASES['default']
    
    if db_config['ENGINE'] == 'django.db.backends.mysql':
        return restore_mysql(backup_dir, db_config)
    elif db_config['ENGINE'] == 'django.db.backends.sqlite3':
        return restore_sqlite(backup_dir, db_config)
    else:
        print(f"  ❌ Unsupported database engine: {db_config['ENGINE']}")
        return False

def restore_mysql(backup_dir, db_config):
    """Restore MySQL database"""
    try:
        backup_file = backup_dir / "database.sql"
        if not backup_file.exists():
            print(f"  ❌ Database backup not found: {backup_file}")
            return False
        
        # Drop and recreate database
        print("  🗑️ Dropping existing database...")
        drop_cmd = [
            'mysql',
            f"--host={db_config['HOST']}",
            f"--port={db_config['PORT']}",
            f"--user={db_config['USER']}",
            f"--password={db_config['PASSWORD']}",
            '-e', f"DROP DATABASE IF EXISTS {db_config['NAME']}; CREATE DATABASE {db_config['NAME']};"
        ]
        subprocess.run(drop_cmd, check=True)
        
        # Restore from backup
        print("  📥 Restoring database...")
        restore_cmd = [
            'mysql',
            f"--host={db_config['HOST']}",
            f"--port={db_config['PORT']}",
            f"--user={db_config['USER']}",
            f"--password={db_config['PASSWORD']}",
            db_config['NAME']
        ]
        
        with open(backup_file, 'r') as f:
            subprocess.run(restore_cmd, stdin=f, check=True)
        
        print(f"  ✅ MySQL database restored")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ❌ MySQL restore failed: {e}")
        return False

def restore_sqlite(backup_dir, db_config):
    """Restore SQLite database"""
    try:
        backup_file = backup_dir / "database.sqlite3"
        if not backup_file.exists():
            print(f"  ❌ Database backup not found: {backup_file}")
            return False
        
        db_path = Path(db_config['NAME'])
        
        # Backup current database if exists
        if db_path.exists():
            db_path.unlink()
        
        # Copy backup to database location
        shutil.copy2(backup_file, db_path)
        print(f"  ✅ SQLite database restored")
        return True
    except Exception as e:
        print(f"  ❌ SQLite restore failed: {e}")
        return False

def restore_media_files(backup_dir):
    """Restore media files"""
    try:
        media_backup_dir = backup_dir / "media"
        if not media_backup_dir.exists():
            print(f"  ⚠️ No media files in backup")
            return True
        
        media_root = Path(settings.MEDIA_ROOT)
        
        # Remove current media files
        if media_root.exists():
            shutil.rmtree(media_root)
        
        # Copy backup media files
        shutil.copytree(media_backup_dir, media_root)
        
        file_count = sum(1 for _ in media_root.rglob('*') if _.is_file())
        print(f"  ✅ Media files restored ({file_count} files)")
        return True
    except Exception as e:
        print(f"  ❌ Media restore failed: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python restore_backup.py <backup_path>")
        print("Examples:")
        print("  python restore_backup.py backups/full_backup_20231201_143022.tar.gz")
        print("  python restore_backup.py backups/full_backup_20231201_143022/")
        sys.exit(1)
    
    backup_path = sys.argv[1]
    restore_backup(backup_path)

if __name__ == '__main__':
    main()