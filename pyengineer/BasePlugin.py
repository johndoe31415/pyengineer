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

class BasePlugin(object):
	_ID = None
	_TITLE = None
	_MENU_HIERARCHY = None

	def __init__(self, configuration):
		assert(isinstance(self._ID, str))
		assert(isinstance(self._TITLE, str))
		assert(isinstance(self._MENU_HIERARCHY, tuple))
		self._config = configuration

	@property
	def plugin_id(self):
		return self._ID

	@property
	def plugin_title(self):
		return self._TITLE

	@property
	def plugin_menu_hierarchy(self):
		return self._MENU_HIERARCHY

	@property
	def config(self):
		return self._config
