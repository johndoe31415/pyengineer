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

import json
import uuid
from pyengineer import LocalTemplateLookup

class BasePlugin(object):
	_ID = None
	_TITLE = None
	_MENU_HIERARCHY = None
	_FORM_TEMPLATE = None
	_RESPONSE_TEMPLATE = None
	__FORM_TEMPLATE_PREFIX = "<%namespace file=\"plugin_form_lib.html\" import=\"*\" />\n"
	__RESPONSE_TEMPLATE_PREFIX = "<%namespace file=\"plugin_response_lib.html\" import=\"*\" />\n<%inherit file=\"plugin_response_base.html\" />\n"

	def __init__(self, configuration, instanciated_from = None):
		assert(isinstance(self._ID, str))
		assert(isinstance(self._TITLE, str))
		assert(isinstance(self._MENU_HIERARCHY, tuple))
		self.__config = configuration
		self.__instanciated_from = instanciated_from
		variables = {
			"request_uri":	self.__request_uri,
			"title":		self.plugin_title,
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
		return "/plugins/" + str(self.plugin_id) + "/" + endpoint

	@property
	def rendered_form_html(self):
		return self._rendered_form_html

	@property
	def instanciated_from(self):
		return self.__instanciated_from

	@property
	def plugin_id(self):
		return uuid.UUID(self._ID)

	@property
	def plugin_title(self):
		return self._TITLE

	@property
	def plugin_menu_hierarchy(self):
		return self._MENU_HIERARCHY

	@property
	def form_template(self):
		return self._FORM_TEMPLATE

	@property
	def response_template(self):
		return self._RESPONSE_TEMPLATE

	@property
	def config(self):
		return self.__config

	def render_response(self, response):
		if self._response_template is None:
			return "No response renderer defined in derived class.\n"
		else:
			variables = {
				"r":	response,
				"d":	response.get("data"),
			}
			return self._response_template.render(**variables)

	def dump_request(self, parameters, endpoint = "default"):
		print("Request <%s>:" % (endpoint))
		print(json.dumps(parameters, sort_keys = True, indent = 4))
		response = self.request(endpoint, parameters)
		print("Response:")
		try:
			print(json.dumps(response, sort_keys = True, indent = 4))
			template_input = {
				"status":	"ok",
				"data":		response,
			}
			try:
				print(self.render_response(template_input))
			except TypeError as e:
				print("Error during rendering: %s" % (str(e)))
				print(template_input)
		except TypeError as e:
			print("Error during serialization: %s" % (str(e)))
			print(response)
		print()
		return response

	def __str__(self):
		return "Plugin<%s / %s from %s>" % (self.plugin_title, self.plugin_id, self.instanciated_from)
