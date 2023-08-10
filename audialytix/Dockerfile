FROM python:3.10

COPY . /audialytix/

WORKDIR /audialytix/

RUN pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic

# Configure database first
ENTRYPOINT python manage.py migrate && daphne audialytix.asgi:application -p $PORT -b $HOST
