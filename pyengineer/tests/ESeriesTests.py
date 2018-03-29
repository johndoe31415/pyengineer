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
import fractions
from pyengineer import ESeries

class ESeriesTests(unittest.TestCase):
	def test_basic(self):
		e6 = ESeries.standard(6)
		self.assertAlmostEqual(e6.closest(9999).value, 10000)
		self.assertAlmostEqual(e6.closest(12345).value, 10000)
		self.assertAlmostEqual(e6.closest(12499).value, 10000)
		self.assertAlmostEqual(e6.closest(12501).value, 15000)
		self.assertAlmostEqual(e6.closest(20000).value, 22000)

		self.assertAlmostEqual(e6.closest(200000).value, 220000)
		self.assertAlmostEqual(e6.closest(2000000).value, 2200000)
		self.assertAlmostEqual(e6.closest(20000000).value, 22000000)

	def test_range(self):
		for series in [ 3, 6, 12, 24, 48, 192 ]:
			eseries = ESeries.standard(series)
			values = list(eseries.from_to(1000, 10000))
			self.assertEqual(len(values), series)

		eseries = ESeries.standard(6)
		values = list(eseries.from_to(1000, 10000))
		self.assertEqual(values, [ 1e3, 1.5e3, 2.2e3, 3.3e3, 4.7e3, 6.8e3 ])

		values = list(eseries.from_to(1000, 10001))
		self.assertEqual(values, [ 1e3, 1.5e3, 2.2e3, 3.3e3, 4.7e3, 6.8e3, 10e3 ])

	def test_range_inclusive(self):
		eseries = ESeries.standard(6)
		values = list(eseries.from_to(1000, 10000, maxvalue_inclusive = True))
		self.assertEqual(values, [ 1e3, 1.5e3, 2.2e3, 3.3e3, 4.7e3, 6.8e3, 10e3 ])

	def test_range_extreme(self):
		eseries = ESeries.standard(6)

		value = fractions.Fraction(33, 100000000000000000)
		self.assertEqual(eseries.closest(value).value, value)

		value = fractions.Fraction(3300000000000000000, 1)
		self.assertEqual(eseries.closest(value).value, value)
