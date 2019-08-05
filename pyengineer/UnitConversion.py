#	pyengineer - Helping hand for electronics and mechanical engineering
#	Copyright (C) 2019-2019 Johannes Bauer
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

class UnitConversion(object):
	def __init__(self, known_units = None):
		if known_units is None:
			known_units = { }
		self._known_units = known_units

	def _get_conversion(self, unit_name):
		scalar_offset = self._known_units[unit_name]
		if isinstance(scalar_offset, (int, float)):
			# offset is zero
			return (scalar_offset, 0)
		else:
			return scalar_offset

	@classmethod
	def lengths(cls):
		return cls({
			"um":	1000,
			"mm":	1,
			"cm":	0.1,
			"m":	0.001,
			"in":	1 / 25.4,
			"ft":	1 / 12 / 25.4,
			"mil":	1 / (25.4 / 1000),
			"thou":	1 / (25.4 / 1000),
		})

	@classmethod
	def temperatures(cls):
		return cls({
			"K":	(1, 0),
			"C":	(1, -273.15),
			"F":	(1.8, (-273.15 * 1.8) + 32),
		})

	def add(self, new_unit_value, new_unit, known_unit_value, known_unit):
		if len(self._known_units) == 0:
			self._known_units[known_unit] = 1
		(known_scalar, known_offset) = self._get_conversion(known_unit)
		new_scalar = new_unit_value / known_unit_value * known_scalar
		self._known_units[new_unit] = new_scalar
		return self

	def add_complex(self, new_unit_value1, new_unit_value2, new_unit, known_unit_value1, known_unit_value2, known_unit):
		if len(self._known_units) == 0:
			self._known_units[known_unit] = 1
		(known_scalar, known_offset) = self._get_conversion(known_unit)
		new_value_delta = new_unit_value1 - new_unit_value2
		known_value_delta = known_unit_value1 - known_unit_value2
		new_unit_scalar = new_value_delta / (known_scalar * known_value_delta)

		xvalue = (known_unit_value1 - known_offset) / known_scalar
		new_unit_offset = new_unit_value1 - (xvalue * new_unit_scalar)
		self._known_units[new_unit] = (new_unit_scalar, new_unit_offset)

	def convert(self, value, from_unit, to_unit):
		(from_scalar, from_offset) = self._get_conversion(from_unit)
		(to_scalar, to_offset) = self._get_conversion(to_unit)
		#print("Converting %.3f %s [%.3f %.3f] -> %s [%.3f %.3f]" % (value, from_unit, from_scalar, from_offset, to_unit, to_scalar, to_offset))
		xvalue = (value - from_offset) / from_scalar
		result = (xvalue * to_scalar) + to_offset
		return result

	def convert_delta(self, value, from_unit, to_unit):
		(from_scalar, from_offset) = self._get_conversion(from_unit)
		(to_scalar, to_offset) = self._get_conversion(to_unit)
		return value / from_scalar * to_scalar
