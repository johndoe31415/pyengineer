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

import hashlib
from .Exceptions import DuplicateEntryException

class BaseMenuNode(object):
	def __init__(self, name = None, parent = None):
		self._name = name
		self._parent = parent

	@property
	def node_id(self):
		if self.parent is None:
			return "<root>"
		else:
			return self.parent.node_id + " / " + self.name

	@property
	def node_hash(self):
		node_id = self.node_id.encode("utf-8")
		return hashlib.md5(node_id).hexdigest()[:16]

	@property
	def is_leaf(self):
		return False

	@property
	def has_children(self):
		return not self.is_leaf

	@property
	def name(self):
		return self._name

	@property
	def parent(self):
		return self._parent

	def __lt__(self, other):
		return self._cmpkey() < other._cmpkey()

	def __eq__(self, other):
		return self._cmpkey() == other._cmpkey()

class ParentMenuNode(BaseMenuNode):
	def __init__(self, name = None, parent = None):
		BaseMenuNode.__init__(self, name = name, parent = parent)
		self._children = [ ]
		self._children_by_name = { }

	@property
	def children(self):
		return iter(self._children)

	def add(self, tree, leaf_data):
		key = tree[0]
		tail = tree[1 : ]
		if len(tree) == 1:
			assert(key not in self._children_by_name)
			leaf_node = MenuLeafNode(data = leaf_data, name = key, parent = self)
			self._children_by_name[key] = leaf_node
			self._children.append(leaf_node)
		else:
			if key not in self._children_by_name:
				intermediate_node = ParentMenuNode(name = key, parent = self)
				self._children_by_name[key] = intermediate_node
				self._children.append(intermediate_node)
			else:
				if self._children_by_name[key].is_leaf:
					raise DuplicateEntryException("Node '%s' is already added as leaf node, cannot attach submenu to it." % (key))
			self._children_by_name[key].add(tail, leaf_data)

	def get_entry(self, tree):
		key = tree[0]
		tail = tree[1 : ]
		if not key in self._children_by_name:
			return None
		if len(tree) == 1:
			return self._children_by_name[key]
		else:
			intermediate = self._children_by_name[key]
			if not intermediate.has_children:
				return None
			return intermediate.get_entry(tail)

	def has_entry(self, tree):
		return self.get_entry(tree) is not None

	def dump(self, indent = 0):
		space = ("   " * indent)
		print("%s[%s]" % (space, self.name or "<root>"))
		for child in self.children:
			child.dump(indent + 1)

	def sort(self):
		self._children.sort()
		for child in self:
			child.sort()

	def _cmpkey(self):
		return (0, self._name)

	def __iter__(self):
		return iter(self._children)

class MenuLeafNode(BaseMenuNode):
	def __init__(self, data, name = None, parent = None):
		BaseMenuNode.__init__(self, name = name, parent = parent)
		self._data = data

	@property
	def data(self):
		return self._data

	@property
	def is_leaf(self):
		return True

	def sort(self):
		pass

	def _cmpkey(self):
		return (1, self._name)

	def dump(self, indent = 0):
		space = ("   " * indent)
		print("%s%s{%s}" % (space, self.name, self.data))

class MenuHierarchy(object):
	def __init__(self):
		self._root_node = ParentMenuNode()
		self._entry_by_uid = { }

	@property
	def root(self):
		return self._root_node

	def register(self, entry_uid, tree, value):
		if entry_uid in self._entry_by_uid:
			raise DuplicateEntryException("In menu structure, entry with UUID %s is already present as '%s' - cannot add %s." % (entry_uid, self[entry_uid], value))
		if self._root_node.has_entry(tree):
			raise DuplicateEntryException("In menu structure, an entry is already present at node \"%s\" - cannot add %s." % (" -> ".join(tree), value))
		self._entry_by_uid[entry_uid] = value
		self._root_node.add(tree, value)

	def sort(self):
		self._root_node.sort()

	def dump(self):
		self._root_node.dump()

	def __getitem__(self, entry_uid):
		return self._entry_by_uid[entry_uid]

	def __iter__(self):
		return iter(self._root_node)
