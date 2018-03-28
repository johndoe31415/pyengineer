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
from pyengineer import UnitValue

class UnitValueTests(unittest.TestCase):
	def test_str_init(self):
		self.assertAlmostEqual(float(UnitValue("1.23456")), 1.23456)
		self.assertAlmostEqual(float(UnitValue(".23456")), .23456)
		self.assertAlmostEqual(float(UnitValue("0000.23456")), .23456)

	def test_str_units(self):
		self.assertAlmostEqual(float(UnitValue("12345f")), 12345e-15)
		self.assertAlmostEqual(float(UnitValue("12345p")), 12345e-12)
		self.assertAlmostEqual(float(UnitValue("12345n")), 12345e-9)
		self.assertAlmostEqual(float(UnitValue("12345u")), 12345e-6)
		self.assertAlmostEqual(float(UnitValue("12345m")), 12345e-3)
		self.assertAlmostEqual(float(UnitValue("12345")), 12345)
		self.assertAlmostEqual(float(UnitValue("12345k")), 12345e3)
		self.assertAlmostEqual(float(UnitValue("12345M")), 12345e6)
		self.assertAlmostEqual(float(UnitValue("12345G")), 12345e9)
		self.assertAlmostEqual(float(UnitValue("12345T")), 12345e12)

	def test_format(self):
		self.assertEqual(UnitValue("0").format(significant_digits = 1), "0")
		self.assertEqual(UnitValue("0").format(significant_digits = 2), "0.0")
		self.assertEqual(UnitValue("0").format(significant_digits = 3), "0.00")
		self.assertEqual(UnitValue("0").format(significant_digits = 4), "0.000")

		self.assertEqual(UnitValue("1").format(significant_digits = 1), "1")
		self.assertEqual(UnitValue("1").format(significant_digits = 2), "1.0")
		self.assertEqual(UnitValue("1").format(significant_digits = 3), "1.00")
		self.assertEqual(UnitValue("1").format(significant_digits = 4), "1.000")

		self.assertEqual(UnitValue("-1").format(significant_digits = 1), "-1")
		self.assertEqual(UnitValue("-1").format(significant_digits = 2), "-1.0")
		self.assertEqual(UnitValue("-1").format(significant_digits = 3), "-1.00")
		self.assertEqual(UnitValue("-1").format(significant_digits = 4), "-1.000")

		self.assertEqual(UnitValue("1").format(significant_digits = 3), "1.00")
		self.assertEqual(UnitValue("12").format(significant_digits = 3), "12.0")
		self.assertEqual(UnitValue("123").format(significant_digits = 3), "123")

		self.assertEqual(UnitValue("1").format(significant_digits = 4), "1.000")
		self.assertEqual(UnitValue("12").format(significant_digits = 4), "12.00")
		self.assertEqual(UnitValue("123").format(significant_digits = 4), "123.0")

		self.assertEqual(UnitValue("1234").format(significant_digits = 4), "1.234 k")
		self.assertEqual(UnitValue("12345").format(significant_digits = 4), "12.35 k")
		self.assertEqual(UnitValue("123456").format(significant_digits = 4), "123.5 k")
		self.assertEqual(UnitValue("123456").format(significant_digits = 5), "123.46 k")

	def test_format_units(self):
		self.assertEqual(UnitValue(1.23e-17).format(significant_digits = 3), "0.0123 f")
		self.assertEqual(UnitValue(1.23e-16).format(significant_digits = 3), "0.123 f")
		self.assertEqual(UnitValue(1.23e-15).format(significant_digits = 3), "1.23 f")
		self.assertEqual(UnitValue(1.23e-14).format(significant_digits = 3), "12.3 f")
		self.assertEqual(UnitValue(1.23e-13).format(significant_digits = 3), "123 f")
		self.assertEqual(UnitValue(1.23e-12).format(significant_digits = 3), "1.23 p")
		self.assertEqual(UnitValue(1.23e-11).format(significant_digits = 3), "12.3 p")
		self.assertEqual(UnitValue(1.23e-10).format(significant_digits = 3), "123 p")
		self.assertEqual(UnitValue(1.23e-9).format(significant_digits = 3), "1.23 n")
		self.assertEqual(UnitValue(1.23e-8).format(significant_digits = 3), "12.3 n")
		self.assertEqual(UnitValue(1.23e-7).format(significant_digits = 3), "123 n")
		self.assertEqual(UnitValue(1.23e-6).format(significant_digits = 3), "1.23 µ")
		self.assertEqual(UnitValue(1.23e-5).format(significant_digits = 3), "12.3 µ")
		self.assertEqual(UnitValue(1.23e-4).format(significant_digits = 3), "123 µ")
		self.assertEqual(UnitValue(1.23e-3).format(significant_digits = 3), "1.23 m")
		self.assertEqual(UnitValue(1.23e-2).format(significant_digits = 3), "12.3 m")
		self.assertEqual(UnitValue(1.23e-1).format(significant_digits = 3), "123 m")
		self.assertEqual(UnitValue(1.23e0).format(significant_digits = 3), "1.23")
		self.assertEqual(UnitValue(1.23e1).format(significant_digits = 3), "12.3")
		self.assertEqual(UnitValue(1.23e2).format(significant_digits = 3), "123")
		self.assertEqual(UnitValue(1.23e3).format(significant_digits = 3), "1.23 k")
		self.assertEqual(UnitValue(1.23e4).format(significant_digits = 3), "12.3 k")
		self.assertEqual(UnitValue(1.23e5).format(significant_digits = 3), "123 k")
		self.assertEqual(UnitValue(1.23e6).format(significant_digits = 3), "1.23 M")
		self.assertEqual(UnitValue(1.23e7).format(significant_digits = 3), "12.3 M")
		self.assertEqual(UnitValue(1.23e8).format(significant_digits = 3), "123 M")
		self.assertEqual(UnitValue(1.23e9).format(significant_digits = 3), "1.23 G")
		self.assertEqual(UnitValue(1.23e10).format(significant_digits = 3), "12.3 G")
		self.assertEqual(UnitValue(1.23e11).format(significant_digits = 3), "123 G")
		self.assertEqual(UnitValue(1.23e12).format(significant_digits = 3), "1.23 T")
		self.assertEqual(UnitValue(1.23e13).format(significant_digits = 3), "12.3 T")
		self.assertEqual(UnitValue(1.23e14).format(significant_digits = 3), "123 T")
		self.assertEqual(UnitValue(1.23e15).format(significant_digits = 3), "1.23 E")
		self.assertEqual(UnitValue(1.23e16).format(significant_digits = 3), "12.3 E")
		self.assertEqual(UnitValue(1.23e17).format(significant_digits = 3), "123 E")
		self.assertEqual(UnitValue(1.23e18).format(significant_digits = 3), "1230 E")
		self.assertEqual(UnitValue(1.23e19).format(significant_digits = 3), "12300 E")

