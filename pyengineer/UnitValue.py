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

import enum
import math
import collections
from fractions import Fraction

class UnitValue(object):
	_SI_PREFIXES = (
		("f",	-15),
		("p",	-12),
		("n",	-9),
		("µ",	-6),
		("u",	-6),
		("m",	-3),
		("k",	3),
		("M",	6),
		("G",	9),
		("T",	12),
		("E",	15),
	)

	def __init__(self, value, repr_callback = None):
		self._repr_callback = repr_callback
		if isinstance(value, UnitValue):
			self._value = value._value
			self._raw_value = value._raw_value
		else:
			self._raw_value = value

			# Unit specified?
			exponent = 0
			if isinstance(value, str):
				value = value.rstrip("\t\n ")
				for (si_prefix, si_exponent) in self._SI_PREFIXES:
					if value.endswith(si_prefix):
						exponent = si_exponent
						value = value[:-len(si_prefix)]
						break
			if exponent > 0:
				self._value = Fraction(value) * (10 ** exponent)
			else:
				self._value = Fraction(value) / (10 ** -exponent)
		if self._repr_callback is None:
			self._repr_callback = lambda value: value.raw_value

	@property
	def exact_value(self):
		return self._value

	@property
	def raw_value(self):
		return self._raw_value

	@property
	def representation(self):
		return self._repr_callback(self)

	def format(self, significant_digits = 3):
		assert(significant_digits >= 1)
		if self._value < 0:
			value = -self._value
			sign = "-"
		else:
			value = self._value
			sign = ""
		if (value == 0) or (1 <= value < 1000):
			si_prefix = None
			mantissa = float(value)
		else:
			for (si_prefix, si_exponent) in self._SI_PREFIXES:
				if si_exponent > 0:
					mantissa = value / (10 ** si_exponent)
				else:
					mantissa = value * (10 ** -si_exponent)
				if 1 <= mantissa < 1000:
					break
			else:
				if self._value < 1:
					# Smaller than smallest unit
					(si_prefix, si_exponent) = self._SI_PREFIXES[0]
				else:
					# Larger than largest unit
					(si_prefix, si_exponent) = self._SI_PREFIXES[-1]
				mantissa = float(value / (10 ** si_exponent))
		if value == 0:
			pre_decimal = 1
		else:
			pre_decimal = math.floor(math.log10(mantissa)) + 1
		post_decimal = significant_digits - pre_decimal
		if post_decimal < 0:
			post_decimal = 0
		if si_prefix is None:
			unit_str = ""
		else:
			unit_str = si_prefix
		return "%s%.*f %s" % (sign, post_decimal, mantissa, unit_str)

	def to_dict(self, significant_digits = 3, include_raw = False, include_repr = False, include_fractional = False):
		result = {
			"flt":		float(self),
			"fmt":		self.format(significant_digits = significant_digits),
		}
		if include_raw:
			result["raw"] = self.raw_value
		if include_fractional:
			result["repr"] = self.representation
		if include_fractional:
			result["fractional"] = self.get_fractional()
		return result

	def __ge__(self, other):
		return self._value >= other._value

	def __gt__(self, other):
		return self._value > other._value

	def __le__(self, other):
		return self._value <= other._value

	def __lt__(self, other):
		return self._value < other._value

	def __eq__(self, other):
		return self._value == other._value

	def __neq__(self, other):
		return not (self == other)

	def __hash__(self):
		return hash(self._value)

	def __float__(self):
		return float(self._value)

	def __repr__(self):
		return "UV(%s)" % (self.representation)

	def __str__(self):
		return self.format(significant_digits = 3)
