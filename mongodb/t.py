#!/usr/bin/python

from pymongo import *


client = MongoClient() 
client = MongoClient("localhost", 27017)
db = client["vin"]

collection = db["wmi-from-offline"]
result = collection.find({"WMI":"LGB"})
print result.next()


collection = db["year"]
result = collection.find({"code":"B"})
print result.next()


collection = db["user"]
data = {"name":"Lucy", "sex":"female","job":"nurse"}
collection.insert(data)

temp = collection.find_one({"name":"Lucy"})
temp["name"] = "Jordan"
collection.save(temp)
