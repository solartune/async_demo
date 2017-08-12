#!/bin/sh
kill -HUP `ps aux |grep gunicorn |grep application.main:app |awk '{ print $1 }'`
