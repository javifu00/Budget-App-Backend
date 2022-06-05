web: gunicorn budgetbackend.wsgi
worker: python worker.py
release: python manage.py makemigrations --noinput
release: python manage.py collectstatic --noinput
release: python manage.py migrate --noinput