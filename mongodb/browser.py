#!/usr/bin/env python2.7
# -*- coding: UTF-8 -*-


from pymongo import *

client = MongoClient("localhost", 27017)
db = client["vin"]
collection = db["vin"]

for document in collection.find():
    if document.has_key("vinLong"):
        print document["vinLong"]
