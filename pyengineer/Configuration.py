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
import collections
from pyengineer import UnitValue
from pyengineer.ValueSets import ValueSets

class Configuration(object):
	def __init__(self, json_filename):
		with open(json_filename, "r") as f:
			self._raw_config = json.loads(f.read())

		self._sets = { }
		for (set_group, sets_data) in self._raw_config["sets"].items():
			self._sets[set_group] = ValueSets.from_dict(sets_data)

	def get_valuesets(self, valueset_group):
		return self._sets[valueset_group]

	@property
	def plugin_directory(self):
		# TODO: Hardcoded for now
		return "plugins"

	def json(self):
		data = {
			"sets": collections.defaultdict(list),
			"values": collections.defaultdict(list),
		}
		for (set_name, sets) in self._raw_config["sets"].items():
			for specific_set in sets:
				data["sets"][set_name].append(specific_set["name"])

		repr_callbacks = {
			"frequencies":	lambda value: value.format(significant_digits = 6),
		}
		for (value_name, values) in self._raw_config["values"].items():
			for value in values:
				data["values"][value_name].append(UnitValue(value, repr_callback = repr_callbacks.get(value_name)).json())
		return data
