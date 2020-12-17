FROM python:3.8.5

WORKDIR /code

COPY . /code

RUN pip install pip --upgrade && pip install -r requirements.txt

RUN python manage.py collectstatic --noinput

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:5000
