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
