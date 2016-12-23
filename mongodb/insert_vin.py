#!/usr/bin/python
# -*- coding: UTF-8 -*-


from pymongo import *


client = MongoClient() 
client = MongoClient("localhost", 27017)
db = client["vin"]

collection = db["vin"]
data = {
    "vincode": "LSVAM4187C2184847",
    "厂家": "一汽大众(奥迪)",
    "品牌": "奥迪",
    "车型": "Q5",
    "VIN年份": "2013",
    "排放标准": "国4",
    "进气形式": "涡轮增压",
    "排量(升)": "2.0 T",
    "最大马力(ps)": "211",
    "驱动形式": "前置四驱",
    "变速器描述": "手自一体变速器(AMT)",
    "档位数": "8",
    "燃油类型": "汽油",
}
collection.insert(data)

data = {
    "vincode": "LVSHCAMB1CE054249",
    "车型": "福克斯-两厢", 
    "厂家": "长安福特马自达", 
    "品牌": "福特", 
    "排量(升)": "1.6 L", 
    "进气形式": "自然吸气", 
    "排放标准": "国4", 
    "最大马力(ps)": "125", 
    "变速器描述": "手动变速器(MT)", 
    "档位数": "5", 
    "驱动形式": "前置前驱", 
    "VIN年份": "2012", 
    "燃油类型": "汽油"
}
collection.insert(data)

