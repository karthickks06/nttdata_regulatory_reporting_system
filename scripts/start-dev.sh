#!/bin/bash

# Development Start Script
# Starts both backend and frontend in development mode

set -e

echo "========================================="
echo "Starting NTT Data Regulatory Reporting System"
echo "Development Mode"
echo "========================================="
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT TERM

# Check if PostgreSQL is running
echo "Checking PostgreSQL..."
if ! pg_isready -q; then
    echo "Error: PostgreSQL is not running"
    echo "Please start PostgreSQL and try again"
    exit 1
fi
echo "PostgreSQL is running"
echo ""

# Start Backend
echo "Starting Backend..."
cd backend

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Error: Virtual environment not found. Run setup.sh first"
    exit 1
fi

# Start backend in background
python app.py &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"
echo ""

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:8000/api/v1/docs > /dev/null 2>&1; then
        echo "Backend is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Error: Backend failed to start"
        kill $BACKEND_PID
        exit 1
    fi
    sleep 1
done
echo ""

cd ..

# Start Frontend
echo "Starting Frontend..."
cd frontend

npm run dev &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"
echo ""

cd ..

# Display status
echo "========================================="
echo "Services Running"
echo "========================================="
echo ""
echo "Backend:"
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/api/v1/docs"
echo "  - PID: $BACKEND_PID"
echo ""
echo "Frontend:"
echo "  - URL: http://localhost:5173"
echo "  - PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all services"
echo "========================================="
echo ""

# Wait for user interrupt
wait
