release: python olist_api_django/manage.py migrate
release: python olist_api_django/manage.py import_authors 2500_authors.csv
web: python olist_api_django/manage.py runserver 0.0.0.0:$PORT