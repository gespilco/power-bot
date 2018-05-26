# -*- coding: utf-8 -*-

###
### gunicorn WSGI server configuration
###

from multiprocessing import cpu_count
from os import environ


def max_workers():
    
    return cpu_count() + 1


name = 'power-bot'
pythonpath = '/home/ubuntu/power-bot/app/'
bind = '0.0.0.0:5000'
loglevel = 'error'

limit_request_line = 0
max_requests = 1000
worker_class = 'gevent'
workers = max_workers()

timeout = 300
