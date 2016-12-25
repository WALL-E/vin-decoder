#!/usr/bin/python
# -*- coding: UTF-8 -*-

import SimpleHTTPServer
import SocketServer

IP = "0.0.0.0"
PORT = 8000

def main():
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer((IP, PORT), Handler)
    print "serving at port", PORT
    httpd.serve_forever()

if __name__ == "__main__":
    main()
