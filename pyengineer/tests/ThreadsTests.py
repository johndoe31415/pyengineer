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
import pkgutil
import json
from pyengineer import Thread, ThreadDB

class ThreadsTests(unittest.TestCase):
	def test_basic(self):
		thread = Thread(diameter = 3, pitch = 0.25)
		self.assertAlmostEqual(thread.diameter, 3)
		self.assertAlmostEqual(thread.pitch, 0.25)

	def test_db(self):
		database_data = json.loads(pkgutil.get_data("pyengineer.data", "threads.json"))
		db = ThreadDB()
		db.add_groups_by_definition(database_data)
		print(db)
