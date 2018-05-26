# -*- coding:utf-8 -*-

from flask import jsonify
from geoip import open_database as geoip__database__open
from pymongo import MongoClient
from os import path as os__path

from settings import *


class MongoConnection(object): # singleton
    
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = MongoClient(MONGO__DATABASE__SERVER, MONGO__DATABASE__PORT, maxPoolSize = 200, waitQueueTimeoutMS = 100)
        return cls._instance


def getDatabase():
    
    connection = MongoConnection()
    database = connection["power-bot-%s" % STAGE]
    return connection, database


def render_to_json(context, status = 200):
    
    response = jsonify(context)
    response.status_code = status
    return response


def getIP(request):
    
    IP = ""
    if 'HTTP_X_FORWARDED_FOR' in request.environ:
        IP = request.environ['HTTP_X_FORWARDED_FOR']
    else:
        if 'REMOTE_ADDR' in request.environ:
            IP = request.environ['REMOTE_ADDR']
    return IP


def getUA(request):
    
    UA = ""
    HTTP_USER_AGENT = request.headers.get('User-Agent')
    if HTTP_USER_AGENT:
        UA = HTTP_USER_AGENT
    return UA




##
## To get information about a IP
##
geoip__database = geoip__database__open(os__path.dirname(os__path.realpath(__file__)) + '/../GeoLite2-City.mmdb')


def geoip__information(IP):
    
    return geoip__database.lookup(IP)
