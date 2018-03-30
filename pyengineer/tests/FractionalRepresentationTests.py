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

import unittest
from fractions import Fraction
from pyengineer import FractionalRepresentation

class FractionalRepresentationTests(unittest.TestCase):
	def test_whole(self):
		value = FractionalRepresentation(Fraction("123"))
		self.assertEqual(value.whole, 123)
		self.assertEqual(value.numerator, 0)
		self.assertEqual(value.denominator, 1)
		self.assertEqual(str(value), "123")

		value = FractionalRepresentation(Fraction("123.5"))
		self.assertEqual(value.whole, 123)
		self.assertEqual(value.numerator, 1)
		self.assertEqual(value.denominator, 2)
		self.assertEqual(str(value), "123 1/2")

		value = FractionalRepresentation(Fraction("123.25"))
		self.assertEqual(value.whole, 123)
		self.assertEqual(value.numerator, 1)
		self.assertEqual(value.denominator, 4)
		self.assertEqual(str(value), "123 1/4")

		value = FractionalRepresentation(Fraction("123.375"))
		self.assertEqual(value.whole, 123)
		self.assertEqual(value.numerator, 3)
		self.assertEqual(value.denominator, 8)
		self.assertEqual(str(value), "123 3/8")

		value = FractionalRepresentation(Fraction("123.5546875"))
		self.assertEqual(value.whole, 123)
		self.assertEqual(value.numerator, 71)
		self.assertEqual(value.denominator, 128)
		self.assertEqual(str(value), "123 71/128")

	def test_negative(self):
		value = FractionalRepresentation(Fraction("-123"))
		self.assertEqual(value.whole, 123)
		self.assertTrue(value.negative)
		self.assertEqual(str(value), "-123")

		value = FractionalRepresentation(Fraction("123"))
		self.assertEqual(value.whole, 123)
		self.assertFalse(value.negative)

	def test_approximate(self):
		value = FractionalRepresentation(Fraction("123.400"))
		self.assertEqual(value.whole, 123)
		self.assertEqual(value.numerator, 51)
		self.assertEqual(value.denominator, 128)

	def test_tolerance(self):
		value = FractionalRepresentation(Fraction("123.700"), max_abs_fractional_error = 0.1)
		self.assertEqual(value.whole, 123)
		self.assertEqual(value.numerator, 3)
		self.assertEqual(value.denominator, 4)

		value = FractionalRepresentation(Fraction("123.700"), max_abs_fractional_error = 0.01)
		self.assertEqual(value.whole, 123)
		self.assertEqual(value.numerator, 45)
		self.assertEqual(value.denominator, 64)

	def test_error(self):
		value = FractionalRepresentation(Fraction("123.700"), max_abs_fractional_error = 0.1)
		self.assertEqual(value.whole, 123)
		self.assertEqual(value.numerator, 3)
		self.assertEqual(value.denominator, 4)
		self.assertAlmostEqual(value.fractional_error, 0.05)
		self.assertAlmostEqual(value.absolute_error, 0.0004042037186741888)

		value = FractionalRepresentation(Fraction("123.800"), max_abs_fractional_error = 0.1)
		self.assertEqual(value.whole, 123)
		self.assertEqual(value.numerator, 3)
		self.assertEqual(value.denominator, 4)
		self.assertAlmostEqual(value.fractional_error, -0.05)
		self.assertAlmostEqual(value.absolute_error, -0.0004038772213247173)

		value = FractionalRepresentation(Fraction("1.700"), max_abs_fractional_error = 0.1)
		self.assertEqual(value.whole, 1)
		self.assertEqual(value.numerator, 3)
		self.assertEqual(value.denominator, 4)
		self.assertAlmostEqual(value.fractional_error, 0.05)
		self.assertAlmostEqual(value.absolute_error, 0.029411764705882356)

