FROM python:3.10

COPY . /audialytix/

WORKDIR /audialytix/

RUN pip install -r requirements.txt

# Configure database first
ENTRYPOINT python manage.py migrate \
    && python manage.py collectstatic --noinput \
    && python manage.py compress \
    && uvicorn audialytix.asgi:application --reload --port $PORT --host $HOST
