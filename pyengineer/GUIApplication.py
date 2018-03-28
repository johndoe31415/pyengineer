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
from flask import Flask
from mako.lookup import TemplateLookup

class GUIApplication(object):
	def __init__(self, config):
		self._config = config
		print(__file__)
		template_dir = os.path.dirname(__file__) + "/templates"
		self._lookup = TemplateLookup([ template_dir ], input_encoding = "utf-8")
		self._app = Flask(__name__)
		self._app.add_url_rule("/", "index", self._serve_index)

	def _serve(self, template_name):
		template = self._lookup.get_template(template_name)
		result = template.render()
		return result

	def _serve_index(self):
		return self._serve("index.html")

	@property
	def app(self):
		return self._app

#app = Flask(__name__)
#ctrlr = GUIApplicationController(app)
#@app.route("/")
#def index():
#	return "Hello, World!"
