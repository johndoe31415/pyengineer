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
from pyengineer.ValueSets import ValueSets, UnitValue

class ValueSetTests(unittest.TestCase):
	def test_explicit(self):
		data = [
			{
				"name":		"foobar",
				"type":		"explicit",
				"items":	[ "1k", "5", "1", "10k", "10000", "5", "0.01M" ],
			}
		]
		sets = ValueSets.from_dict(data)
		vs = sets["foobar"]
		self.assertEqual(len(vs), 4)
		self.assertEqual([ float(x) for x in vs ], [ 1, 5, 1e3, 10e3 ])

	def test_eseries(self):
		data = [
			{
				"name":		"foobar",
				"type":		"eseries",
				"series":	6,
				"min":		"10",
				"max":		"1k",
			}
		]
		sets = ValueSets.from_dict(data)
		vs = sets["foobar"]
		self.assertEqual(len(vs), 13)
		self.assertEqual([ float(x) for x in vs ], [ 10, 15, 22, 33, 47, 68, 100, 150, 220, 330, 470, 680, 1000 ])

	def test_union(self):
		data = [
			{
				"name":		"foo",
				"type":		"explicit",
				"items":	[ "1k", "5", "1", "10k", "10000", "5", "0.01M" ],
			},
			{
				"name":		"bar",
				"type":		"explicit",
				"items":	[ "3", "33", "5", "1", "9" ],
			},
			{
				"name":		"foobar",
				"type":		"union",
				"groups":	[ "foo", "bar" ],
			},

		]
		sets = ValueSets.from_dict(data)
		vs = sets["foobar"]
		self.assertEqual(len(vs), 7)
		self.assertEqual([ float(x) for x in vs ], [ 1, 3, 5, 9, 33, 1e3, 10e3 ])


	def test_find_closest(self):
		data = [
			{
				"name":		"foobar",
				"type":		"explicit",
				"items":	[ "5", "7", "8", "9", "25" ],
			}
		]
		vs = ValueSets.from_dict(data)["foobar"]

		self.assertEqual(vs.find_closest(0), (None, UnitValue(5)))
		self.assertEqual(vs.find_closest(4), (None, UnitValue(5)))
		self.assertEqual(vs.find_closest(5), (UnitValue(5), UnitValue(7)))
		self.assertEqual(vs.find_closest(6), (UnitValue(5), UnitValue(7)))
		self.assertEqual(vs.find_closest(7), (UnitValue(7), UnitValue(8)))
		self.assertEqual(vs.find_closest(8), (UnitValue(8), UnitValue(9)))
		self.assertEqual(vs.find_closest(9), (UnitValue(9), UnitValue(25)))
		self.assertEqual(vs.find_closest(15), (UnitValue(9), UnitValue(25)))
		self.assertEqual(vs.find_closest(24), (UnitValue(9), UnitValue(25)))
		self.assertEqual(vs.find_closest(25), (UnitValue(25), None))
		self.assertEqual(vs.find_closest(1234), (UnitValue(25), None))
