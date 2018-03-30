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

		self._valuesets = { }
		for (group, valuesets_data) in self._raw_config["valuesets"].items():
			self._valuesets[group] = ValueSets.from_dict(valuesets_data)

		self._config_dict = self._create_dict()

	def to_dict(self):
		return self._config_dict

	def _create_dict(self):
		data = {
			"valuesets": { },
		}
		repr_callbacks = {
			"frequency":	lambda value: value.format(significant_digits = 6),
			"r":			lambda value: value.format(significant_digits = 3),
			"c":			lambda value: value.format(significant_digits = 3),
			"l":			lambda value: value.format(significant_digits = 3),
		}
		for (group, valuesets) in self._valuesets.items():
			data["valuesets"][group] = [ ]
			for valueset in valuesets:
				data["valuesets"][group].append(valueset.to_dict(repr_callback = repr_callbacks.get(group)))
		return data

	def get_valuesets(self, group):
		if group not in self._valuesets:
			raise KeyError("No such ValueSet: %s" % (group))
		return self._valuesets[group]

	@property
	def plugin_directory(self):
		# TODO: Hardcoded for now
		return "plugins"
