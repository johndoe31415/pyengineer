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

import bisect
from pyengineer import UnitValue, ESeries
from pyengineer.Exceptions import DuplicateEntryException, DataMissingException, InvalidDataException

class ValueSet(object):
	def __init__(self, name, values, resolved = True):
		self._name = name
		self._values = tuple(sorted(set(values)))
		self._resolved = resolved

	def find_closest(self, value):
		value = UnitValue(value)
		index = bisect.bisect(self._values, value) - 1
		if index >= 0:
			smaller = self._values[index]
		else:
			smaller = None
		if index + 1 < len(self._values):
			larger = self._values[index + 1]
		else:
			larger = None
		return (smaller, larger)

	@property
	def name(self):
		return self._name

	@classmethod
	def from_dict(cls, dict_data):
		if not "name" in dict_data:
			raise DataMissingException("No 'name' attribute in ValueSet definition: %s" % (str(dict_data)))
		if not "type" in dict_data:
			raise DataMissingException("No 'type' attribute in ValueSet definition: %s" % (str(dict_data)))

		vs_type = dict_data["type"]
		if vs_type == "explicit":
			if not "items" in dict_data:
				raise DataMissingException("No 'items' attribute in explicit ValueSet definition: %s" % (str(dict_data)))
			return cls(name = dict_data["name"], values = [ UnitValue(v) for v in dict_data["items"] ])
		elif vs_type == "eseries":
			if not "series" in dict_data:
				raise DataMissingException("No 'series' attribute in eseries ValueSet definition: %s" % (str(dict_data)))
			if not "min" in dict_data:
				raise DataMissingException("No 'min' attribute in eseries ValueSet definition: %s" % (str(dict_data)))
			if not "max" in dict_data:
				raise DataMissingException("No 'max' attribute in eseries ValueSet definition: %s" % (str(dict_data)))

			eseries = ESeries.standard(dict_data["series"])
			(minval, maxval) = UnitValue(dict_data["min"]), UnitValue(dict_data["max"])
			values = [ UnitValue(v) for v in eseries.from_to(minval.exact_value, maxval.exact_value, maxvalue_inclusive = True) ]
			return cls(name = dict_data["name"], values = values)
		else:
			raise InvalidDataException("Invalid 'type' attribute of ValueSet '%s': %s" % (vs_type, str(dict_data)))

	def __iter__(self):
		return iter(self._values)

	def __len__(self):
		return len(self._values)

	def resolved(self):
		return self._resolved

	def resolve(self, valuesets):
		pass

class ValueSets(object):
	def __init__(self):
		self._sets = { }


	def add_set(self, valueset):
		if valueset.name in self._sets:
			raise DuplicateEntryException("Valueset %s defined twice." % (valueset.name))
		self._sets[valueset.name] = valueset

	@classmethod
	def from_dict(cls, dict_data):
		valuesets = cls()

		# Add all sets first
		for valueset_data in dict_data:
			valueset = ValueSet.from_dict(valueset_data)
			valuesets.add_set(valueset)

		# Do a second pass over all valuesets to resolve cross-references
		# TODO: This in unable to handle recursive cross-references for now
		for valueset in valuesets:
			if not valueset.resolved:
				valueset.resolve(self)

		return valuesets

	def __getitem__(self, set_name):
		return self._sets[set_name]

	def __iter__(self):
		return iter(self._sets.values())
