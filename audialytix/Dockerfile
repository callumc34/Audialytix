FROM python:3.10

ENV PORT 80
ENV HOST 0.0.0.0
ENV DJANGO_SECRET_KEY "django-insecure-#6l*)qe#e-qq#kf@18m(e-34tg7^pikd81v0(+vupy)w%7mlln"
ENV DJANGO_DEBUG False

ENV MONGO_HOST mongodb://127.0.0.1:27017
ENV MONGO_PORT 27017
ENV MONGO_USERNAME audialytix-root
ENV MONGO_PASSWORD insecure

EXPOSE $PORT

COPY . /audialytix/

WORKDIR /audialytix/

RUN pip install -r requirements.txt

ENTRYPOINT daphne audialytix.asgi:application -p $PORT -b $HOST
