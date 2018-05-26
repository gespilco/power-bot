#-*- coding:UTF-8 -*-

from flask import redirect
from flask import request
from flask_restful import Api
from flask_restful import Resource

from datetime import datetime
from random import choice
from string import ascii_lowercase
from string import digits

from settings import *
from app.utils import *


class MainView(Resource):
    
    def get(self):
        
        context = {
            'version': STAGE,
        }
        return render_to_json(context)


class PingView(Resource):
    
    def get(self):

        context = {
            'message': 'pong',
            'version': STAGE,
            'time': int(datetime.utcnow().strftime('%s')),
        }
        return render_to_json(context)


class ValidateView(Resource):    
    # QUERY:
    # - mail
    # - IP
    def get(self):

        transaction_key = "%s" % (''.join(choice(ascii_lowercase + digits) for _ in range(6)))
        transaction_id = "%s-%s" % (datetime.utcnow().strftime('%s'), transaction_key)
        connection, database = getDatabase()
        table = database["transaction"]
        transactionRaw = {
            'id': transaction_id,
        }
        table.insert_one(transactionRaw)
        context = {
            "id": transaction_id,
        }
        return render_to_json(context, 201)


class ValidateDetailsView(Resource):
    # QUERY:
    # - id
    def get(self):

        id = request.args.get('id', '')
        connection, database = getDatabase()
        table = database["transaction"]
        item = table.find_one({
            "id": id 
        })
        if item == None:
            context = {
            }
            return render_to_json(context, 404)
        context.pop('_id')
        return render_to_json(context)
