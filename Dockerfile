# Dockerfile

# python base image
FROM python:3.10-alpine

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collecting static
RUN python3 manage.py collectstatic --noinput

# migrating
RUN find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
RUN find . -path "*/migrations/*.pyc"  -delete
RUN echo "from django.db.migrations.recorder import MigrationRecorder;MigrationRecorder.Migration.objects.filter(app='main').delete()" | python3 manage.py shell 
RUN python manage.py makemigrations main
RUN python manage.py migrate --fake main zero
RUN python manage.py migrate --fake

# run gunicorn
CMD daphne drp.asgi:application --port $PORT --bind 0.0.0.0
