#!/bin/sh

prefect server start --port=4200 --host=0.0.0.0 &
cd processor && gunicorn -c gunicorn.conf.py app:APP &

wait