# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sentence import comparation

class select(object):
	def __init__(self, *selects):
		self.selects = []
		self.select(*selects)
		self.comparations = []
		self.seljoins = []
		self.group_bys = []
		self.models = []
		self.limits = []
		self.name = "SELECT"
	# end def

	def select(self, *selects):
		for select in selects:
			self.selects.append(select)
		# end for
	# end def

	def seljoin(self, *seljoins):
		seljoins = seljoin(*seljoins)
		self.seljoins.append(seljoins)
		return self
	# end def

	def from_models(self, *models):
		self.models = models
		return self
	# end def

	def where(self, *comparations):
		self.comparations = comparations
		return self
	# end def

	def group_by(self, *group_bys):
		self.group_bys = group_bys
		return self
	# end def

	def limit(self, *limits):
		self.limits = limits
		return self
	# end def

	def merge(self, select):
		self.selects = self.selects + select.selects
		self.comparations = self.comparations + select.comparations
		self.seljoins = self.seljoins + select.seljoins
		self.group_bys = self.group_bys + select.group_bys
		self.models = self.models + select.models
		self.limits = self.limits + select.limits
	# end if

	def paginate(self, paginated_by, page):
		return self
	# end def

	def __str__(self):
		return "(%s)" % (self.as_sql())
	# end def

	def as_sql(self):
		selects = []
		for select in self.selects:
			if hasattr(select, 'model') and not select.model in self.models:
				self.models.append(select.model)
			# end if
			selects.append(str(select))
		# end for
		models = []
		for model in self.models:
			models.append(model.as_sql())
		# end for
		seljoins = []
		for seljoin in self.seljoins:
			models.append(seljoin.join().as_sql())
		# end for
		comparations = []
		for comparation in self.comparations:
			comparations.append(comparation.as_sql())
		# end for
		limits = []
		for limit in self.limits:
			limits.append(str(limit))
		# end for
		group_bys = []
		for group_by in self.group_bys:
			group_bys.append(group_by.table_column())
		# end for
		if len(models):
			models = " FROM " + ', '.join(models)
		else:
			models = ""
		# end if
		if len(comparations):
			comparations = " WHERE " + ', '.join(comparations)
		else:
			comparations = ""
		# end if
		if len(group_bys):
			group_bys = " GROUP BY " + ', '.join(group_bys)
		else:
			group_bys = ""
		# end if
		if len(limits):
			limits = " LIMIT " + ', '.join(limits)
		else:
			limits = ""
		# end if
		sql = "%(name)s %(selects)s%(models)s%(comparations)s%(group_bys)s%(limits)s" % {
			"selects": ', '.join(selects),
			"models": models,
			"comparations": comparations,
			"group_bys": group_bys,
			"limits": limits,
			"name": self.name,
		}
		return sql
	# end def
# end class

class insert(object):
	def __init__(self, table):
		self.table = table
		self.columns_values = {}
	# end def

	def values(self, **values):
		self.columns_values.update(values)
		return self
	# end def
  
	def as_sql(self):
		return """INSERT INTO %(table)s (%(columns)s) VALUES ('%(values)s') """ % {
			"table": self.table.as_sql(),
			"columns": ', '.join(self.columns_values.keys()),
			"values": "', '".join(self.columns_values.values()),
		}
	# end def
# end class

class perform(select):
	def __init__(self, *selects):
		super(perform, self).__init__(*selects)
		self.name = "PERFORM"
	# end def
# end class

class join(object):
	def __init__(self, relation1, relation2, on):
		self.relation1 = relation1
		self.relation2 = relation2
		self.on = on
	# end def

	def as_sql(self):
		sql = "%(relation1)s JOIN %(relation2)s ON %(on)s" % {
			"relation1": self.relation1.as_sql(),
			"relation2": self.relation2.as_sql(),
			"on": self.on.as_sql(),
		}
		return sql
	# end def
# end class

class seljoin(object):
	def __init__(self, *foreign_keys):
		self.foreign_keys = foreign_keys
	# end def

	def join(self):
		old_foreign_key = None
		joins = None
		for foreign_key in self.foreign_keys:
			if old_foreign_key:
				joins = join(
					joins, 
					foreign_key.reference.model, 
						comparation(
							foreign_key.table_column(), '=', 
							foreign_key.reference.table_column()
						)
				)
			else:
				joins = join(
					foreign_key.model, 
					foreign_key.reference.model, 
						comparation(
							foreign_key.table_column(), '=', 
							foreign_key.reference.table_column()
						)
				)
			# end if
			old_foreign_key = foreign_key
		# end for
		return joins
	# end def
# end class

class aggregation(object):
	def __init__(self, aggregation_name, *params):
		self.aggregation_name = aggregation_name
		self.params = params
	# end def

	def as_sql(self):
		params = []
		for param in self.params:
			params.append(param.as_sql())
		# end for
		sql = "%(aggregation_name)s(%(params)s)" % {
			"aggregation_name": self.aggregation_name,
			"params": ', '.join(params)
		}
		return sql
# end class

class sum_agg(aggregation):
	def __init__(self, *params):
		super(sum_agg, self).__init__("sum", *params)
	# end def
# end class

class count_agg(aggregation):
	def __init__(self, *params):
		super(count_agg, self).__init__("count", *params)
	# end def
# end class

class concat(aggregation):
	def __init__(self, *params):
		super(concat, self).__init__("concat", *params)
	# end def
# end class