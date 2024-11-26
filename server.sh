#!/bin/bash

source env/bin/activate
# Replace 'your_project_name' with the actual name of your Django project
project_name="LAB"

# Make migrations
python manage.py makemigrations

# Migrate changes
python manage.py migrate

# Run the development server
python manage.py runserver