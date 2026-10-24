# Deployment notes (Amrin — finish in Week 4)
Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, `ALLOWED_HOSTS=yourdomain`. Run `python manage.py collectstatic` and serve with gunicorn + a static file server.
