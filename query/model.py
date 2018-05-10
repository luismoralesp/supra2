# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from query import join, select
from sentence import operation, procedure

class Watcher(type):
	__models__ = []
	def __init__(cls, name, bases, clsdict):
		if len(cls.mro()) > 3:
			cls.model = cls()
			Watcher.__models__.append(cls.model)
        # edn if
		super(Watcher, cls).__init__(name, bases, clsdict)
	# end def
# end class

class relation(object): 
	__metaclass__ = Watcher

	def __init__(self, model_name):
		self.model_name = model_name
	# end def

	def join(self, relation, on):
		return join(self, relation, on)
	# end def

	def as_sql(self):
		return self.model_name
	# end def
# end def

class classproperty(property):
	def __get__(self, cls, owner):
		return classmethod(self.fget).__get__(None, owner)()
	# end def
# end def

class model(relation):
	columns = None
	def __init__(self, model_name=None):
		super(model, self).__init__(model_name or type(self).__name__)
		self.constrains = []
		self.objects = select()
		self.map_model()
	# end def

	def constrain(self, *constrains):
		for constrain in constrains:
			self.constrains.append(constrain)
		# end for
		return self
	# end def

	def map_model(self):
		for name in dir(self):
			column = getattr(self, name)
			self.on_map(column, name)
		# end for
	# end def

	def on_map(self, col, name):
		if isinstance(col, column):
			col.column_name = name
			col.model = self
			self.constrain(*col.constrains)
		# end if

		if isinstance(col, select):
			self.objects.merge(col)
		# end if
	# end if

	@staticmethod
	def column(column_name):
		return column(column_name)
	# end def

	@staticmethod
	def foreignkey(reference):
		return foreignkey(reference)
	# end def

	@staticmethod
	def unique(column_type):
		return unique(column_type)
	# end def

	@staticmethod
	def primarykey(column_type):
		return primarykey(column_type)
	# end def

	def __call__(self, *params):
		params = map(str, params)
		return "%s(%s)" % (self.model_name, ', '.join(params))
	# end def

	def drop_sql(self):
		return """DROP TABLE %(model_name)s;""" % {
			'model_name': self.model_name,
		}
	# end def

	def create_sql(self):
		columns = []
		for col in dir(self):
			if isinstance(getattr(self, col), column):
				sql_col = "%s %s" % (col, getattr(self, col).as_sql())
				if getattr(self, col).is_not_null:
					sql_col = sql_col + " NOT NULL"
				# end if
				columns.append(sql_col)
			# end if
		# end for
		constrains = []
		for constrain in self.constrains:
			constrains.append(constrain.as_sql())
		# end def
		if len(constrains):
			constrains = ', ' + ', '.join(constrains)
		else:
			constrains = ""
		# end if
		sql = "CREATE TABLE %(model_name)s (%(columns)s%(constrains)s);" % {
			'model_name': self.model_name,
			'columns': ', '.join(columns),
			'constrains': constrains,
		}
		return sql
	# end def
# end class

class trigger(procedure):
	def __init__(self, trigger_name, table_name, on_insert=False, on_update=False, on_delete=True):
		self.procedure_name = trigger_name
		self.table_name = table_name
		self.on_insert = on_insert
		self.on_update = on_update
		self.on_delete = on_delete
		self.returns('TRIGGER')
	# end def


	def as_sql(self):
		procedure = super(trigger, self).as_sql()
		sql = "TRIGGER IN %(table_name)s ON %(ons)s " #continue here ..
		return sql
	# end def

# end class

class column(operation):
	def __init__(self, column_type, *constrains):
		self.column_type = column_type
		self.model = None
		self.column_name = None
		self.is_not_null = False
		self.constrain(*constrains)
	# end def

	def constrain(self, *constrains):
		for constrain in constrains:
			constrain.columns = [self]
		# end for
		self.constrains = constrains
		return self
	# end def

	def not_null(self):
		self.is_not_null = True
		return self
	# end def

	def as_sql(self):
		return str(self.column_type)
	# end def

	def table_column(self):
		return "%s.%s" % (self.model.model_name, self.column_name)
	# end def

	def __str__(self):
		return self.table_column()
	# end def
# end def

class foreignkey(column):
	def __init__(self, reference):
		super(foreignkey, self).__init__(reference.column_type)
		self.constrain(constrain('FOREIGN KEY').reference(reference))
		self.reference = reference
	# end def
# end class

class primarykey(column):
	def __init__(self, column_type):
		super(primarykey, self).__init__(column_type)
		self.constrain(constrain('PRIMARY KEY'))
	# end def
# end class

class unique(column):
	def __init__(self, column_type):
		super(unique, self).__init__(column_type)
		self.constrain(constrain('UNIQUE'))
	# end def
# end class

class constrain(object):
	number = 0
	def __init__(self, constrain_name, constrain_type=None, *columns):
		self.constrain_name = constrain_name
		self.constrain_type = constrain_type or "cons"  + str(constrain.number)
		self.columns = columns
		self.references = [] 
		constrain.number = constrain.number + 1
	# end def

	def reference(self, *references):
		self.references = references
		return self
	# end def

	def as_sql(self):
		columns = []
		for column in self.columns:
			columns.append(column.column_name)
		# end for
		references = []
		for reference in self.references:
			references.append("%s(%s)" % (str(reference.model.model_name), str(reference)) )
		# end for
		if len(self.references):
			references = " REFERENCES " + ', '.join(references)
		else:
			references = ""
		# end if
		return "CONSTRAINT %(constrain_type)s %(constrain_name)s (%(columns)s)%(references)s" % {
			"constrain_name": self.constrain_name,
			"constrain_type": self.constrain_type,
			"columns": ', '.join(columns),
			"references": references
		}
	# end def
# end class

		
	