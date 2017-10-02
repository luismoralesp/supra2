# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sys import argv
import importlib

APP  = 1
COM  = 2
PORT = 3

if __name__ == "__main__":
	argv_len = len(argv) - 1
	print argv_len
	if APP <= argv_len:
		app = argv[APP]
		config = importlib.import_module("%s.config" % (argv[APP], ))
		if COM <= argv_len:
			command = importlib.import_module("coms.%s" % (argv[COM], ))
			if PORT <= argv_len:
				port = argv[PORT]
				command.main(app=app, config=config, port=port)
			else:
				command.main(app=app, config=config)
			# end if
		else:
			raise Exception("param 2 command is missing")
		# end class
	else:
		raise Exception("param 1 app is missing")
	# end class
# end if


