#!/bin/bash

# Start backend server in production mode with Gunicorn

echo "Starting Trading Scripts Web App (Production Mode)..."
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "Error: backend/.env not found"
    exit 1
fi

# Check if gunicorn is installed
if ! python3 -c "import gunicorn" 2>/dev/null; then
    echo "Installing gunicorn..."
    pip3 install gunicorn
fi

# Number of workers (2-4 x CPU cores)
WORKERS=${WORKERS:-4}
PORT=${PORT:-5000}

echo "Starting Gunicorn with $WORKERS workers on port $PORT..."
echo "Access the API at: http://localhost:$PORT/api/health"
echo ""

cd backend
gunicorn -w $WORKERS -b 0.0.0.0:$PORT --access-logfile - --error-logfile - app:app
