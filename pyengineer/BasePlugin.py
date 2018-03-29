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

from pyengineer import LocalTemplateLookup

class BasePlugin(object):
	_ID = None
	_TITLE = None
	_MENU_HIERARCHY = None
	__FORM_TEMPLATE_PREFIX = "<%namespace file=\"plugin_form_lib.html\" import=\"*\" />\n"
	__RESPONSE_TEMPLATE_PREFIX = "<%namespace file=\"plugin_response_lib.html\" import=\"*\" />\n<%inherit file=\"plugin_response_base.html\" />\n"

	def __init__(self, configuration):
		assert(isinstance(self._ID, str))
		assert(isinstance(self._TITLE, str))
		assert(isinstance(self._MENU_HIERARCHY, tuple))
		self._config = configuration
		variables = {
			"request_uri":	self.__request_uri,
		}

		# Render the request handler completely now
		form_template = self.__FORM_TEMPLATE_PREFIX + self.form_template
		self._rendered_form_html = LocalTemplateLookup().create(form_template).render(**variables)

		# But only prepare the response handler (so we can render it with
		# actual responses later)
		if self.response_template is not None:
			response_template = self.__RESPONSE_TEMPLATE_PREFIX + self.response_template
			self._response_template = LocalTemplateLookup().create(response_template)
		else:
			self._response_template = None

	def __request_uri(self, endpoint = None):
		if endpoint is None:
			endpoint = "default"
		return "/plugins/" + self.plugin_id + "/" + endpoint

	@property
	def rendered_form_html(self):
		return self._rendered_form_html

	@property
	def plugin_id(self):
		return self._ID

	@property
	def plugin_title(self):
		return self._TITLE

	@property
	def plugin_menu_hierarchy(self):
		return self._MENU_HIERARCHY

	@property
	def config(self):
		return self._config

	@property
	def form_template(self):
		return "Template source undefined in derived class."

	@property
	def response_template(self):
		return None

	def render_response(self, response):
		if self._response_template is None:
			return "No response renderer defined in derived class.\n"
		else:
			return self._response_template.render(r = response)
