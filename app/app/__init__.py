#-*- coding:UTF-8 -*-

from flask import jsonify
from flask import Flask
from flask_restful import Api
from flask_restful import Resource

from celery import Celery
from requests import Session

from app.utils import *
from settings import *


app = Flask(__name__)
app.config.from_object('settings')

api = Api(app)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)


@celery.task()
def check__filter(URL, transaction__id, filter__id, params):

    session = Session()
    response = session.get(
        URL,
        params = params,
        verify = False,
        timeout = 5
    )
    if response.status_code != 201:
        return False
    raw = response.json()
    connection, database = getDatabase()
    table = database["transaction"]
    score = 0
    if raw["success"]:
        score = FILTERS__SCORE[filter__id]
    raw__details = {}
    if "raw" in raw:
        raw__details = raw["raw"]
    table.update_one({
        'id': transaction__id
    }, {
        '$inc': {
            'score': score,
            'progress': 1,
        },
        '$set': {
            'details.%s' % filter__id: raw__details,
        },
    }, upsert = False)
    return True


@app.after_request
def after_request(response):
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.errorhandler(404)
def view404(error):
    
    context = {
    }
    return render_to_json(context, 404)


@app.errorhandler(500)
def view500(error):
    
    context = {
    }
    return render_to_json(context, 500)


## URLs

from .views import MainView
from .views import PingView
from .views import ValidateView
from .views import ValidateDetailsView
from .views import FiltersIPView
from .views import FiltersUAView
from .views import FiltersTransactionTimeView

api.add_resource(MainView                  , '/')
api.add_resource(PingView                  , '/ping/')
api.add_resource(ValidateView              , '/validate/')
api.add_resource(ValidateDetailsView       , '/validate/details/')
api.add_resource(FiltersIPView             , '/filters/IP/')
api.add_resource(FiltersUAView             , '/filters/UA/')
api.add_resource(FiltersTransactionTimeView, '/filters/transaction__time/')
