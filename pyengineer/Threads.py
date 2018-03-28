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

class Thread(object):
	def __init__(self, diameter, pitch, group = None, name = None, usage = None):
		"""Diameter is given in meters, pitch given in meters/turn."""
		self._diameter = diameter
		self._pitch = pitch
		self._group = group
		self._name = name
		self._usage = usage

	@property
	def diameter(self):
		return self._diameter

	@property
	def pitch(self):
		return self._pitch

	@property
	def pitch_tpi(self):
		return 0.0254 / self.pitch

	@property
	def group(self):
		return self._group

	@property
	def name(self):
		return self._name

	@property
	def usage(self):
		return self._usage

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
		ddiff = Thread._diffval(self.diameter, other.diameter)
		if ddiff < 0:
			ddiff = 2 * abs(ddiff)
		else:
			ddiff = abs(ddiff)
		pdiff = abs(Thread._diffval(self.pitch, other.pitch) * 2)
		sumdiff = ddiff + pdiff
#		print("%-30s %-30s %.4f %.4f %.4f" % (str(self), str(other), ddiff, pdiff, sumdiff))
		return sumdiff

	def __str__(self):
		return "%s / %s (d=%.1fmm p=%.0f µm/turn=%.1f TPI)" % (self.group, self.name, self.diameter * 1000, self.pitch * 1e6, self.pitch_tpi)

class ThreadDB(object):
	_DIAMETER_ELEMENTS = set(("diameter", "diameter_thou", "diameter_inch"))
	_PITCH_ELEMENTS = set(("pitch", "tpi"))

	def __init__(self):
		self._threads_by_group = collections.defaultdict(list)

	def add_thread(self, thread):
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


		if "diameter" in thread_data:
			diameter = thread_data["diameter"]
		elif "diameter_thou" in thread_data:
			diameter = thread_data["diameter_thou"] * 25.4 / 1000 / 1000
		elif "diameter_inch" in thread_data:
			if len(thread_data["diameter_inch"]) not in [ 2, 3 ]:
				raise InvalidThreadDefinitionException("Expected two or three array members for diameter_inch definition, but got %d: %s" % (len(thread_data["diameter_inch"]), str(thread_data)))
			if len(thread_data["diameter_inch"]) == 2:
				diameter = (thread_data["diameter_inch"][0] / thread_data["diameter_inch"][1]) * 25.4 / 1000
			else:
				diameter = (thread_data["diameter_inch"][0] + (thread_data["diameter_inch"][1] / thread_data["diameter_inch"][2])) * 25.4 / 1000

		if "pitch" in thread_data:
			pitch = thread_data["pitch"]
		elif "tpi" in thread_data:
			pitch = 0.0254 / thread_data["tpi"]

		thread = Thread(diameter = diameter, pitch = pitch, group = group_name, name = thread_data["name"], usage = thread_data.get("usage"))
		self.add_thread(thread)

	def add_groups_by_definition(self, thread_groups):
		for (group_name, threads_data) in thread_groups.items():
			for thread_data in threads_data:
				self.add_by_definition(group_name, thread_data)

	def closest(self, reference, closest_n = 5):
		candidates = [ ]
		for thread in self:
			error = thread.diff(reference)
			candidates.append((error, thread))
		candidates.sort(key = lambda x: x[0])
		for ((error, candidate), _) in zip(candidates, range(closest_n)):
			yield candidate

	def __iter__(self):
		for (group_name, threads_data) in self._threads_by_group.items():
			yield from threads_data
