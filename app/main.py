# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from http.service import BaseService

class Main(BaseService):
	def response(self, *params):
		return {'message': 'hello word!'}
	# end def
# end class