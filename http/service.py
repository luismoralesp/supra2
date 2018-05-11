# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
from query import model
from query.query import insert, update, select, perform
from query.sentence import context, body, declare, for_loop, if_cond
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
NAME = 'name'
TYPE = 'type'
VALUE = 'value'
DACLARE = 'declare_as'
RETURNING = 'returning'
INSERT_TYPE = 'insert'
UPDATE_TYPE = 'update'
DELETE_TYPE = 'delete'
SELECT_TYPE = 'select'

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
  
	def insert(self, data):
		model_class = getattr(self.models, data[MODEL])
		values = data[DATA]
		response = insert(model_class.model).values(**values)
		if RETURNING in data:
			response = response.returning(data[RETURNING])
		# end if
		return response
	# end def
  
	def update(self):
		return self.get.get('page', '0')
	# end def
  
	def select(self):
		return self.get.get('page', '0')
	# end def
  
	def delete(self):
		return self.get.get('page', '0')
	# end def
  
	def crud_list(self, data, ctxt):
		for elm in data:
			self.crud(elm, ctxt)
		# end for
	# end def
  
	def crud_dict(self, data, ctxt):
		if data[CRUD_TYPE] == INSERT_TYPE:
			query = self.insert(data)
		elif data[CRUD_TYPE] == UPDATE_TYPE:
			query = self.update(data)
		elif data[CRUD_TYPE] == DELETE_TYPE:
			query = self.delete(data)
		elif data[CRUD_TYPE] == SELECT_TYPE:
			query = self.select(data)
		# end if
		if DACLARE in data:
			vdt = data[DACLARE]
			var = declare(vdt[NAME], vdt[TYPE])
			ctxt.declares.append(var)
			query = var.set(query)
		# end if
		ctxt.do(query)
	# end def
  
	def crud(self, data, ctxt):
		if isinstance(data, list):
			return self.crud_list(data, ctxt)
		elif isinstance(data, dict):
			return self.crud_dict(data, ctxt)
    # end if
	# end def
  
	def response(self, *params):
		try:
			json_body = self.json_body()
			ctxt = context()
			self.crud(json_body, ctxt)
			return {"sql": ctxt.as_sql_context()}
		except Exception as e:
			return {"error": str(e)}
		# end if
		#con = ConnectionBase.connect()
		#return con.execute(self.get_query().paginate(self.get_paginated_by()), self.get_page())
	# end def
# end class
