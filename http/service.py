# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import json
from query import model
from query.query import insert, update, select, perform
from query.sentence import context, body, declare, for_loop, if_cond, comparation
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
	# end def
	
	def review_list(self, json_body):
		for key in range(len(json_body)):
			json_body[key] = self.review(json_body[key])
		# end for
		return json_body
	# end def
	
	def review_str(self, json_body):
		import re
		json_body = json_body.replace("'", "''")
		if json_body.startswith("%"):
			json_body = json_body.replace("%", "")
			json_body = re.sub("\W", "", json_body)
			json_body = re.sub("\s", "", json_body)
		else:
			json_body = "'%s'" % json_body
		# end if
		return json_body
	# end def
	
	def review(self, json_body):
		if isinstance(json_body, str) or isinstance(json_body, unicode):
				return self.review_str(json_body)
		elif isinstance(json_body, dict):
				return self.review_dict(json_body)
		elif isinstance(json_body, list):
				return self.review_list(json_body)
		# end if
		return json_body
	# end def
	
	def review_dict(self, json_body):
		for key in json_body:
			json_body[key] = self.review(json_body[key])
		# end for
		return json_body
	# end def

	def json_body(self):
		length = int(self.headers.getheader('content-length'))
		json_body = json.loads(self.rfile.read(length))
		return self.review(json_body)
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
SET = 'set'
NAME = 'name'
WHERE = 'where'
TYPE = 'type'
VALUE = 'value'
VALUES = 'values'
DACLARE = 'declare_as'
COLUMNS = 'columns'
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
  
	def insert(self, data, ctxt):
		model_class = getattr(self.models, data[MODEL])
		values = data[VALUES]
		response = insert(model_class.model).values(**values)
		if RETURNING in data:
			response = response.returning(data[RETURNING])
		# end if
		if DACLARE in data:
			vdt = data[DACLARE]
			var = declare(vdt[NAME], vdt[TYPE])
			ctxt.declares.append(var)
			response.into(var)
		# end if
		return response
	# end def
  
	def update(self, data, ctxt):
		model_class = getattr(self.models, data[MODEL])
		sets = data[SET]
		where = data[WHERE]
		response = update(model_class.model).set(**sets).where(comparation.comparations(**where))
		if RETURNING in data:
			response = response.returning(data[RETURNING])
		# end if
		return response
	# end def
  
	def select(self, data, ctxt):
		model_class = getattr(self.models, data[MODEL])
		columns = data[COLUMNS]
		where = data[WHERE]
		query = select(*columns).from_models(model_class.model).where(comparation.comparations(**where))
		if DACLARE in data:
			vdt = data[DACLARE]
			var = declare(vdt[NAME], vdt[TYPE])
			ctxt.declares.append(var)
			query = var.set(query)
		# end if
		return query
	# end def
  
	def delete(self, data, ctxt):
		return self.get.get('page', '0')
	# end def
  
	def crud_list(self, data, ctxt):
		for elm in data:
			self.crud(elm, ctxt)
		# end for
	# end def
  
	def crud_dict(self, data, ctxt):
		if data[CRUD_TYPE] == INSERT_TYPE:
			query = self.insert(data, ctxt)
		elif data[CRUD_TYPE] == UPDATE_TYPE:
			query = self.update(data, ctxt)
		elif data[CRUD_TYPE] == DELETE_TYPE:
			query = self.delete(data, ctxt)
		elif data[CRUD_TYPE] == SELECT_TYPE:
			query = self.select(data, ctxt)
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
		import sys, os, traceback
		from dbs.db import ConnectionBase
		
		try:
			json_body = self.json_body()
			ctxt = context()
			self.crud(json_body, ctxt)
			

			con = ConnectionBase.conect(self.config)
			if self.method == 'PUT':
				print ctxt.as_sql_context()
				return con.perform(ctxt.as_sql_context())
			elif self.method == 'POST':
				print ctxt.as_sql()
				return con.execute(ctxt.as_sql())
			# end if
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			formatted_lines = traceback.format_exc().splitlines()
			return {
				'type': str(exc_type.__name__),
				'traceback': formatted_lines,
				'file': fname,
				'error': str(e)
			}
		# end try
		
	# end def
# end class
