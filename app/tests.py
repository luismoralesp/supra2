# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
  
class ScriptTest(unittest.TestCase):
	def _test_connection(self):
		from dbs.db import ConnectionBase
		con = ConnectionBase.conect()
		print con.execute("select * from aa")
	# end def

	def _test_context(self):
		from query.query import select, perform
		from query.sentence import body
		from query.types import integer, varchar
		from query.model import model, constrain

		class a(model):
			id = model.primarykey(integer)
			sd = model.column(varchar(11))
		# end class

		body.do(
			perform(a.id).from_models(a.model)
		)
		print body.as_sql()
		from dbs.db import ConnectionBase
		con = ConnectionBase.conect()
		print con.execute(body.as_sql())
	# end def

	def test_join(self):
		from query.query import select, perform
		from query.model import model
		from query.types import integer, varchar, date, text
		from query.sentence import body, declare, for_loop, if_cond

		class carro(model):
			id = model.primarykey(integer)
			placa = model.column(varchar(11))
		# end class

		class datospersonales(model):
			id = model.primarykey(integer)
			nombre = model.column(varchar(120))
			telefono = model.column(varchar(10))
			direccion = model.column(text)
		# end class

		class mecanico(model):
			id = model.primarykey(integer)
			datospersonales_id = model.foreignkey(datospersonales.id)
		# end class

		class reparacion(model):
			id = model.primarykey(integer)
			carro_id = model.foreignkey(carro.id)
			mecanico_id = model.foreignkey(mecanico.id)
			fecha = model.column(date)
			#telefono_mecanico = select(datospersonales.telefono).seljoin(mecanico_id, mecanico.datospersonales_id)
		# end class


		#print a.set(reparacion.telefono_mecanico).as_sql()
		#print select(reparacion.id, reparacion.telefono_mecanico).as_sql()
		#print reparacion.model.create_sql()
		#print reparacion.model.objects.as_sql()
		a = declare('a', integer)
		body.do(
			a.set(a.plus(1)),
			for_loop(a, 1, 10).do(
				if_cond(a.lt(11)).do(
				)
			)
		)
		print select(reparacion.id, mecanico.id, datospersonales.nombre).seljoin(reparacion.mecanico_id, mecanico.datospersonales_id).group_by(mecanico.id)

	

		#class get_data(procedure):
		#	def body(self, param1, param2):
		#		a = self.declare('a', integer)
		#		self.returns(integer)
		#		return self.do(
		#			
		#		).language(plpgsql)
		#	# end def
		## end class