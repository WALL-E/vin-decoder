#!/usr/bin/python

from pymongo import *
import json


class Mongo():
    def __init__(self, host="localhost", port=27017):
        self.host = host
        self.port = port

    def query_vin(self, vin_code):
        client = MongoClient() 
        client = MongoClient(self.host, self.port)
        db = client["vin"]
        collection = db["vin"]
        results = collection.find({"vinCode":vin_code})
        return results

    def query_wmi(self, wmi_code):
        client = MongoClient() 
        client = MongoClient(self.host, self.port)
        db = client["vin"]
        collection = db["wmi"]
        results = collection.find({"wmiCode":wmi_code})
        return results


if __name__ == '__main__':
    mongo = Mongo()
    results = mongo.query_vin("LSVAM418")
    for result in results:
        print "vin:", type(result), result
    results = mongo.query_wmi("LFV")
    for result in results:
        print "wmi:", type(result), result

