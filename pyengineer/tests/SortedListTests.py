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
from pyengineer.SortedList import SortedList

class SortedListTests(unittest.TestCase):
	def test_empty(self):
		sl = SortedList([ ])
		(less, more) = sl.less_more(123)
		self.assertEqual(less, None)
		self.assertEqual(more, None)

		less_more_list = sl.less_more_list(123)
		self.assertEqual(less_more_list, [ ])

	def test_simple(self):
		sl = SortedList(range(50))
		(less, more) = sl.less_more(12.345)
		self.assertEqual(less, 12)
		self.assertEqual(more, 13)
		self.assertEqual(sl.less_more_list(12.345), [ 12, 13 ])

		(less, more) = sl.less_more(12)
		self.assertEqual(less, 12)
		self.assertEqual(more, 13)
		self.assertEqual(sl.less_more_list(12), [ 12, 13 ])

		(less, more) = sl.less_more(11.9)
		self.assertEqual(less, 11)
		self.assertEqual(more, 12)
		self.assertEqual(sl.less_more_list(11.9), [ 11, 12 ])

		(less, more) = sl.less_more(13)
		self.assertEqual(less, 13)
		self.assertEqual(more, 14)
		self.assertEqual(sl.less_more_list(13), [ 13, 14 ])

		(less, more) = sl.less_more(0)
		self.assertEqual(less, 0)
		self.assertEqual(more, 1)
		self.assertEqual(sl.less_more_list(0), [ 0, 1 ])

		(less, more) = sl.less_more(0.1)
		self.assertEqual(less, 0)
		self.assertEqual(more, 1)
		self.assertEqual(sl.less_more_list(0.1), [ 0, 1 ])

		(less, more) = sl.less_more(48.9)
		self.assertEqual(less, 48)
		self.assertEqual(more, 49)
		self.assertEqual(sl.less_more_list(48.9), [ 48, 49 ])

	def test_noless(self):
		sl = SortedList(range(50))
		(less, more) = sl.less_more(-1)
		self.assertEqual(less, None)
		self.assertEqual(more, 0)
		self.assertEqual(sl.less_more_list(-1), [ 0 ])

	def test_nomore(self):
		sl = SortedList(range(50))
		(less, more) = sl.less_more(200)
		self.assertEqual(less, 49)
		self.assertEqual(more, None)
		self.assertEqual(sl.less_more_list(200), [ 49 ])
