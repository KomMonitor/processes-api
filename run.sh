#!/bin/sh

cd processor && gunicorn -c gunicorn.conf.py --workers 2 --worker-connections 100 --threads 2 app:APP &
wait