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

class OrderedSet(object):
	def __init__(self):
		self._ordered_tuple = tuple()
		self._sorted_tuple = tuple()
		self._set = set()

	def add_items(self, items):
		new_item_list = list(self._ordered_tuple)
		for item in items:
			if item not in self._set:
				self._set.add(item)
				new_item_list.append(item)
		self._ordered_tuple = tuple(new_item_list)
		self._sorted_tuple = tuple(sorted(new_item_list))

	def add_item(self, item):
		return self.add_items([ item ])

	@property
	def ordered_tuple(self):
		return self._ordered_tuple

	@property
	def sorted_tuple(self):
		return self._sorted_tuple

	def __getitem__(self, index):
		return self._sorted_tuple[index]

	def __len__(self):
		return len(self._sorted_tuple)

	def __iter__(self):
		return iter(self.sorted_tuple)
