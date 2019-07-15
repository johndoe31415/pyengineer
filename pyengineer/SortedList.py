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

import bisect

class SortedList(object):
	def __init__(self, values):
		self._values = list(sorted(set(values)))

	def less_more(self, search_value):
		if len(self._values) == 0:
			return (None, None)

		index = bisect.bisect(self._values, search_value)

		if index >= len(self._values):
			less_value = self._values[index - 1]
			more_value = None
		elif (index == 0) and (self._values[index] > search_value):
			less_value = None
			more_value = self._values[0]
		else:
			less_value = self._values[index - 1]
			more_value = self._values[index]
		return (less_value, more_value)

	def less_more_list(self, search_value):
		return [ value for value in self.less_more(search_value) if value is not None ]
