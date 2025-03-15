#!/bin/bash

echo "🚀 Running Migrations..."
python manage.py migrate

echo "📦 Collecting Static Files..."
python manage.py collectstatic --noinput
