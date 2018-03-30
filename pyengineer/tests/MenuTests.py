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
from pyengineer.MenuHierarchy import MenuHierarchy
from pyengineer.Exceptions import DuplicateEntryException

class MenuTests(unittest.TestCase):
	def test_flat(self):
		menu = MenuHierarchy()
		menu.register(1, ("Foo", ), "Foo-Item")
		menu.register(2, ("Bar", ), "Bar-Item")
		menu.register(3, ("Moo", ), "Moo-Item")

		self.assertEqual(menu[1], "Foo-Item")
		self.assertEqual(menu[2], "Bar-Item")
		self.assertEqual(menu[3], "Moo-Item")


	def test_duplicate_id(self):
		menu = MenuHierarchy()
		menu.register(3, ("Moo", ), "Moo-Item")
		with self.assertRaises(DuplicateEntryException):
			menu.register(3, ("asd", ), "asd-Item")

	def test_duplicate_name(self):
		menu = MenuHierarchy()
		menu.register(3, ("Moo", ), "Moo-Item")
		with self.assertRaises(DuplicateEntryException):
			menu.register(4, ("Moo", ), "asd-Item")

	def test_submenu_simple(self):
		menu = MenuHierarchy()
		menu.register(1, ("Basic", "Foo", ), "Foo-Item")
		menu.register(2, ("Basic", "Bar", ), "Bar-Item")
		menu.register(3, ("Basic", "Moo", ), "Moo-Item")
		menu.register(4, ("Second", "Moo", ), "Moo2-Item")
		menu.register(5, ("Second", "Koo", ), "Koo2-Item")
		self.assertEqual(menu[1], "Foo-Item")
		self.assertEqual(menu[5], "Koo2-Item")
		self.assertTrue(menu.root.has_entry(("Basic", )))
		self.assertTrue(menu.root.has_entry(("Basic", "Foo")))
		self.assertFalse(menu.root.has_entry(("X", "Y", "Z")))
		self.assertFalse(menu.root.has_entry(("Basic", "XYZ")))
		self.assertEqual(len(list(menu.root.children)), 2)
		self.assertEqual(len(list(list(menu.root.children)[0].children)), 3)
		self.assertEqual(len(list(list(menu.root.children)[1].children)), 2)

	def test_submenu_deep_dualuse(self):
		menu = MenuHierarchy()
		menu.register(1, ("Basic", "Foo", "LOL", "Koo"), "Koo1-Item")
		menu.register(2, ("Basic", "Foo", "LOL2", "Koo2"), "Koo2-Item")
		menu.register(3, ("Basic", "Foo4", "LOL2", "Koo2"), "Koo3-Item")
		menu.register(4, ("Basic", "Foo4", "LOL3", "Koo2"), "Koo4-Item")
		with self.assertRaises(DuplicateEntryException):
			menu.register(5, ("Basic", "Foo4", "LOL3", "Koo2", "Meh"), "Koo4-Item")

	def test_node_id(self):
		menu = MenuHierarchy()
		menu.register(1, ("Basic", "Foo", "LOL", "Koo"), "Koo1-Item")
		leaf_node = menu.root.get_entry(("Basic", "Foo", "LOL", "Koo"))
		self.assertTrue(leaf_node.is_leaf)
		self.assertFalse(leaf_node.has_children)
		self.assertEqual(leaf_node.node_id, "<root> / Basic / Foo / LOL / Koo")
		self.assertEqual(leaf_node.node_hash, "9f7630293d88cb2a")

	def test_sort(self):
		menu = MenuHierarchy()
		menu.register(1, ("X", "Y", ), "Foo-Item")
		menu.register(2, ("Y", "X", ), "Bar-Item")
		menu.register(3, ("D", "1", ), "Moo-Item")
		menu.register(4, ("D", "2", ), "Moo2-Item")
		menu.register(5, ("D", "3", ), "Koo2-Item")
		menu.register(6, ("A", ), "Leafy")
		menu.register(7, ("X", "E", ), "Last-Item")
		menu.sort()

		base = list(menu.root.children)
		self.assertEqual(len(base), 4)
		self.assertEqual(base[0].name, "D")
		self.assertEqual(base[1].name, "X")
		self.assertEqual(base[2].name, "Y")
		self.assertEqual(base[3].name, "A")

		sub = list(base[1].children)
		self.assertEqual(len(sub), 2)
		self.assertEqual(sub[0].name, "E")
		self.assertEqual(sub[1].name, "Y")
