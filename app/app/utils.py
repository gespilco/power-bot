# -*- coding:utf-8 -*-

from flask import jsonify

from pymongo import MongoClient

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
