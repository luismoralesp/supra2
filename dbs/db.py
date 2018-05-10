# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import importlib

class ConnectionBase(object):
	def __init__(self, config):
		self.config = config
	# end def

	@staticmethod
	def conect(config, config_name="default"):
		conf = config.DB_CONFIG[config_name]
		db = importlib.import_module("dbs.%s" % (config.DB_CONFIG[config_name]['type'], ))
		return db.Connection(conf)
	# end def
# end def
