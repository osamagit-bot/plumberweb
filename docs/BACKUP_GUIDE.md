# 🔒 Comprehensive Backup & Restore Guide

## 📋 What Gets Backed Up

### ✅ Full Backup Includes:
1. **Database** - All your data (bookings, services, testimonials, etc.)
2. **Media Files** - User uploaded images, gallery photos
3. **Configuration Files** - Settings, environment variables, deployment configs
4. **Static Files** - CSS, JS, images (optional - can be regenerated)

### 📊 Database Backup Includes:
- All tables and data
- Database structure
- Indexes and constraints
- Triggers and stored procedures
- User permissions

## 🚀 How to Create Backups

### Method 1: Interactive Backup Manager (Recommended)
```bash
python scripts/backup_manager.py
```
**Features:**
- Easy menu interface
- List existing backups
- Create full or database-only backups
- Restore from backups
- Clean old backups

### Method 2: Command Line Scripts

#### Full Backup (Everything)
```bash
python scripts/full_backup.py
```
**Creates:** `backups/full_backup_YYYYMMDD_HHMMSS.tar.gz`

#### Database Only Backup
```bash
python scripts/backup_database.py
```
**Creates:** `backups/backup_YYYYMMDD_HHMMSS.sql.gz`

### Method 3: Automated Backups (Production)

#### Daily Automatic Backup
Add to crontab (`crontab -e`):
```bash
# Daily full backup at 2 AM
0 2 * * * cd /path/to/project && /path/to/venv/bin/python scripts/full_backup.py

# Weekly database backup at 3 AM on Sundays
0 3 * * 0 cd /path/to/project && /path/to/venv/bin/python scripts/backup_database.py
```

## 📦 Backup Contents Detail

### Full Backup Structure:
```
full_backup_20231201_143022.tar.gz
├── database.sql (or database.sqlite3)
├── media/
│   ├── gallery/
│   │   ├── before/
│   │   └── after/
│   └── uploads/
├── config/
│   ├── .env
│   ├── requirements.txt
│   ├── gunicorn.conf.py
│   ├── nginx.conf
│   └── plumber_site_settings.py
├── static/ (optional)
└── backup_info.txt
```

### Backup Info File Contains:
- Backup timestamp
- Django version
- Database type and name
- Debug mode status
- Restore instructions

## 🔄 How to Restore Backups

### Method 1: Interactive Restore
```bash
python scripts/backup_manager.py
# Select option 4 (Restore from backup)
```

### Method 2: Command Line Restore
```bash
python scripts/restore_backup.py backups/full_backup_20231201_143022.tar.gz
```

### Method 3: Manual Restore Steps

#### 1. Extract Backup
```bash
tar -xzf full_backup_20231201_143022.tar.gz
cd full_backup_20231201_143022
```

#### 2. Restore Database

**MySQL:**
```bash
mysql -u username -p -h localhost database_name < database.sql
```

**SQLite:**
```bash
cp database.sqlite3 /path/to/project/db.sqlite3
```

#### 3. Restore Media Files
```bash
cp -r media/* /path/to/project/media/
```

#### 4. Review Configuration Files
```bash
# Check config/ directory for important settings
# Manually apply any needed configuration changes
```

#### 5. Run Django Commands
```bash
python manage.py migrate
python manage.py collectstatic
```

## ⚠️ Important Restore Notes

### Before Restoring:
- ✅ **Current data is automatically backed up** before restore
- ✅ **Confirmation required** - you'll be asked to confirm
- ✅ **Database is completely replaced** - no merging
- ✅ **Media files are completely replaced**

### After Restoring:
- 🔄 Run `python manage.py migrate` (if needed)
- 📁 Run `python manage.py collectstatic` 
- 👤 You may need to recreate superuser if not in backup
- 🔧 Review and apply configuration changes manually

## 🧹 Backup Maintenance

### Automatic Cleanup
- **Full backups:** Kept for 7 days by default
- **Database backups:** Kept for 7 days by default
- **Old backups automatically deleted** when creating new ones

### Manual Cleanup
```bash
python scripts/backup_manager.py
# Select option 5 (Clean old backups)
```

### Storage Recommendations
- **Development:** Keep 3-7 days of backups
- **Production:** Keep 30 days of backups
- **Critical Production:** Keep 90 days + monthly archives

## 📊 Backup Sizes (Approximate)

| Backup Type | Typical Size | Description |
|-------------|--------------|-------------|
| Database Only | 1-10 MB | Just the data |
| Full Backup | 10-100 MB | Everything included |
| With Large Media | 100MB-1GB+ | Depends on images |

## 🚨 Emergency Recovery Scenarios

### Scenario 1: Database Corruption
```bash
# Quick database restore
python scripts/restore_backup.py latest_backup.tar.gz
python manage.py migrate
```

### Scenario 2: Accidental Data Deletion
```bash
# Restore from most recent backup
python scripts/backup_manager.py
# Select restore option
```

### Scenario 3: Server Migration
```bash
# On old server
python scripts/full_backup.py

# Transfer backup file to new server
scp backups/full_backup_*.tar.gz user@newserver:/path/

# On new server
python scripts/restore_backup.py full_backup_*.tar.gz
```

### Scenario 4: Development Reset
```bash
# Reset to clean state
python scripts/restore_backup.py clean_backup.tar.gz
python manage.py createsuperuser
```

## ✅ Backup Best Practices

### For Development:
- 📅 **Daily backups** before major changes
- 🧪 **Test restore process** regularly
- 💾 **Keep backups locally** and in cloud storage

### For Production:
- 📅 **Automated daily backups**
- 🌐 **Store backups off-site** (cloud storage)
- 🔒 **Encrypt sensitive backups**
- 🧪 **Test restore monthly**
- 📋 **Document recovery procedures**

### Security:
- 🔐 **Encrypt backup files** containing sensitive data
- 🚫 **Don't store backups in web-accessible directories**
- 🔑 **Secure backup storage credentials**
- 🗑️ **Securely delete old backups**

## 🆘 Troubleshooting

### Backup Fails:
- Check disk space
- Verify database credentials
- Ensure MySQL/SQLite is accessible
- Check file permissions

### Restore Fails:
- Verify backup file integrity
- Check database server is running
- Ensure sufficient disk space
- Verify file permissions

### Missing Files After Restore:
- Check backup contents: `tar -tzf backup.tar.gz`
- Verify media directory permissions
- Run `python manage.py collectstatic`

## 📞 Quick Reference Commands

```bash
# Create full backup
python scripts/full_backup.py

# Interactive backup manager
python scripts/backup_manager.py

# Restore from backup
python scripts/restore_backup.py backup_file.tar.gz

# List backups
ls -la backups/

# Check backup contents
tar -tzf backups/full_backup_*.tar.gz
```

Your data is now fully protected with comprehensive backup and restore capabilities! 🛡️