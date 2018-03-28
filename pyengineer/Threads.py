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

import collections

from pyengineer.Exceptions import InvalidThreadDefinitionException

def pitch_turn_per_inch(x):
	return 0.0254 / x

class Thread(object):
	def __init__(self, diameter, pitch, usage = None, group = None):
		"""Diameter is given in meters, pitch given in meters/turn."""
		self._diameter = diameter
		self._pitch = pitch

	@property
	def diameter(self):
		return self._diameter

	@property
	def pitch(self):
		return self._pitch

	@property
	def usage(self):
		return self._usage

	@property
	def group(self):
		return self._group

	def _diffval(x, y):
		diff = abs(x / y)
		if diff < 1:
			diff = 1 / diff
			factor = -1
		else:
			factor = 1
		diff = factor * ((diff * 100) - 100)
		return diff

	def diff(self, other):
		ddiff = Thread._diffval(self._d, other._d)
		if ddiff < 0:
			ddiff = 2 * abs(ddiff)
		else:
			ddiff = abs(ddiff)
		pdiff = abs(Thread._diffval(self._s, other._s) * 2)
		sumdiff = ddiff + pdiff
#		print("%-30s %-30s %.4f %.4f %.4f" % (str(self), str(other), ddiff, pdiff, sumdiff))
		return sumdiff

	def __str__(self):
		return "d=%.1f p=%.1f" % (self.diameter, self.pitch)

class ThreadDB(object):
	_DIAMETER_ELEMENTS = set(("diameter", "diameter_thou", "diameter_inch"))
	_PITCH_ELEMENTS = set(("pitch", "tpi"))

	def __init__(self):
		self._threads_by_group = collections.defaultdict(list)

	def add(self, thread):
		group = thread.group or "Misc"
		self._threads_by_group[group].append(thread)

	def add_by_definition(self, group_name, thread_data):
		if "name" not in thread_data:
			raise InvalidThreadDefinitionException("No 'name' element present in thread definition: %s" % (str(thread_data)))

		diameter_elements = self._DIAMETER_ELEMENTS & thread_data.keys()
		if len(diameter_elements) != 1:
			raise InvalidThreadDefinitionException("Expected exactly one diameter element in thread definition, but got %d (%s): %s" % (len(diameter_elements), ", ".join(sorted(diameter_elements)), str(thread_data)))

		pitch_elements = self._PITCH_ELEMENTS & thread_data.keys()
		if len(pitch_elements) != 1:
			raise InvalidThreadDefinitionException("Expected exactly one pitch element in thread definition, but got %d (%s): %s" % (len(pitch_elements), ", ".join(sorted(pitch_elements)), str(thread_data)))
#		print(diameter_elements)
#		print(thread_data)

	def add_groups_by_definition(self, thread_groups):
		for (group_name, threads_data) in thread_groups.items():
			for thread_data in threads_data:
				self.add_by_definition(group_name, thread_data)

	def closest(refthread, closestn = 5):
		diffs = [ ]
		for (threadclass, threads) in ThreadValues._threaddb.items():
			for (threadname, thread) in threads.items():
				diff = thread.diff(refthread)
#				print(threadname, thread, diff)
				diffs.append((diff, threadclass, threadname, thread))
		diffs.sort()
		return diffs[:closestn]


