#!/bin/bash

# Quick MySQL Setup Script for Workshop Management System

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Workshop Management System - MySQL Quick Setup          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo -e "${RED}✗${NC} MySQL is not installed"
    echo ""
    echo "Please install MySQL first:"
    echo "  macOS:   brew install mysql"
    echo "  Ubuntu:  sudo apt install mysql-server"
    echo "  Windows: Download from https://dev.mysql.com/downloads/mysql/"
    exit 1
fi

echo -e "${GREEN}✓${NC} MySQL is installed"

# Check if MySQL is running
if ! mysqladmin ping -h localhost --silent 2>/dev/null; then
    echo -e "${YELLOW}⚠${NC} MySQL server is not running"
    echo ""
    echo "Starting MySQL..."
    
    # Try to start MySQL
    if command -v brew &> /dev/null; then
        brew services start mysql
    elif command -v systemctl &> /dev/null; then
        sudo systemctl start mysql
    else
        echo -e "${RED}✗${NC} Could not start MySQL automatically"
        echo "Please start MySQL manually and run this script again"
        exit 1
    fi
    
    sleep 2
fi

echo -e "${GREEN}✓${NC} MySQL server is running"
echo ""

# Prompt for MySQL credentials
echo -e "${BLUE}MySQL Configuration${NC}"
echo "Please enter your MySQL credentials:"
echo ""

read -p "MySQL Host [localhost]: " DB_HOST
DB_HOST=${DB_HOST:-localhost}

read -p "MySQL Port [3306]: " DB_PORT
DB_PORT=${DB_PORT:-3306}

read -p "MySQL User [root]: " DB_USER
DB_USER=${DB_USER:-root}

read -sp "MySQL Password: " DB_PASSWORD
echo ""

read -p "Database Name [workshop_management]: " DB_NAME
DB_NAME=${DB_NAME:-workshop_management}

echo ""

# Test connection
echo "Testing MySQL connection..."
if mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1" &>/dev/null; then
    echo -e "${GREEN}✓${NC} MySQL connection successful"
else
    echo -e "${RED}✗${NC} MySQL connection failed"
    echo "Please check your credentials and try again"
    exit 1
fi

# Create database if it doesn't exist
echo ""
echo "Creating database '$DB_NAME'..."
mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" -p"$DB_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Database created/verified"
else
    echo -e "${RED}✗${NC} Failed to create database"
    exit 1
fi

# Update .env file
echo ""
echo "Updating .env file..."

if [ ! -f .env ]; then
    cp .env.example .env
fi

# Update database configuration in .env
sed -i.bak "s/^DB_HOST=.*/DB_HOST=$DB_HOST/" .env
sed -i.bak "s/^DB_PORT=.*/DB_PORT=$DB_PORT/" .env
sed -i.bak "s/^DB_NAME=.*/DB_NAME=$DB_NAME/" .env
sed -i.bak "s/^DB_USER=.*/DB_USER=$DB_USER/" .env
sed -i.bak "s/^DB_PASSWORD=.*/DB_PASSWORD=$DB_PASSWORD/" .env

rm .env.bak 2>/dev/null || true

echo -e "${GREEN}✓${NC} .env file updated"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install -q mysql-connector-python

echo -e "${GREEN}✓${NC} Dependencies installed"

# Initialize database schema
echo ""
echo "Initializing database schema..."
python init_db.py

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              ✓ MySQL Setup Complete!                      ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Database: $DB_NAME"
    echo "Host: $DB_HOST:$DB_PORT"
    echo "User: $DB_USER"
    echo ""
    echo "You can now start the application:"
    echo "  python run.py"
    echo ""
else
    echo -e "${RED}✗${NC} Failed to initialize database schema"
    exit 1
fi
