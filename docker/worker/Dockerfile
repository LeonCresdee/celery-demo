FROM python:3.12-alpine

# Install FFMPEG
RUN apk update
RUN apk upgrade
RUN apk add --no-cache \
    ffmpeg \
    postgresql-libs \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev 

RUN apk add --no-cache postgresql-libs

WORKDIR /fumnail/worker

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

COPY . .

CMD ["celery", "worker"]