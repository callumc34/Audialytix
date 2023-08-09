FROM python:3.10

EXPOSE $PORT

COPY . /audialytix/

WORKDIR /audialytix/

RUN pip install -r requirements.txt

ENTRYPOINT daphne audialytix.asgi:application -p $PORT -b $HOST
