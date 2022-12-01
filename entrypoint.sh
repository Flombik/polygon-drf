#!/bin/sh
python manage.py collectstatic --no-input
python manage.py migrate
wget -qO- https://raw.githubusercontent.com/eficode/wait-for/v2.2.3/wait-for | sh -s -- $DB_HOST:$DB_PORT
exec "$@"
