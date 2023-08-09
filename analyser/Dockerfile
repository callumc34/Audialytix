FROM python:3.10

ENV HOST 0.0.0.0
ENV PORT 8000
ENV DEBUG True
ENV PRODUCTION True

EXPOSE $PORT

COPY . /analyser/

WORKDIR /analyser/

RUN pip install -r requirements.txt

ENTRYPOINT uvicorn server:app --reload --port $PORT --host 0.0.0.0 --log-level info
