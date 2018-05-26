#-*- coding:UTF-8 -*-

from flask import redirect
from flask import request
from flask_restful import Api
from flask_restful import Resource

from datetime import datetime
from random import choice
from string import ascii_lowercase
from string import digits
from time import sleep
from user_agents import parse as ua__parse

from settings import *
from app.utils import *
from app import check__filter


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
    # - validate__IP
    # - IP
    # - validate__UA
    # - UA
    # - validate__transaction__time
    # - transaction__time
    def get(self):

        transaction_key = "%s" % (''.join(choice(ascii_lowercase + digits) for _ in range(6)))
        transaction_id = "%s-%s" % (datetime.utcnow().strftime('%s'), transaction_key)
        connection, database = getDatabase()
        table = database["transaction"]
        transactionRaw = {
            'id': transaction_id,
            'score': 0,
            'progress': 0,
            'details': {},
        }
        table.insert_one(transactionRaw)
        filters = 0
        validate__IP = request.args.get('validate__IP', 1)
        try:
            validate__IP = int(validate__IP)
        except:
            pass
        IP = request.args.get('IP', '')
        buyer__country = request.args.get('buyer__country', '')
        if validate__IP:
            if IP == "":
                IP = getIP(request)
            filters = filters + 1
            check__filter.delay(FILTERS__URL["IP"], transaction_id, "IP", {"IP": IP, "buyer__country": buyer__country})
        validate__UA = request.args.get('validate__UA', 1)
        try:
            validate__UA = int(validate__UA)
        except:
            pass
        UA = request.args.get('UA', '')
        if validate__UA:
            if UA == "":
                UA = getUA(request)
            filters = filters + 1
            check__filter.delay(FILTERS__URL["UA"], transaction_id, "UA", {"UA": UA})
        validate__transaction__time = request.args.get('validate__transaction__time', 1)
        try:
            validate__transaction__time = int(validate__transaction__time)
        except:
            pass
        transaction__time = request.args.get('transaction__time', '')
        if validate__transaction__time:
            try:
                transaction__time = int(transaction__time)
                filters = filters + 1
                check__filter.delay(FILTERS__URL["transaction__time"], transaction_id, "transaction__time", {"transaction__time": transaction__time})
            except:
                pass
        table.update_one({
            'id': transaction_id
        }, {
            '$set': {
                "total": filters,
            }
        }, upsert = False)
        request__duration = 0
        request__completed = False
        while request__duration < 10 and not request__completed:
            item = table.find_one({
                "id": transaction_id,
            })
            if item["progress"] == item["total"]:
                request__completed = True
            if not request__completed:
                request__duration = request__duration + 1            
                sleep(1)
        item = table.find_one({
            "id": transaction_id,
        })
        item.pop("_id")
        return render_to_json(item, 201)


class ValidateDetailsView(Resource):
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
        item.pop('_id')
        return render_to_json(item)


class FiltersIPView(Resource):
    # - IP
    # - buyer__country
    def get(self):

        IP = request.args.get('IP', '')
        buyer__country = request.args.get('buyer__country', '')
        context = {
            "success": False,
        }
        matchedIP = geoip__information(IP)
        if matchedIP is None or matchedIP.location is None:
            context = {
               "success": False,
            }
            return render_to_json(context, 200)

        if matchedIP.country != buyer__country:
            context = {
               "success": True,
            }
            return render_to_json(context, 201)
        context["raw"] = {
            "reason": "País del comercio es % y país del pagador es %s" % (buyer__country, matchedIP.country),
            "country": matchedIP.country,
            "timezone": matchedIP.timezone,
        }
        return render_to_json(context, 201)


class FiltersUAView(Resource):
    # - UA
    def get(self):

        UA = request.args.get('UA', '')
        context = {
            "success": False,
        }
        UA__parsed = ua__parse(UA)
        if UA__parsed.is_bot:
            context = {
               "success": True,
               "raw": {
                   "reason": "UA es %s, al parecer es un bot" % (UA),
               }
            }
            return render_to_json(context, 201)
        context["raw"] = {
            "reason": "UA es %s, al parecer no es un bot" % (UA),
        }
        return render_to_json(context, 201)


class FiltersTransactionTimeView(Resource):
    # - UA
    def get(self):

        transaction__time = request.args.get('transaction__time', '')
        context = {
            "success": False,
        }
        try:
            transaction__time = int(transaction__time)
        except:
            context = {
                "success": False,
            }
            return render_to_json(context, 200)
        if transaction__time < 3: # a bot can do a buy in less than 3 seconds
            context = {
                "success": True,
            }
            return render_to_json(context, 201)
        context["raw"] = {
            "reason": "La transacción fue hecha en %s segundos" % transaction__time,
        }
        return render_to_json(context, 201)
