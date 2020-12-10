#!/bin/bash

pip install -r requirements.txt

./manage.py compose build web

./manage.py flask db init

./manage.py compose up -d

./manage.py create-initial-db

./manage.py flask db migrate

./manage.py flask db upgrade

