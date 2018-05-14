# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from query import query

class sentence(object):
	def __init__(self, sentence, context):
		self.sentence = sentence
		self.context = context
	# end def

	def __unicode__(self):
		return self.as_sql()
	# end def

	def as_sql(self):
		sql = ""
		for i in range(self.context.tabulation):
			sql = sql + "    "
		# end for
		sql = sql + self.sentence.as_sql()
		return sql
	# end def
# end class

class context(object):

	def __init__(self):
		self.declares = []
		self.sentences = []
		self.ctx = None
	# end def

	@property
	def tabulation(self):
		ctx = self
		tabulation = 0
		while (ctx):
			ctx = ctx.ctx
			tabulation = tabulation + 1
		# end def
		return tabulation
	# end def

	def declare(**declares):
		for var_name in declares:
			declare(var_name, declares[var_name])
		# end for
	# end def

	def do(self, *sentences):
		for sentence in sentences:
			self.append(sentence)
		# end if
		return self
	# end def

	def append(self, sentence):
		sentence.ctx = self
		self.sentences.append(sentence)
		return self
	# end def

	def as_sql_context(self):
		sql = "DO $$\n"
		for declare in self.declares:
			sql = sql + declare.as_sql() + ";\n"
		# end for
		sql = sql + "BEGIN\n"
		for sent in self.sentences:
			sql = sql + sentence(sent, self).as_sql() + ";\n"
		# end for
		sql = sql + "END $$;"
		return sql
	# end def

	def as_sql(self):
		sql = ""
		for declare in self.declares:
			sql = sql + declare.as_sql() + ";\n"
		# end for
		# sql = sql + "BEGIN\n"
		for sent in self.sentences:
			sql = sql + sentence(sent, self).as_sql() + ";\n"
		# end for
		#sql = sql + "END;"
		return sql
	# end def
# end class

body = context()

class set():
	def __init__(self, var_name, value):
		self.var_name = var_name
		self.value = value
	# end def

	def as_sql(self):
		if isinstance(self.value, query): 
			value = "(%s)" % self.value.as_sql()
		else:
			value = self.value
		# end if
		return "%(var_name)s := %(value)s" % {
			"var_name": self.var_name,
			"value": value,
		}
	# end def
# end class

class operation(object):
	def __init__(self, var_name1, operator, var_name2):
		self.var_name1 = var_name1
		self.operator = operator
		self.var_name2 = var_name2
	# end def
	def as_sql(self):
		if isinstance(self.var_name2, operation):
			var_name2 = "(%s)" % (self.var_name2.as_sql(), )
		else:
			var_name2 = self.var_name2
		# end if
		return "(%(var_name1)s %(operator)s %(var_name2)s)" % {
			"var_name1": self.var_name1,
			"operator": self.operator,
			"var_name2": var_name2,
		}
	# end def

	def by(self, value):
		return operation(self, "*", value)
	# end def

	def div(self, value):
		return operation(self, "/", value)
	# end def

	def plus(self, value):
		return operation(self, "+", value)
	# end def

	def minus(self, value):
		return operation(self, "-", value)
	# end def

	def o(self, value):
		return operation(self, "or", value)
	# end def

	def y(self, value):
		return operation(self, "and", value)
	# end def

	def eq(self, value):
		return operation(self, "=", value)
	# end def

	def dis(self, value):
		return operation(self, "<>", value)
	# end def

	def gt(self, value):
		return operation(self, ">", value)
	# end def

	def lt(self, value):
		return operation(self, "<", value)
	# end def

	def gte(self, value):
		return operation(self, ">=", value)
	# end def

	def lte(self, value):
		return operation(self, "<=", value)
	# end def

	def __unicode__(self):
		return self.as_sql()
	# end def
# end class

class comparation(operation):
	@staticmethod
	def comparations(**comps):
		comp = False
		for column in comps:
			value = comps[column]
			if comp:
				comp = comp.y(comparation(column, '=', value))
			else:
				comp = comparation(column, '=', value)
			# end if
		# end for
		return comp
	# end def
# end class

class close(object):
	def __init__(self, closing):
		self.closing = closing
	# end def

	def as_sql(self):
		return "end %s" % (self.closing, )
	# end if
# end class

class for_loop(context):
	def __init__(self, var_name, start, end, step=1):
		super(for_loop, self).__init__()
		self.var_name = var_name
		self.start = start
		self.end = end
		self.step = step
	# end def

	def as_sql(self):
		sql = "for %(var_name)s = %(start)s to %(end)s loop\n" % {
			"var_name": self.var_name,
			"start": self.start,
			"end": self.end,
			"step": self.step,
		}
		sql = sql + super(for_loop, self).as_sql()
		sql = sql + sentence(close("loop"), self.ctx).as_sql()
		return sql
	# end def
# end class

class for_in(context):
	def __init__(self, var_name, inn):
		super(for_in, self).__init__()
		self.var_name = var_name
		self.inn = inn
	# end def

	def as_sql(self):
		sql = "for %(var_name)s in (%(inn)s) loop\n" % {
			"var_name": self.var_name,
			"inn": self.inn.as_sql(),
		}
		sql = sql + super(for_in, self).as_sql()
		sql = sql + sentence(close("loop"), self.ctx).as_sql()
		return sql
	# end def
# end class

class if_cond(context):
	def __init__(self, compare):
		super(if_cond, self).__init__()
		self.compare = compare
	# end def

	def as_sql(self):
		sql = "if %(compare)s then\n" % {
			"compare": self.compare
		}
		sql = sql + super(if_cond, self).as_sql()
		sql = sql + sentence(close("if"), self.ctx).as_sql()
		return sql
	# end def
# end class

class declare(operation):
	def __init__(self, var_name, var_type, default_value=None):
		self.var_name = var_name
		self.var_type = var_type
		self.default_value = default_value or 'null'
		body.declares.append(self)
	# end def

	def as_sql(self):
		return "DECLARE %(var_name)s %(var_type)s := %(default_value)s" % {
			"var_name": self.var_name,
			"var_type": self.var_type,
			"default_value": self.default_value,
		}
	# end def

	def __str__(self):
		return self.var_name
	# end def

	def __unicode__(self):
		return self.var_name
	# end def

	def set(self, value):
		return set(var_name=self.var_name, value=value)
	# end def
# end class

class procedure(context):
	def __init__(self, procedure_name):
		self.procedure_name = procedure_name
		self.returns = None
		self.language = None
	# end if

	def returns(self, returns):
		self.returns = returns
	# end def

	def language(self, language):
		self.language = language
	# end def

	def body(self, *args):
		pass
	# end def

	def as_sql(self):
		pass
		#"CREATE OR REPLACE PROCEDURE %(procedure_name)s(%(params)s) RETURNS %(returns)s AS \n%(body)s language %(language)s" {
		#	# continue here ...
		#}
	# end def
# end def