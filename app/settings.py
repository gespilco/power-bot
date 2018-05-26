#-*- coding:UTF-8 -*-

from os.path import dirname


##
## App
##

SERVER = 'power-bot'
SECRET_KEY = '*i-l07*decs8l2=5ee9kdm7eudw9x*^4zhhb+^----power-bot'
BASE_DIR = dirname(__file__)
DEBUG = False
BUNDLE_ERRORS = True


##
## env
##

STAGE = 1
FILTERS__URL = {
    "IP": "http://0.0.0.0:5000/filters/IP/",
    "UA": "http://0.0.0.0:5000/filters/UA/",
    "transaction__time": "http://0.0.0.0:5000/filters/transaction__time/",
}
FILTERS__SCORE = {
    "IP": 30,
    "UA": 20,
    "transaction__time": 40,
}


##
## data
##

MONGO__DATABASE__SERVER = "127.0.0.1"
MONGO__DATABASE__PORT = 27017


##
## Local settings
##

try:
    from local_settings import *
except ImportError:
    pass

