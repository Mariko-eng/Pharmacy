#!/bin/bash

pwd 
# Collect static files
echo "Collect static files"
python3 manage.py collectstatic --settings=pharmacy.settings.development --clear --no-input

# Apply database migrations
echo "Apply database migrations"
python3 manage.py makemigrations --settings=pharmacy.settings.development

python3 manage.py migrate --settings=pharmacy.settings.development

# Setup currencies using management command
python3 manage.py setup_app_defaults
python3 manage.py setup_app_groups

# Start server
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000 --settings=pharmacy.settings.development
