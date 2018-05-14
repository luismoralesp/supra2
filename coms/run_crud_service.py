# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from BaseHTTPServer import HTTPServer
from http.service import CrudService 
import importlib

def main(app, config, server_class=HTTPServer, port=8081):
    main_service = importlib.import_module("%s.%s" % (app, config.main_service, ))
    models = importlib.import_module("%s.models" % (app, ))
    server_address = ('', port)
    CrudService.models = models
    CrudService.config = config
    httpd = server_class(server_address, CrudService)
    print 'Starting httpd...'
    httpd.serve_forever()