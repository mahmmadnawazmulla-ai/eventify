# Eventify
pip install -r requirements.txt
python manage.py migrate
python manage.py seed            # sample data
python manage.py createsuperuser # admin (is_staff) account
python manage.py runserver       # http://127.0.0.1:8000
