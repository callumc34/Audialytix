FROM python:3.10

COPY . /analyser/

WORKDIR /analyser/

RUN pip install -r requirements.txt

ENTRYPOINT uvicorn server:app --reload --port $PORT --host $HOST --log-level info
