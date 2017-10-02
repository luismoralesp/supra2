# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import psycopg2
from db import ConnectionBase

class Connection(ConnectionBase):
	def connection(self):
		return psycopg2.connect("dbname='%(dbname)s' user='%(user)s' host='%(host)s' password='%(password)s'" % self.config)
	# end def

	def execute(self, sql):
		return []
		con = self.connection()
		cur = con.cursor()
		cur.execute(sql)
		fetch = cur.fetchall()
		con.close()
		return fetch
	# end def
# end def