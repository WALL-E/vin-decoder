#!/usr/bin/python
"""
mongo python module
"""

import pymongo
import copy


class Mongo(object):
    """
    Mongo Class
    """
    def __init__(self, host="localhost", port=27017, dbname="vin"):
        self.host = host
        self.port = port
        self.conn = pymongo.MongoClient(self.host, self.port)
        self.database = self.conn[dbname]

    def query_vin(self, vin_code):
        """
        query vin collection
        """
        collection = self.database["vin"]
        return collection.find({"vinCode":vin_code})

    def query_wmi(self, wmi_code):
        """
        query wmi collection
        """
        collection = self.database["wmi"]
        return collection.find({"wmiCode":wmi_code})

    def insert_vin(self, objs):
        """
        insert vin collection, vinCode and vinLong
        """
        collection = self.database["vin"]
        for obj in objs:
            tmp = copy.deepcopy(obj)
            collection.insert(tmp)


def main():
    """
    main function
    """
    mongo = Mongo()
    results = mongo.query_vin("LSVAM418")
    for result in results:
        print "vin:", type(result), result
    results = mongo.query_wmi("LVG")
    for result in results:
        print "wmi:", type(result), result


if __name__ == '__main__':
    main()
