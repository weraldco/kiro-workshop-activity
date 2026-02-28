# Deployment Guide

Complete guide for deploying the Workshop Management System to production.

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Environment Setup](#environment-setup)
3. [Database Setup](#database-setup)
4. [Backend Deployment](#backend-deployment)
5. [Frontend Deployment](#frontend-deployment)
6. [Security Configuration](#security-configuration)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Backup and Recovery](#backup-and-recovery)
9. [Scaling](#scaling)
10. [Troubleshooting](#troubleshooting)

---

## Pre-Deployment Checklist

### Code Preparation
- [ ] All tests passing (backend and frontend)
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Version number updated
- [ ] CHANGELOG.md updated
- [ ] No debug code or console.logs
- [ ] Environment variables documented

### Security
- [ ] Strong JWT_SECRET_KEY generated
- [ ] Database credentials secured
- [ ] CORS origins configured
- [ ] HTTPS enabled
- [ ] Rate limiting configured
- [ ] Input validation verified
- [ ] SQL injection prevention verified
- [ ] XSS protection enabled

### Infrastructure
- [ ] Domain name registered
- [ ] SSL certificate obtained
- [ ] Server provisioned
- [ ] Database server ready
- [ ] Backup system configured
- [ ] Monitoring tools set up
- [ ] CDN configured (optional)

---

## Environment Setup

### Production Server Requirements

**Minimum Specifications**:
- CPU: 2 cores
- RAM: 4GB
- Storage: 20GB SSD
- OS: Ubuntu 20.04 LTS or later

**Recommended Specifications**:
- CPU: 4 cores
- RAM: 8GB
- Storage: 50GB SSD
- OS: Ubuntu 22.04 LTS

### Software Requirements

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.8 python3-pip python3-venv -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install MySQL
sudo apt install mysql-server -y

# Install Nginx
sudo apt install nginx -y

# Install Certbot (for SSL)
sudo apt install certbot python3-certbot-nginx -y

# Install PM2 (process manager)
sudo npm install -g pm2
```

---

## Database Setup

### MySQL Configuration

1. **Secure MySQL Installation**:
```bash
sudo mysql_secure_installation
```

2. **Create Production Database**:
```sql
mysql -u root -p

CREATE DATABASE workshop_management_prod CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE USER 'workshop_prod'@'localhost' IDENTIFIED BY 'STRONG_PASSWORD_HERE';

GRANT ALL PRIVILEGES ON workshop_management_prod.* TO 'workshop_prod'@'localhost';

FLUSH PRIVILEGES;

EXIT;
```

3. **Initialize Schema**:
```bash
mysql -u workshop_prod -p workshop_management_prod < backend/init_db.py
```

4. **Configure MySQL for Production**:
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

Add/modify:
```ini
[mysqld]
max_connections = 200
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow-query.log
long_query_time = 2
```

Restart MySQL:
```bash
sudo systemctl restart mysql
```

### Database Backup

**Automated Daily Backup**:
```bash
# Create backup script
sudo nano /usr/local/bin/backup-workshop-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/workshop"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="workshop_management_prod"
DB_USER="workshop_prod"
DB_PASS="YOUR_PASSWORD"

mkdir -p $BACKUP_DIR

mysqldump -u $DB_USER -p$DB_PASS $DB_NAME | gzip > $BACKUP_DIR/workshop_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "workshop_*.sql.gz" -mtime +30 -delete
```

```bash
# Make executable
sudo chmod +x /usr/local/bin/backup-workshop-db.sh

# Add to crontab (daily at 2 AM)
sudo crontab -e
0 2 * * * /usr/local/bin/backup-workshop-db.sh
```

---

## Backend Deployment

### 1. Deploy Code

```bash
# Create application directory
sudo mkdir -p /var/www/workshop-backend
sudo chown $USER:$USER /var/www/workshop-backend

# Clone repository
cd /var/www/workshop-backend
git clone https://github.com/yourusername/workshop-management.git .

# Or upload files via SCP
scp -r backend/* user@server:/var/www/workshop-backend/
```

### 2. Setup Python Environment

```bash
cd /var/www/workshop-backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install production server
pip install gunicorn
```

### 3. Configure Environment

```bash
# Create production .env
nano .env
```

```env
# Production Environment Variables
JWT_SECRET_KEY=GENERATE_STRONG_RANDOM_KEY_HERE
JWT_EXPIRATION_MINUTES=30

DB_HOST=localhost
DB_PORT=3306
DB_NAME=workshop_management_prod
DB_USER=workshop_prod
DB_PASSWORD=YOUR_STRONG_PASSWORD

FLASK_ENV=production
FLASK_DEBUG=0

# CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Generate Strong JWT Secret**:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

### 4. Setup Gunicorn

```bash
# Create Gunicorn configuration
nano gunicorn_config.py
```

```python
import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/var/log/workshop/access.log"
errorlog = "/var/log/workshop/error.log"
loglevel = "info"

# Process naming
proc_name = "workshop-backend"

# Server mechanics
daemon = False
pidfile = "/var/run/workshop/gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None
```

### 5. Setup Systemd Service

```bash
sudo nano /etc/systemd/system/workshop-backend.service
```

```ini
[Unit]
Description=Workshop Management Backend
After=network.target mysql.service

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/workshop-backend
Environment="PATH=/var/www/workshop-backend/venv/bin"
ExecStart=/var/www/workshop-backend/venv/bin/gunicorn \
    --config gunicorn_config.py \
    run:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Create log directory
sudo mkdir -p /var/log/workshop
sudo chown www-data:www-data /var/log/workshop

# Create run directory
sudo mkdir -p /var/run/workshop
sudo chown www-data:www-data /var/run/workshop

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable workshop-backend
sudo systemctl start workshop-backend

# Check status
sudo systemctl status workshop-backend
```

### 6. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/workshop-backend
```

```nginx
upstream workshop_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Logging
    access_log /var/log/nginx/workshop-backend-access.log;
    error_log /var/log/nginx/workshop-backend-error.log;

    # Proxy settings
    location / {
        proxy_pass http://workshop_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/workshop-backend /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### 7. Setup SSL Certificate

```bash
# Obtain SSL certificate
sudo certbot --nginx -d api.yourdomain.com

# Auto-renewal is configured automatically
# Test renewal
sudo certbot renew --dry-run
```

---

## Frontend Deployment

### 1. Build Frontend

```bash
# On development machine or CI/CD
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Test build locally
npm start
```

### 2. Deploy to Server

```bash
# Create directory
sudo mkdir -p /var/www/workshop-frontend
sudo chown $USER:$USER /var/www/workshop-frontend

# Upload build
scp -r frontend/.next frontend/public frontend/package.json frontend/next.config.js \
    user@server:/var/www/workshop-frontend/

# Or use git
cd /var/www/workshop-frontend
git clone https://github.com/yourusername/workshop-management.git .
cd frontend
npm install
npm run build
```

### 3. Configure Environment

```bash
cd /var/www/workshop-frontend
nano .env.production
```

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

### 4. Setup PM2

```bash
cd /var/www/workshop-frontend/frontend

# Start with PM2
pm2 start npm --name "workshop-frontend" -- start

# Save PM2 configuration
pm2 save

# Setup PM2 startup
pm2 startup
# Follow the instructions provided

# Monitor
pm2 status
pm2 logs workshop-frontend
```

### 5. Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/workshop-frontend
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Logging
    access_log /var/log/nginx/workshop-frontend-access.log;
    error_log /var/log/nginx/workshop-frontend-error.log;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;

    # Proxy to Next.js
    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Cache static assets
    location /_next/static {
        proxy_pass http://127.0.0.1:3000;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }

    location /static {
        proxy_pass http://127.0.0.1:3000;
        add_header Cache-Control "public, max-age=31536000, immutable";
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/workshop-frontend /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx

# Setup SSL
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---

## Security Configuration

### Firewall Setup

```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow MySQL (only from localhost)
sudo ufw deny 3306/tcp

# Check status
sudo ufw status
```

### Fail2Ban Setup

```bash
# Install Fail2Ban
sudo apt install fail2ban -y

# Configure
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
logpath = /var/log/nginx/*error.log
```

```bash
# Start Fail2Ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Rate Limiting

Already configured in Nginx. Adjust as needed:

```nginx
# In nginx.conf or site config
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req zone=api_limit burst=20 nodelay;
```

---

## Monitoring and Logging

### Setup Monitoring

**Install Monitoring Tools**:
```bash
# Install htop
sudo apt install htop -y

# Install netdata (optional)
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

**Monitor Services**:
```bash
# Check backend status
sudo systemctl status workshop-backend

# Check frontend status
pm2 status

# Check Nginx status
sudo systemctl status nginx

# Check MySQL status
sudo systemctl status mysql

# View logs
sudo journalctl -u workshop-backend -f
pm2 logs workshop-frontend
sudo tail -f /var/log/nginx/workshop-backend-error.log
```

### Centralized Logging

**Setup Logrotate**:
```bash
sudo nano /etc/logrotate.d/workshop
```

```
/var/log/workshop/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        systemctl reload workshop-backend > /dev/null 2>&1 || true
    endscript
}
```

---

## Backup and Recovery

### Automated Backups

**Application Backup**:
```bash
#!/bin/bash
# /usr/local/bin/backup-workshop-app.sh

BACKUP_DIR="/var/backups/workshop-app"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup backend
tar -czf $BACKUP_DIR/backend_$DATE.tar.gz /var/www/workshop-backend

# Backup frontend
tar -czf $BACKUP_DIR/frontend_$DATE.tar.gz /var/www/workshop-frontend

# Keep only last 7 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

### Recovery Procedures

**Database Recovery**:
```bash
# Restore from backup
gunzip < /var/backups/workshop/workshop_20240101_020000.sql.gz | \
    mysql -u workshop_prod -p workshop_management_prod
```

**Application Recovery**:
```bash
# Stop services
sudo systemctl stop workshop-backend
pm2 stop workshop-frontend

# Restore files
tar -xzf /var/backups/workshop-app/backend_20240101_020000.tar.gz -C /
tar -xzf /var/backups/workshop-app/frontend_20240101_020000.tar.gz -C /

# Start services
sudo systemctl start workshop-backend
pm2 start workshop-frontend
```

---

## Scaling

### Vertical Scaling

1. Upgrade server resources (CPU, RAM)
2. Adjust Gunicorn workers
3. Increase MySQL connections
4. Optimize database queries

### Horizontal Scaling

**Load Balancer Setup**:
```nginx
upstream workshop_backend {
    least_conn;
    server backend1.internal:8000;
    server backend2.internal:8000;
    server backend3.internal:8000;
}
```

**Database Replication**:
- Setup MySQL master-slave replication
- Use read replicas for read-heavy operations
- Consider database clustering

**CDN Integration**:
- Use CloudFlare or AWS CloudFront
- Cache static assets
- Reduce server load

---

## Troubleshooting

### Common Issues

**Backend Not Starting**:
```bash
# Check logs
sudo journalctl -u workshop-backend -n 50

# Check if port is in use
sudo netstat -tulpn | grep 8000

# Test manually
cd /var/www/workshop-backend
source venv/bin/activate
gunicorn --bind 127.0.0.1:8000 run:app
```

**Database Connection Errors**:
```bash
# Test MySQL connection
mysql -u workshop_prod -p -h localhost workshop_management_prod

# Check MySQL status
sudo systemctl status mysql

# Check MySQL logs
sudo tail -f /var/log/mysql/error.log
```

**Nginx Errors**:
```bash
# Test configuration
sudo nginx -t

# Check error logs
sudo tail -f /var/log/nginx/error.log

# Restart Nginx
sudo systemctl restart nginx
```

**SSL Certificate Issues**:
```bash
# Renew certificate
sudo certbot renew

# Check certificate
sudo certbot certificates

# Test SSL
openssl s_client -connect yourdomain.com:443
```

---

## Post-Deployment

### Verification Checklist

- [ ] Backend API responding
- [ ] Frontend loading correctly
- [ ] User registration working
- [ ] User login working
- [ ] Workshop creation working
- [ ] Join requests working
- [ ] SSL certificate valid
- [ ] Monitoring active
- [ ] Backups running
- [ ] Logs rotating

### Performance Testing

```bash
# Install Apache Bench
sudo apt install apache2-utils -y

# Test API endpoint
ab -n 1000 -c 10 https://api.yourdomain.com/api/workshops

# Test frontend
ab -n 1000 -c 10 https://yourdomain.com/
```

### Monitoring Checklist

- [ ] Server CPU usage < 70%
- [ ] Server RAM usage < 80%
- [ ] Disk usage < 80%
- [ ] Database connections < max
- [ ] Response time < 500ms
- [ ] Error rate < 1%

---

## Maintenance

### Regular Tasks

**Daily**:
- Check error logs
- Monitor server resources
- Verify backups completed

**Weekly**:
- Review security logs
- Check SSL certificate expiry
- Update dependencies (if needed)

**Monthly**:
- Security updates
- Performance review
- Backup verification
- Database optimization

### Update Procedure

1. Test updates in staging environment
2. Notify users of maintenance window
3. Create backup
4. Stop services
5. Update code/dependencies
6. Run migrations
7. Start services
8. Verify functionality
9. Monitor for issues

---

**Need Help?** Contact your system administrator or create an issue on GitHub.
