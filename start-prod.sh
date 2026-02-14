#!/bin/sh
set -e

# Add current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# Run migrations
echo "Running migrations..."
alembic upgrade head

# Create initial data
echo "Creating initial data..."
# Use || true to prevent startup failure if this script fails (e.g. data unique constraint)
python initial_data.py || true

# Start application
echo "Starting application on port ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
