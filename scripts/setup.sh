#!/bin/bash

# Setup Script for NTT Data Regulatory Reporting System
# This script sets up the development environment

set -e  # Exit on error

echo "========================================="
echo "NTT Data Regulatory Reporting System"
echo "Development Environment Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.11+ is required. Found: $python_version"
    exit 1
fi
echo "Python version OK: $python_version"
echo ""

# Check Node.js version
echo "Checking Node.js version..."
node_version=$(node --version 2>&1 | sed 's/v//')
required_node="18"

if [ "$(printf '%s\n' "$required_node" "$node_version" | sort -V | head -n1)" != "$required_node" ]; then
    echo "Error: Node.js 18+ is required. Found: $node_version"
    exit 1
fi
echo "Node.js version OK: v$node_version"
echo ""

# Check PostgreSQL
echo "Checking PostgreSQL..."
if ! command -v psql &> /dev/null; then
    echo "Warning: PostgreSQL client not found. Please install PostgreSQL 14+"
else
    psql_version=$(psql --version | awk '{print $3}')
    echo "PostgreSQL version: $psql_version"
fi
echo ""

# Setup Backend
echo "========================================="
echo "Setting up Backend"
echo "========================================="
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit backend/.env with your configuration"
fi

cd ..

# Setup Frontend
echo ""
echo "========================================="
echo "Setting up Frontend"
echo "========================================="
cd frontend

# Install dependencies
echo "Installing npm dependencies..."
npm install

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please edit frontend/.env with your configuration"
fi

cd ..

# Create storage directories
echo ""
echo "========================================="
echo "Creating Storage Directories"
echo "========================================="
mkdir -p storage/documents/{fca,pra,boe}
mkdir -p storage/reports/{submissions,validation}
mkdir -p storage/audit_logs
mkdir -p storage/generated_code/{sql,python}
mkdir -p storage/graphrag/{graphs,communities,entities,analysis}
mkdir -p storage/embeddings/{vectors,tiktoken_cache,indexes}
mkdir -p storage/workflows/{definitions,executions,state,history}
mkdir -p storage/backups/{daily,weekly,monthly}
mkdir -p storage/temp/{uploads,processing}
mkdir -p chroma_db

echo "Storage directories created"
echo ""

# Database setup reminder
echo "========================================="
echo "Database Setup"
echo "========================================="
echo "Please ensure PostgreSQL is running and create the database:"
echo ""
echo "  createdb regulatory_reporting"
echo ""
echo "Or using psql:"
echo "  psql -U postgres"
echo "  CREATE DATABASE regulatory_reporting;"
echo ""

# Final instructions
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Configure environment variables:"
echo "   - backend/.env"
echo "   - frontend/.env"
echo ""
echo "2. Create PostgreSQL database:"
echo "   createdb regulatory_reporting"
echo ""
echo "3. Start the backend (auto-initializes database):"
echo "   cd backend"
echo "   python app.py"
echo ""
echo "4. Start the frontend (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "5. Access the application:"
echo "   - Frontend: http://localhost:5173"
echo "   - Backend API: http://localhost:8000/api/v1/docs"
echo ""
echo "Default admin credentials:"
echo "   Email: admin@example.com"
echo "   Password: admin123"
echo ""
echo "========================================="
