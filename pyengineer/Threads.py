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

#from Units import Units

def pitch_turn_per_inch(x):
	return 0.0254 / x

class Thread():
	def __init__(self, diameter, pitch):
		"""diameter in meters, pitch in meters/turn"""
		self._d = diameter
		self._s = pitch

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

	def getdiameter(self):
		return self._d

	def getpitch(self):
		return self._s

	def __str__(self):
		return "d=%sm s=%sm/turn" % (Units.unify(self._d), Units.unify(self._s))

class ThreadValues():
	_threaddb = {
	}

	def getusage(threadclass, name):
		if ThreadValues._threadusagedb.get(threadclass) is None:
			return tuple()
		if ThreadValues._threadusagedb.get(threadclass).get(name) is None:
			return tuple()
		return ThreadValues._threadusagedb[threadclass][name]

	def get(threadclass, name):
		return ThreadValues._threaddb[threadclass][name]

	def closest(refthread, closestn = 5):
		diffs = [ ]
		for (threadclass, threads) in ThreadValues._threaddb.items():
			for (threadname, thread) in threads.items():
				diff = thread.diff(refthread)
#				print(threadname, thread, diff)
				diffs.append((diff, threadclass, threadname, thread))
		diffs.sort()
		return diffs[:closestn]


if __name__ == "__main__":
	ref = ThreadValues.get("Metric", "M4")
	print("Reference: ", ref)
	for c in  ThreadValues.closest(ref):
		print("Close:", c)

	print("-" * 120)

	ref = Thread(6.66e-3, 6.55e-3 / 5)	# Air pressure 1/4"
	print("Reference: ", ref)
	for c in  ThreadValues.closest(ref):
		print("Close:", c)

	print("-" * 120)

	ref = Thread(13.3e-3, 5.09e-3 / 3)		# Air pressure 1/2"
	print("Reference: ", ref)
	for c in  ThreadValues.closest(ref):
		print("Close:", c)

