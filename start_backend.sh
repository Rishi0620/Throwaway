#!/bin/bash

# Start backend server for Trading Scripts Web App

echo "Starting Trading Scripts Web App Backend..."
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "Error: backend/.env not found"
    echo "Run: cp backend/.env.example backend/.env"
    echo "Then edit backend/.env with your configuration"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    cd backend
    pip3 install -r requirements.txt
    cd ..
fi

# Start the server
echo "Starting Flask server on port 5000..."
echo ""
echo "Access the app at:"
echo "  Backend API: http://localhost:5000/api/health"
echo "  Frontend: Open frontend/index.html in your browser"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd backend
python3 app.py
