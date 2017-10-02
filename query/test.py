# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from query.model import model, constrain
from query.query import *
from query.sentence import *
from query.types import *

import unittest

class QueryTest(unittest.TestCase):

	def test_query(self):
		class Tabla(model):
			column1 = model.column(integer)
			column2 = model.column(varchar(45))
		# end class

		class Tabla2(model):
			column1 = model.foreignkey(Tabla.column1)
			column2 = model.unique(varchar(45)).not_null()
		# end class

		a = declare("a", integer, 4)
		body.c = declare("x", integer)
		body.do(
			a.set(a.plus(1)),
			for_loop(a, 1, 10).do(
				a.set(a.by(2))
			),
			for_in(body.c, select(Tabla2.column1).from_models(Tabla2.model).where())
		)

		print body.as_sql()

		print Tabla().create_sql()
		print Tabla2().create_sql()
	# end def
#end class

if __name__ == '__main__':
	unittest.main()