#!/usr/bin/python3
# -*- coding:utf-8 -*-

import os
import sys
from tornado.options import options, define
from django.core.wsgi import get_wsgi_application
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

# Django Application加入查找路径中
app_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
define("port", default=6000, type=int, help="run on the given port")


def main():
    tornado.options.parse_command_line()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings_local")
    wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())
    http_server = tornado.httpserver.HTTPServer(wsgi_app, xheaders=True)  # xheaders=True是啥意思？
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
