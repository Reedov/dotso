#!/bin/bash
chmod 777 /tmp
python manage.py makemigrations
python manage.py migrate
python manage.py runserver