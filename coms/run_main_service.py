# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from BaseHTTPServer import HTTPServer
import importlib

def main(app, config, server_class=HTTPServer, port=8000):
    main_service = importlib.import_module("%s.%s" % (app, config.main_service, ))
    server_address = ('', port)
    httpd = server_class(server_address, main_service.Main)
    print 'Starting httpd...'
    httpd.serve_forever()