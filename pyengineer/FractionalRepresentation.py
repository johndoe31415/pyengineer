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

class FractionalRepresentation(object):
	def __init__(self, value, max_abs_fractional_error = 0.005, max_denominator = 128):
		self._negative = value < 0
		if self.negative:
			value = -value

		self._whole = int(value)
		fraction = value - self._whole

		if fraction == 0:
			numerator = 0
			denominator = 1
		else:
			denominator = 1
			while denominator < max_denominator:
				denominator *= 2
				numerator = round(fraction * denominator)
				error = abs((numerator / denominator) - fraction)
				if error < max_abs_fractional_error:
					break
		self._numerator = numerator
		self._denominator = denominator
		self._fractional_error = (self._numerator / self._denominator) - fraction
		if value > 0:
			self._absolute_error = (float(self) - value) / value
		else:
			self._absolute_error = 0

	@property
	def negative(self):
		return self._negative

	@property
	def whole(self):
		return self._whole

	@property
	def numerator(self):
		return self._numerator

	@property
	def denominator(self):
		return self._denominator

	@property
	def absolute_error(self):
		return self._absolute_error

	@property
	def fractional_error(self):
		return self._fractional_error

	@property
	def is_zero(self):
		return (self.whole, self.numerator) == (0, 0)

	def __float__(self):
		sign = -1 if self.negative else 1
		return sign * (self.whole + (self.numerator / self.denominator))

	def to_string(self, whole_formatter = None, fractional_formatter = None):
		if whole_formatter is None:
			whole_formatter = str
		if fractional_formatter is None:
			fractional_formatter = lambda n, d: "%d/%d" % (n, d)

		sign = "-" if self.negative else ""
		text = [ ]
		if self.whole > 0:
			text.append(whole_formatter(self.whole))
		if self.numerator > 0:
			text.append(fractional_formatter(self.numerator, self.denominator))
		if len(text) == 0:
			text.append("0")
		text = sign + " ".join(text)
		return text

	@property
	def html(self):
		return self.to_string(fractional_formatter = lambda n, d: "<sup>%d</sup>/<sub>%d</sub>" % (n, d))

	def to_dict(self):
		return {
			"negative":		self.negative,
			"whole":		self.whole,
			"numerator":	self.numerator,
			"denominator":	self.denominator,
			"frac_error":	self.fractional_error,
			"abs_error":	self.absolute_error,
			"text":			str(self),
			"html":			self.html,
			"is_zero":		self.is_zero,
		}

	def __str__(self):
		return self.to_string()
