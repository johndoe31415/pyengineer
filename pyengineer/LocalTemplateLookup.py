#	pyengineer - Helping hand for electronics and mechanical engineering
#	Copyright (C) 2012-2018 Johannes Bauer
#
#	This file is part of pyengineer.
#
#	pyengineer is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pyengineer is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with pyengineer; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>

import os
from mako.template import Template
from mako.lookup import TemplateLookup

class LocalTemplateLookup(object):
	def __init__(self):
		template_dir = os.path.dirname(__file__) + "/templates"
		self._lookup = TemplateLookup([ template_dir ], input_encoding = "utf-8", strict_undefined = True)

	def get_template(self, template_name):
		return self._lookup.get_template(template_name)

	def create(self, template_source):
		template = Template(template_source, strict_undefined = True, lookup = self._lookup)
		return template
