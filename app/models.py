# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from query.model import model
from query.query import select, insert
from query.sentence import if_cond
from query.types import datetime, bigint, time, varchar, serial, rowtype

class rangofecha(model):
	id = model.primarykey(serial)
	inicio = model.column(datetime).not_null()
	final = model.column(datetime).not_null()

	def interesct(self, body, rangofecha_id):
		rango = declare('rango', rowtype, select(rangofecha.inicio, rangofecha.final).where(rangofecha.id.eq(rangofecha_id)))
		body.do(
			if_cond(self.final.lt(rango.inicio).y(self.inicio.lte(rango.inicio))).do(
				insert(rangofecha).values(inicio=rango.inicio, final=self.low_date(self.final, rango.final))
			).elseif(rango.final.qt(self.inicio).y(self.inicio.gte(rango.inicio))).do(
				insert(rangofecha).values(inicio=self.inicio, final=self.low_date(self.final, rango.final))
			)
		)
	# end def
# end class

class turno(model):
	id = model.primarykey(serial)
	rangofecha_id = model.foreignkey(rangofecha.id)
	empleado = model.column(bigint).not_null()

	def on_insert(self, body):
		body.do(

		)
	# end def
# end class

class tiporango(model):
	id = model.primarykey(serial)
	nombre = model.column(varchar(45))
	inicio = model.column(time)
	final = model.column(time)

#end class
