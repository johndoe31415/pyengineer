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
import flask
import traceback
import importlib.machinery
from mako.lookup import TemplateLookup
from .Exceptions import DuplicatePluginIDException, DuplicateEntryException

class MenuHierarchy(object):
	def __init__(self, name = None, parent = None):
		self._name = name
		self._parent = parent
		self._submenus = { }
		self._entries = { }
		if parent is None:
			self._id = self.local_id or "root"
		else:
			self._id = self._parent.id + "_" + self.local_id

	@property
	def id(self):
		return self._id

	@property
	def local_id(self):
		if self.name is None:
			return None
		else:
			return self.name.replace(" ", "")

	@property
	def name(self):
		return self._name

	@property
	def entries(self):
		return iter(self._entries.items())

	@property
	def submenus(self):
		return iter(self._submenus.values())

	def register(self, tree, value):
		key = tree[0]
		if len(tree) == 1:
			self._entries[key] = value
		else:
			if key not in self._submenus:
				self._submenus[key] = MenuHierarchy(name = key, parent = self)
			self._submenus[key].register(tree[1:], value)

	def dump(self, indent = 0):
		spaces = ("    " * indent)
		print("%s%s (%d entries)" % (spaces, self._name, len(self._entries)))
		for entry in self._entries:
			print("%s* %s" % (spaces, entry))
		for submenu in self.submenus:
			submenu.dump(indent + 1)

class GUIApplication(object):
	def __init__(self, config):
		self._plugins = { }
		self._menu = MenuHierarchy()
		self._config = config
		template_dir = os.path.dirname(__file__) + "/templates"
		self._lookup = TemplateLookup([ template_dir ], input_encoding = "utf-8", strict_undefined = True)
		self._app = flask.Flask(__name__)
		self._app.add_url_rule("/", "index", self._serve_index)
		self._app.add_url_rule("/config", "config", self._serve_config)
		self._app.add_url_rule("/plugins/<uuid:plugin_uuid>", "plugin_index", self._serve_plugin_index)
		self._app.add_url_rule("/plugins/<uuid:plugin_uuid>/<endpoint>", "plugin_request", self._serve_plugin_request, methods = [ "POST" ])
		self._load_plugins(self._config.plugin_directory)

	def _load_plugin(self, python_filename):
		module = importlib.machinery.SourceFileLoader("plugin_module", python_filename).load_module()
		plugin_class = module.Plugin
		instance = plugin_class(self._config)
		if instance.plugin_id in self._plugins:
			raise DuplicatePluginIDException("Cannot load plugin %s: Plugin with UUID %s already loaded (%s)." % (python_filename, instance.plugin_id, " -> ".join(self._plugins[instance.plugin_id].plugin_menu_hierarchy)))
		self._plugins[instance.plugin_id] = instance
		self._menu.register(instance.plugin_menu_hierarchy, instance)

	def _load_plugins(self, plugin_directory):
		if not plugin_directory.endswith("/"):
			plugin_directory += "/"
		for filename in filter(lambda name: name.endswith(".py"), os.listdir(plugin_directory)):
			full_filename = plugin_directory + filename
			self._load_plugin(full_filename)

	def _serve(self, template_name, variables = None):
		template = self._lookup.get_template(template_name)
		render_variables = {
			"title":		None,
			"menu":			self._menu,
		}
		if variables is not None:
			render_variables.update(variables)
		result = template.render(**render_variables)
		return result

	def _serve_index(self):
		return self._serve("index.html")

	def _serve_plugin_index(self, plugin_uuid):
		instance = self._plugins[str(plugin_uuid)]
		variables = {
			"title":				instance.plugin_title,
			"rendered_form_html":	instance.rendered_form_html,
		}
		return self._serve("plugin.html", variables)

	def _serve_plugin_request(self, plugin_uuid, endpoint):
		instance = self._plugins[str(plugin_uuid)]
		if "Accept" not in flask.request.headers:
			return flask.jsonify({
				"status":		"failed",
				"errorcode":	"NoAcceptHeader",
				"description":	"No 'Accept' header set.",
			})

		accepts = flask.request.accept_mimetypes.best_match([ "application/json", "text/html" ])
		if accepts == "application/json":
			renderer = flask.jsonify
		elif accepts == "text/html":
			renderer = instance.render_response
		else:
			return flask.jsonify({
				"status":		"failed",
				"errorcode":	"UnknownAcceptHeader",
				"description":	"'Accept' header must be either application/json or text/html, but was '%s'." % (flask.request.headers["Accept"]),
			})

		input_data = flask.request.json
		if input_data is None:
			return renderer({
				"status":		"failed",
				"errorcode":	"JSONInputWasNone",
				"description":	"No JSON input provided.",
			})
		try:
			result = instance.request(endpoint, flask.request.json)
		except (KeyError, ValueError) as e:
			print(traceback.format_exc())
			return renderer({
				"status":		"exception",
				"errorcode":	e.__class__.__name__,
				"description":	str(e),
			})

		return renderer({
			"status":		"ok",
			"data":			result,
		})

	def _serve_config(self):
		return flask.jsonify(self._config.json())

	@property
	def app(self):
		return self._app

