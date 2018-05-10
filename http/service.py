# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
from query import model
from dbs import db

class BaseService(BaseHTTPRequestHandler):
	get = {}

	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
	# end def

	def get_url_params(self):
		return []
	# end def

	def process(self, method):
		self.method = method
		self._set_headers()
		response = self.response(*self.get_url_params())
		self.wfile.write(json.dumps(response))
	# end def

	def response(*params):
		return json.loads('{"data":"dummy"}')
	# end def

	def do_OPTIONS(self):
		return self.process('OPTIONS')
	# end def

	def do_GET(self):
		return self.process('GET')
	# end def

	def do_HEAD(self):
		return self.process('HEAD')
	# end def

	def do_POST(self):
		return self.process('POST')
	# end def

	def do_PUT(self):
		return self.process('PUT')
	# end def

	def do_DELETE(self):
		return self.process('DELETE')
	# end def

	def do_TRACE(self):
		return self.process('TRACE')
	# end def

	def do_CONNECT(self):
		return self.process('CONNECT')
	# end def

	def body(self):
		length = int(self.headers.getheader('content-length'))
		return json.loads(self.rfile.read(length))
	# end def	# end def

	def json_body(self):
		length = int(self.headers.getheader('content-length'))
		return json.loads(self.rfile.read(length))
	# end def

	@property
	def post(self):
		ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
		if ctype == 'multipart/form-data':
			postvars = cgi.parse_multipart(self.rfile, pdict)
		elif ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers.getheader('content-length'))
			postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
		else:
			postvars = {}
		# end if
		return postvars
	# end def
# end class

CRUD_TYPE = 'crud_type'
MODEL = 'model'
DATA = 'data'

class CrudService(BaseService):
	query = None
	paginated_by = 10

	def get_query(self):
		return self.query
	# end def

	def get_paginated_by(self):
		return self.get.get('paginated_by', self.paginated_by)
	# end def

	def get_page(self):
		return self.get.get('page', '0')
	# end def

	def response(self, *params):
		try:
			json_body = self.json_body()
		except Exception as e:
			return {"error": "Invalid json"}
		# end if

		if CRUD_TYPE in json_body:
			crud_type = json_body[CRUD_TYPE]
			if MODEL in json_body:
				model = json_body[MODEL]
				if DATA in json_body:
					data = json_body[DATA]
					model_class = getattr(self.models, model)
					return {"data": data, "objects": str(model_class.model.objects), "query": self.query}
				else:
					return {"error": "'data' param is missing"}
				# end if
			else:
				return {"error": "'model' param is missing"}
			# end if
		else:
			return {"error": "'crud_type' param is missing"}
		# end if

		#con = ConnectionBase.connect()
		#return con.execute(self.get_query().paginate(self.get_paginated_by()), self.get_page())
	# end def
# end class
