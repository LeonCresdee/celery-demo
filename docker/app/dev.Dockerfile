FROM python:3.12-alpine

WORKDIR /fumnail/app

RUN apk update
RUN apk upgrade

RUN apk add --no-cache nginx

# Install postgresql deps
RUN apk add --no-cache \
    postgresql-libs \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev \
    postgresql-libs


COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

ENV FLASK_DEBUG=1


CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]