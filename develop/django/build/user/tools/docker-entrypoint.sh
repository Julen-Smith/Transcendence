#!/bin/sh

service=user
project=transcendence

if [ ! -d "/app/$service" ]; then

    echo "$service project not found!"
    mkdir -p /app/$service
    django-admin startproject $project /app
    django-admin startapp $service /app/$service
    touch /app/$project/api.py
    touch /app/$service/api.py
    touch /app/$service/models.py
    touch /app/$service/schemas.py
    touch /app/$service/crud.py

else
    echo "$service project found"
fi

exec python /app/manage.py runserver 0.0.0.0:22748