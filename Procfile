web: gunicorn ProjectY.wsgi --log-file -
release: python3 manage.py makemigrations core
release: python3 manage.py makemigrations accounts
release: python3 manage.py makemigrations
release: python3 manage.py migrate
