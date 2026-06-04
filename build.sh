#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py migrate

python manage.py collectstatic --no-input

# Parol bilan birga yaratish:
DJANGO_SUPERUSER_PASSWORD='ahrorbek123456789' python manage.py createsuperuser --no-input --username=admin --email=admin@gmail.com
