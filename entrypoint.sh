#!/bin/sh


echo "Starting entrypoint.sh script"
sleep 3

echo "my-postgres:5432:postgres:postgres:mypassword" > ~/.pgpass
chmod 600 ~/.pgpass

python manage.py makemigrations 
python manage.py migrate


exec "$@"
