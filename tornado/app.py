#!/usr/bin/env python
# coding:utf-8

import sys
import os
import json

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '..'))

from utils.vin import Vin
from mongodb.mongodb import MongoDB
from rabbitmq.rabbitmq import RabbitMQ
import settings

from spider.vin.com_51kahui import worker as com_51kahui_worker
from spider.vin.net_vin114 import worker as net_vin114_worker
from spider.vin.cn_vincar import worker as cn_vincar_worker


WORKERS = [
    {
        "module": cn_vincar_worker,
        "enable": True
    },
    {
        "module": com_51kahui_worker,
        "enable": True
    },
    {
        "module": net_vin114_worker,
        "enable": True
    },
]

try:
    import tornado.httpserver
    import tornado.ioloop
    import tornado.web
    from tornado.options import define, options
except ImportError:
    print "Notify service need tornado, please run depend.sh"
    sys.exit(1)


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
        if vinobj.is_valid():
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
        is_realtime = self.get_argument('is_realtime', False)
        vinobj = Vin(vincode)
        if not vinobj.is_valid():
            res = {
                "status": "40000000",
                "message": "bad request",
            }
            self.write(json.dumps(res, ensure_ascii=False))
            return
        results = self.application.mongo.query_vin(vinobj.get_wmi()+vinobj.get_vds())
        if results.count() == 0:
            res = {
                "status": "40400000",
                "message": "not found",
            }
            if is_realtime:
                workers = [worker for worker in WORKERS if worker["enable"]]
                for worker in workers:
                    data = worker["module"].do_task(vinobj.get_vin())
                    if data:
                        res = {
                            "status": "20000000",
                            "message": "ok",
                            "result": data
                        }
                        self.application.mongo.insert_vin(data)
                        break
            if res["status"] != "20000000":
                self.application.rabbitmq.publish(vinobj.get_vin())
            self.write(json.dumps(res, ensure_ascii=False))
        else:
            lists = []
            for result in results:
                result.pop("_id")
                lists.append(result)
            res = {
                "status": "20000000",
                "message": "ok",
                "result": lists
            }
            self.write(json.dumps(res, ensure_ascii=False))


class WmiCodeHandler(tornado.web.RequestHandler):
    def get(self, wmicode):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        result = self.application.mongo.query_wmi(wmicode)
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


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/vin/v1/(\w+)", VinCodeHandler),
            (r"/wmi/v1/(\w+)", WmiCodeHandler),
            (r"/vin/v1/checksum/(\w+)", VinChecksumHandler),
        ]
        self.mongo = MongoDB(host=settings.mongodb["host"])
        self.rabbitmq = RabbitMQ(host=settings.rabbitmq["host"])
        tornado.web.Application.__init__(self, handlers, debug=True)


def  main():
    tornado.options.parse_command_line()

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
