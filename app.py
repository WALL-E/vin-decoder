#!/usr/bin/env python
# coding:utf-8

import sys
import os
import logging
import json

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, 'mongodb'))
sys.path.append(os.path.join(ROOT_DIR, 'rabbitmq'))

from mongo import Mongo
from vin import Vin
from rabbitmq import RabbitMQ

try:
    import tornado.ioloop
    import tornado.web
    import tornado.escape
    from tornado.options import define, options
except ImportError:
    print "Notify service need tornado, please run depend.sh"
    sys.exit(1)


ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)

define("port", default=10090, help="run on the given port", type=int)
define('debug', default=True, help='enable debug mode')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        html = """
        <h1>Welcome Vin Decoder</h1>
        <br>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/vin/v1/LVSHCAMB1CE054249">vinDemo</a></li>
          <li><a href="/wmi/v1/LVS">wmiDemo</a></li>
          <li><a href="/vin/v1/checksum/LVSHCAMB1CE054249">vinChecksumDemo</a></li>
        </ul>
        """
        self.write(html)


class VinChecksumHandler(tornado.web.RequestHandler):
    def get(self, vincode):
        vinobj = Vin(vincode)
        if vinobj.isValid():
            res = {
                "status": "20000000", 
                "message": "ok",
                "checksum": True
            }
        else:
            res = {
                "status": "40000000", 
                "message": "bad request",
                "checksum": False
            }
        self.write(json.dumps(res, ensure_ascii=False))
        

class VinCodeHandler(tornado.web.RequestHandler):
    def get(self, vincode):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        vinobj = Vin(vincode)
        if not vinobj.isValid():
            res = {
                "status": "40000000", 
                "message": "bad request",
            }
            self.write(json.dumps(res, ensure_ascii=False))
            return
        result = Mongo().query_vin(vinobj.getWmi()+vinobj.getVds())
        if result is None:
            res = {
                "status": "40400000", 
                "message": "not found",
            }
            RabbitMQ().publish(vinObj.getVin())
            self.write(json.dumps(res, ensure_ascii=False))
        else:
            result.pop("_id")
            res = {
                "status": "20000000", 
                "message": "ok",
                "result": result
            }
            self.write(json.dumps(res, ensure_ascii=False))


class WmiCodeHandler(tornado.web.RequestHandler):
    def get(self, wmicode):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        result = Mongo().query_wmi(wmicode)
        if result is None:
            res = {
                "status": "40400000", 
                "message": "not found",
            }
            self.write(json.dumps(res, ensure_ascii=False))
        else:
            result.pop("_id")
            res = {
                "status": "20000000", 
                "message": "ok",
                "result": result
            }
            self.write(json.dumps(res, ensure_ascii=False))


def  main():
    tornado.options.parse_command_line()

    settings = {
        'debug': options.debug,
    }

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/vin/v1/(\w+)", VinCodeHandler),
        (r"/wmi/v1/(\w+)", WmiCodeHandler),
        (r"/vin/v1/checksum/(\w+)", VinChecksumHandler),
    ], **settings)

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

