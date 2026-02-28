#!/bin/bash

# Quick MySQL Setup Script for Workshop Management System

echo "============================================================"
echo "Workshop Management System - MySQL Quick Setup"
echo "============================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo -e "${RED}✗${NC} MySQL is not installed"
    echo ""
    echo "Install MySQL:"
    echo "  macOS:   brew install mysql"
    echo "  Ubuntu:  sudo apt install mysql-server"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓${NC} MySQL is installed"
echo ""

# Prompt for MySQL root password
echo -e "${BLUE}Enter MySQL root password:${NC}"
read -s MYSQL_ROOT_PASSWORD
echo ""

# Test MySQL connection
echo "Testing MySQL connection..."
if ! mysql -u root -p"$MYSQL_ROOT_PASSWORD" -e "SELECT 1;" &> /dev/null; then
    echo -e "${RED}✗${NC} Failed to connect to MySQL"
    echo "Please check your password and try again"
    exit 1
fi

echo -e "${GREEN}✓${NC} MySQL connection successful"
echo ""

# Create database
echo "Creating database 'workshop_management'..."
mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<EOF
CREATE DATABASE IF NOT EXISTS workshop_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Database created"
else
    echo -e "${RED}✗${NC} Failed to create database"
    exit 1
fi

echo ""

# Ask if user wants to create a dedicated database user
echo -e "${YELLOW}Do you want to create a dedicated database user? (recommended) [y/N]${NC}"
read -r CREATE_USER

if [[ $CREATE_USER =~ ^[Yy]$ ]]; then
    echo ""
    echo -e "${BLUE}Enter username for database user:${NC} (default: workshop_user)"
    read DB_USER
    DB_USER=${DB_USER:-workshop_user}
    
    echo -e "${BLUE}Enter password for database user:${NC}"
    read -s DB_PASSWORD
    echo ""
    
    echo "Creating database user '$DB_USER'..."
    mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<EOF
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL PRIVILEGES ON workshop_management.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
EOF
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Database user created"
        USE_ROOT=false
    else
        echo -e "${RED}✗${NC} Failed to create database user"
        echo "Will use root user instead"
        USE_ROOT=true
        DB_USER="root"
        DB_PASSWORD="$MYSQL_ROOT_PASSWORD"
    fi
else
    USE_ROOT=true
    DB_USER="root"
    DB_PASSWORD="$MYSQL_ROOT_PASSWORD"
fi

echo ""

# Update .env file
echo "Updating .env file..."

if [ -f ".env" ]; then
    # Backup existing .env
    cp .env .env.backup
    echo -e "${YELLOW}⚠${NC} Backed up existing .env to .env.backup"
fi

# Update or create .env
cat > .env <<EOF
# JWT Configuration
JWT_SECRET_KEY=$(openssl rand -base64 32)
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=workshop_management
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
EOF

echo -e "${GREEN}✓${NC} .env file updated"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
if pip install -r requirements.txt > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC} Python dependencies installed"
else
    echo -e "${RED}✗${NC} Failed to install Python dependencies"
    echo "Please run: pip install -r requirements.txt"
fi

echo ""

# Initialize database schema
echo "Initializing database schema..."
if python init_db.py; then
    echo ""
    echo -e "${GREEN}✓${NC} Database setup complete!"
else
    echo -e "${RED}✗${NC} Failed to initialize database"
    exit 1
fi

echo ""
echo "============================================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "============================================================"
echo ""
echo "Database Configuration:"
echo "  Host:     localhost"
echo "  Port:     3306"
echo "  Database: workshop_management"
echo "  User:     $DB_USER"
echo ""
echo "Next steps:"
echo "  1. Run tests:  PYTHONPATH=. pytest tests/ -v"
echo "  2. Start app:  python run.py"
echo ""
