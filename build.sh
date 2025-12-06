#!/bin/bash

# Install frontend dependencies
echo "Installing frontend dependencies..."
npm install --prefix frontend

# Build frontend
echo "Building frontend..."
npm run build --prefix frontend

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

# Run Django migrations
echo "Running migrations..."
cd backend
python manage.py migrate
cd ..

echo "Build completed successfully!"
