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
        result = collection.find_one({"vinCode":vin_code})
        return result

    def query_wmi(self, wmi_code):
        client = MongoClient() 
        client = MongoClient(self.host, self.port)
        db = client["vin"]
        collection = db["wmi"]
        result = collection.find_one({"wmiCode":wmi_code})
        return result


if __name__ == '__main__':
    mongo = Mongo()
    result = mongo.query_wmi("LSG")
    print type(result), result
    result = mongo.query_vin("LSVAM4187C2184847")
    print type(result), result

