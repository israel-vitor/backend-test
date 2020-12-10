#!/bin/bash

pip install -r requirements.txt

python prepare_env.py

./manage.py compose build web

./manage.py flask db init

./manage.py compose up -d

./manage.py create-initial-db

./manage.py flask db migrate

./manage.py flask db upgrade

python update_env.py

./manage.py compose down

./manage.py compose up -d
