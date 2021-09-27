release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input
release: python manage.py loaddata Factions --no-input
release: python manage.py loaddata Settlements --no-input
release: python manage.py loaddata Servers --no-input
release: python manage.py loaddata Items --no-input
release: python manage.py loaddata users --no-input
release: python manage.py loaddata Tokens --no-input
release: python manage.py loaddata GameUsers --no-input
release: python manage.py loaddata Posts --no-input
release: python manage.py loaddata Messages --no-input

web: gunicorn newworld.wsgi
