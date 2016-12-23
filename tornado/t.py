#!/usr/bin/env python
# coding:utf-8

import sys
import os
import logging
import json


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

define("port", default=10089, help="run on the given port", type=int)
define('debug', default=True, help='enable debug mode')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        html = """
        <h1>Welcome Vin Decoder</h1>
        <br>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/demo">Demo</a></li>
        </ul>
        """
        self.write(html)

class DemoHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect("/vin/v1/LVSHCAMB1CE054249")

class VinCodeHandler(tornado.web.RequestHandler):
    def get(self, vincode):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        res = {
            "status": "20000000", 
            "message": "ok",
            "result": {
                "vincode": vincode.encode("utf-8"),
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
        }
        self.write(json.dumps(res, ensure_ascii=False))


def  main():
    tornado.options.parse_command_line()

    settings = {
        'debug': options.debug,
    }

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/demo", DemoHandler),
        (r"/vin/v1/(\w+)", VinCodeHandler),
    ], **settings)

    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

