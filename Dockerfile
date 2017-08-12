FROM python:3.6-alpine
MAINTAINER Anatoly Serebryansky <solartune@rambler.ru>
RUN apk add --update gcc g++ python3-dev musl-dev linux-headers git \
    && rm -rf /var/cache/apk/*

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . /usr/src/app

RUN adduser -D -g '' async

EXPOSE 8000

ENTRYPOINT ["sh_scripts/entrypoint.sh"]
