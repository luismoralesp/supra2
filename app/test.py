# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import config
import unittest
  
class ScriptTest(unittest.TestCase):
	def _test_connection(self):
		from dbs.db import ConnectionBase
		con = ConnectionBase.conect()
		print con.execute("select * from aa")
	# end def

	def test_context(self):
		from query.query import insert, select, perform
		from query.sentence import context, body, declare, for_loop, if_cond
		from query.types import integer, varchar
		from query.model import model, constrain

		class a(model):
			id = model.primarykey(integer)
			sd = model.column(varchar(11))
		# end class

		body.do(
			insert(a.model).values(id='1', sd='hello'),
			insert(a.model).values(id='2', sd='hello2'),
			if_cond('(extract(seconds from current_time)::int % 2 = 0)').do(
				insert(a.model).values(id='3', sd='hello3'),
			)
		)
    
		query = context().do(
			select(a.id, a.sd).from_models(a.model)
    )
		sql = body.as_sql_context()
		sql2 = query.as_sql()
		print sql, sql2
		from dbs.db import ConnectionBase
		con = ConnectionBase.conect(config)
		print con.perform(a().create_sql())
		print con.perform(sql)
		print con.execute(sql2)
		print con.perform(a().drop_sql())
	# end def

	def _test_join(self):
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
    