# MySQL Quick Reference

## Setup Commands

```bash
# Start MySQL
brew services start mysql              # macOS
sudo systemctl start mysql             # Linux

# Login to MySQL
mysql -u root -p

# Run setup script
cd backend
./setup_mysql.sh

# Initialize database
python init_db.py

# Test connection
python -c "from app.database.connection import test_connection; test_connection()"
```

## SQL Commands

```sql
-- Create database
CREATE DATABASE workshop_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use database
USE workshop_management;

-- Show tables
SHOW TABLES;

-- Describe table
DESCRIBE users;

-- View all users
SELECT * FROM users;

-- Count users
SELECT COUNT(*) FROM users;

-- View workshops with owners
SELECT w.*, u.name as owner_name 
FROM workshops w 
LEFT JOIN users u ON w.owner_id = u.id;

-- View participants with user info
SELECT p.*, u.name as user_name, w.title as workshop_title
FROM participants p
JOIN users u ON p.user_id = u.id
JOIN workshops w ON p.workshop_id = w.id;

-- Drop all tables (CAUTION!)
DROP TABLE IF EXISTS challenges;
DROP TABLE IF EXISTS participants;
DROP TABLE IF EXISTS workshops;
DROP TABLE IF EXISTS users;
```

## Backup & Restore

```bash
# Backup
mysqldump -u root -p workshop_management > backup.sql

# Restore
mysql -u root -p workshop_management < backup.sql
```

## Troubleshooting

```bash
# Check MySQL status
brew services list | grep mysql        # macOS
sudo systemctl status mysql            # Linux

# Reset root password
sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'newpassword';
FLUSH PRIVILEGES;
EXIT;
```

