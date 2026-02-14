#!/bin/sh
set -e

# Add current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:.

# Check for existing migrations
count=$(ls -1 alembic/versions/*.py 2>/dev/null | wc -l)
if [ "$count" = "0" ]; then
    echo "No migrations found. Generating initial migration..."
    alembic revision --autogenerate -m "Initial migration"
else
    echo "Checking for model changes..."
    # Attempt to generate a new migration
    alembic revision --autogenerate -m "auto_migration_$(date +%Y%m%d_%H%M%S)"
fi

# Run migrations
echo "Running migrations..."
alembic upgrade head

# Create initial data
echo "Creating initial data..."
python initial_data.py

# Start application
echo "Starting application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
