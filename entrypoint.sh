#!/bin/sh

# Wait for the database to be ready
# You might need to customize this for your database and wait strategy
echo "Waiting for database to be ready..."
while ! nc -z db 5432; do
  sleep 1
done

# Apply database migrations
echo "Making database migrations..."
python manage.py makemigrations

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Populate Database with Fake Data
echo "Populating DataBase..."
python manage.py populate_users 1000

# Start the Django server
echo "Starting the server..."
exec python manage.py runserver 0.0.0.0:8000
