#!/bin/sh

# Применяем миграции
python manage.py migrate

# Запускаем сервер
python manage.py runserver 0.0.0.0:8000