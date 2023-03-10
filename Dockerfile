FROM python:3.10-alpine3.13
LABEL maintainer="Parthiban Baskar"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /resistor && \
    /resistor/bin/pip install --upgrade pip && \
    apk add --update --no-cache gcc musl-dev python3-dev libffi-dev openssl-dev cargo && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    /resistor/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ] ; then \
    /resistor/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
    --disabled-password \
    --no-create-home \
    django-user

ENV PATH="/resistor/bin:$PATH"

USER django-user