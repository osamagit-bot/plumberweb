#!/usr/bin/env python
import os
import sys
from pathlib import Path
from datetime import datetime

# Add the project directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

def show_menu():
    """Display backup management menu"""
    print("\n🔧 Plumber Website Backup Manager")
    print("=" * 40)
    print("1. Create full backup (recommended)")
    print("2. Create database-only backup")
    print("3. List available backups")
    print("4. Restore from backup")
    print("5. Clean old backups")
    print("6. Exit")
    print("=" * 40)

def list_backups():
    """List available backups"""
    backup_dir = Path(__file__).parent.parent / 'backups'
    if not backup_dir.exists():
        print("📁 No backups directory found")
        return
    
    full_backups = list(backup_dir.glob('full_backup_*.tar.gz'))
    db_backups = list(backup_dir.glob('backup_*.sql.gz'))
    
    print("\n📦 Available Backups:")
    print("-" * 50)
    
    if full_backups:
        print("🎯 Full Backups (Database + Media + Config):")
        for backup in sorted(full_backups, reverse=True):
            size = backup.stat().st_size / (1024*1024)
            date = datetime.fromtimestamp(backup.stat().st_mtime)
            print(f"  • {backup.name} ({size:.1f} MB) - {date.strftime('%Y-%m-%d %H:%M')}")
    
    if db_backups:
        print("\n💾 Database-Only Backups:")
        for backup in sorted(db_backups, reverse=True):
            size = backup.stat().st_size / (1024*1024)
            date = datetime.fromtimestamp(backup.stat().st_mtime)
            print(f"  • {backup.name} ({size:.1f} MB) - {date.strftime('%Y-%m-%d %H:%M')}")
    
    if not full_backups and not db_backups:
        print("  No backups found")

def create_full_backup():
    """Create full backup"""
    print("\n🚀 Creating full backup...")
    try:
        from full_backup import create_full_backup
        success = create_full_backup()
        if success:
            print("✅ Full backup completed successfully!")
        else:
            print("❌ Backup failed!")
    except ImportError:
        print("❌ Full backup script not found")

def create_db_backup():
    """Create database-only backup"""
    print("\n💾 Creating database backup...")
    try:
        from backup_database import backup_mysql_database
        success = backup_mysql_database()
        if success:
            print("✅ Database backup completed!")
        else:
            print("❌ Database backup failed!")
    except ImportError:
        print("❌ Database backup script not found")

def restore_backup():
    """Restore from backup"""
    backup_dir = Path(__file__).parent.parent / 'backups'
    if not backup_dir.exists():
        print("❌ No backups directory found")
        return
    
    full_backups = list(backup_dir.glob('full_backup_*.tar.gz'))
    if not full_backups:
        print("❌ No full backups found")
        return
    
    print("\n📦 Available backups for restore:")
    for i, backup in enumerate(sorted(full_backups, reverse=True), 1):
        size = backup.stat().st_size / (1024*1024)
        date = datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"  {i}. {backup.name} ({size:.1f} MB) - {date.strftime('%Y-%m-%d %H:%M')}")
    
    try:
        choice = int(input("\nSelect backup to restore (number): ")) - 1
        if 0 <= choice < len(full_backups):
            selected_backup = sorted(full_backups, reverse=True)[choice]
            print(f"\n🔄 Restoring from: {selected_backup.name}")
            
            try:
                from restore_backup import restore_backup
                restore_backup(selected_backup)
            except ImportError:
                print("❌ Restore script not found")
        else:
            print("❌ Invalid selection")
    except ValueError:
        print("❌ Invalid input")

def clean_old_backups():
    """Clean old backups"""
    backup_dir = Path(__file__).parent.parent / 'backups'
    if not backup_dir.exists():
        print("❌ No backups directory found")
        return
    
    print("\n🧹 Cleaning old backups...")
    
    try:
        days = int(input("Keep backups from last how many days? (default 7): ") or "7")
    except ValueError:
        days = 7
    
    import time
    cutoff_time = time.time() - (days * 24 * 60 * 60)
    
    removed = 0
    for pattern in ['full_backup_*.tar.gz', 'backup_*.sql.gz']:
        for backup_file in backup_dir.glob(pattern):
            if backup_file.stat().st_mtime < cutoff_time:
                backup_file.unlink()
                removed += 1
                print(f"  🗑️ Removed: {backup_file.name}")
    
    if removed > 0:
        print(f"✅ Cleaned up {removed} old backups")
    else:
        print("✅ No old backups to clean")

def main():
    """Main menu loop"""
    while True:
        show_menu()
        
        try:
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == '1':
                create_full_backup()
            elif choice == '2':
                create_db_backup()
            elif choice == '3':
                list_backups()
            elif choice == '4':
                restore_backup()
            elif choice == '5':
                clean_old_backups()
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid option. Please select 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")

if __name__ == '__main__':
    main()