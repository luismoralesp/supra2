# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import psycopg2
from db import ConnectionBase

class Connection(ConnectionBase):
	def connection(self):
		return psycopg2.connect("dbname='%(dbname)s' user='%(user)s' host='%(host)s' password='%(password)s'" % self.config)
	# end def
	
	def query_db(self, cur, query, args=(), one=False):
		cur.execute(query, args)
		row = [ dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall() ]
		return (row[0] if row else None) if one else row
	# end def
  
	def perform(self, sql):
		con = self.connection()
		cur = con.cursor()
		cur.execute(sql)
		con.commit()
		cur.close()
		con.close()
		return True
  # end def
  
	def execute(self, sql):
		con = self.connection()
		cur = con.cursor()
		fetch = self.query_db(cur, sql)
		con.commit()
		cur.close()
		con.close()
		return fetch
	# end def
  
# end def