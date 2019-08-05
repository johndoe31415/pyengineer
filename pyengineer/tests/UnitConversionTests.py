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
from pyengineer import UnitConversion

class UnitConversionTests(unittest.TestCase):
	def test_nonexist(self):
		uc = UnitConversion.lengths()
		with self.assertRaises(KeyError):
			uc.convert(1, "m", "foobar")

	def test_convert(self):
		uc = UnitConversion({
			"mm":	1,
			"cm":	0.1,
			"m":	0.001,
			"in":	1 / 25.4,
		})
		self.assertAlmostEqual(uc.convert(1, "mm", "m"), 0.001)
		self.assertAlmostEqual(uc.convert(1, "in", "mm"), 25.4)
		self.assertAlmostEqual(uc.convert(1, "m", "cm"), 100)
		self.assertAlmostEqual(uc.convert(1, "cm", "m"), 0.01)
		self.assertAlmostEqual(uc.convert(12, "in", "cm"), 30.48)
		self.assertAlmostEqual(uc.convert(123, "cm", "m"), 1.23)

	def test_convert_lengths(self):
		uc = UnitConversion.lengths()
		self.assertAlmostEqual(uc.convert(1, "m", "m"), 1)
		self.assertAlmostEqual(uc.convert(1, "m", "ft"), 3.28084, places = 4)
		self.assertAlmostEqual(uc.convert(1, "m", "in"), 39.3701, places = 4)
		self.assertAlmostEqual(uc.convert(1, "m", "cm"), 100)
		self.assertAlmostEqual(uc.convert(1, "m", "mm"), 1000)
		self.assertAlmostEqual(uc.convert(1000, "mil", "in"), 1)
		self.assertAlmostEqual(uc.convert(1, "in", "thou"), 1000)

	def test_add_unit(self):
		uc = UnitConversion()
		uc.add(1, "in", 25.4, "mm")
		self.assertAlmostEqual(uc.convert(1, "in", "mm"), 25.4)
		self.assertAlmostEqual(uc.convert(25.4, "mm", "in"), 1)

		uc.add(1, "ft", 12, "in")
		uc.add(1, "m", 1000, "mm")
		self.assertAlmostEqual(uc.convert(1, "m", "ft"), 3.28084, places = 4)
		self.assertAlmostEqual(uc.convert(1, "m", "in"), 39.3701, places = 4)

	def test_convert_temperatures(self):
		uc = UnitConversion.temperatures()
		self.assertAlmostEqual(uc.convert(0, "K", "C"), -273.15)
		self.assertAlmostEqual(uc.convert(0, "C", "K"), 273.15)
		self.assertAlmostEqual(uc.convert(10, "C", "K"), 283.15)
		self.assertAlmostEqual(uc.convert(10, "K", "C"), -263.15)
		self.assertAlmostEqual(uc.convert(0, "C", "F"), 32)
		self.assertAlmostEqual(uc.convert(32, "F", "C"), 0)
		self.assertAlmostEqual(uc.convert(100, "C", "F"), 212)
		self.assertAlmostEqual(uc.convert(212, "F", "C"), 100)
		self.assertAlmostEqual(uc.convert(-40, "C", "F"), -40)
		self.assertAlmostEqual(uc.convert(-40, "F", "C"), -40)
		self.assertAlmostEqual(uc.convert(50, "C", "F"), 122)
		self.assertAlmostEqual(uc.convert(122, "F", "C"), 50)

	def test_convert_complex_offset_only(self):
		uc = UnitConversion()
		uc.add_complex(-273.15, -263.15, "C", 0, 10, "K")
		self.assertAlmostEqual(uc.convert(0, "K", "C"), -273.15)
		self.assertAlmostEqual(uc.convert(0, "C", "K"), 273.15)
		self.assertAlmostEqual(uc.convert(10, "C", "K"), 283.15)
		self.assertAlmostEqual(uc.convert(10, "K", "C"), -263.15)
		self.assertAlmostEqual(uc.convert(100, "C", "K"), 373.15)
		self.assertAlmostEqual(uc.convert(100, "K", "C"), -173.15)

		uc = UnitConversion()
		uc.add_complex(0, 10, "K", -273.15, -263.15, "C")
		self.assertAlmostEqual(uc.convert(0, "K", "C"), -273.15)
		self.assertAlmostEqual(uc.convert(0, "C", "K"), 273.15)
		self.assertAlmostEqual(uc.convert(100, "C", "K"), 373.15)
		self.assertAlmostEqual(uc.convert(100, "K", "C"), -173.15)

	def test_convert_complex_offset_scalar(self):
		uc = UnitConversion()
		uc.add_complex(50, 212, "F", 10, 100, "C")
		self.assertAlmostEqual(uc.convert(0, "C", "F"), 32)
		self.assertAlmostEqual(uc.convert(32, "F", "C"), 0)
		self.assertAlmostEqual(uc.convert(100, "C", "F"), 212)
		self.assertAlmostEqual(uc.convert(212, "F", "C"), 100)
		self.assertAlmostEqual(uc.convert(-40, "C", "F"), -40)
		self.assertAlmostEqual(uc.convert(-40, "F", "C"), -40)
		self.assertAlmostEqual(uc.convert(50, "C", "F"), 122)
		self.assertAlmostEqual(uc.convert(122, "F", "C"), 50)

	def test_convert_complex_offset_scalar_multi(self):
		uc = UnitConversion()
		uc.add_complex(10, 20, "*10", 1, 2, "base")
		self.assertAlmostEqual(uc.convert(3, "base", "*10"), 30)
		self.assertAlmostEqual(uc.convert(30, "*10", "base"), 3)

		uc.add_complex(15, 25, "*10+5", 1, 2, "base")
		self.assertAlmostEqual(uc.convert(3, "base", "*10+5"), 35)
		self.assertAlmostEqual(uc.convert(35, "*10+5", "base"), 3)
		self.assertAlmostEqual(uc.convert(27, "base", "*10+5"), 275)

		uc.add_complex(102, 104, "*2+100", 1, 2, "base")
		self.assertAlmostEqual(uc.convert(3, "base", "*2+100"), 106)
		self.assertAlmostEqual(uc.convert(106, "*2+100", "base"), 3)
		self.assertAlmostEqual(uc.convert(27, "base", "*2+100"), 154)
		self.assertAlmostEqual(uc.convert(154, "*2+100", "base"), 27)

		self.assertAlmostEqual(uc.convert(154, "*2+100", "*10+5"), 275)
		self.assertAlmostEqual(uc.convert(275, "*10+5", "*2+100"), 154)
