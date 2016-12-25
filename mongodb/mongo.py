#!/usr/bin/python

from pymongo import *


class Mongo():
    def __init__(self, host="localhost", port=27017, dbname="vin"):
        self.host = host
        self.port = port
        self.conn = MongoClient(self.host, self.port)
        self.db = self.conn[dbname]

    def query_vin(self, vin_code):
        collection = self.db["vin"]
        results = collection.find({"vinCode":vin_code})
        return results

    def query_wmi(self, wmi_code):
        collection = self.db["wmi"]
        results = collection.find({"wmiCode":wmi_code})
        return results

    def insert_vin(self, objs, vin_code):
        collection = self.db["vin"]
        for obj in objs:
            obj["vinCode"] = vin_code[0:8]
            obj["vinLong"] = vin_code
            collection.insert(obj)


if __name__ == '__main__':
    mongo = Mongo()
    results = mongo.query_vin("LSVAM418")
    for result in results:
        print "vin:", type(result), result
    results = mongo.query_wmi("LVG")
    for result in results:
        print "wmi:", type(result), result

