# -*- coding:utf-8 -*-

from pymongo import ASCENDING
from pymongo import DESCENDING
from pymongo import HASHED

from app.utils import getDatabase


connection, database = getDatabase()
table = database["transaction"]
table.create_index([("id", ASCENDING)], background = True)
