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
		"Metric": {
			"M1":				Thread(1e-3, 0.25e-3),
			"M1.2":				Thread(1.2e-3, 0.25e-3),
			"M1.4":				Thread(1.4e-3, 0.3e-3),
			"M1.6":				Thread(1.6e-3, 0.35e-3),
			"M1.7":				Thread(1.7e-3, 0.35e-3),
			"M1.8":				Thread(1.8e-3, 0.35e-3),
			"M2":				Thread(2e-3, 0.4e-3),
			"M2.3":				Thread(2.3e-3, 0.4e-3),
			"M2.5":				Thread(2.5e-3, 0.45e-3),
			"M2.6":				Thread(2.6e-3, 0.45e-3),
			"M3":				Thread(3e-3, 0.5e-3),
			"M3.5":				Thread(3.5e-3, 0.6e-3),
			"M4":				Thread(4e-3, 0.7e-3),
			"M5":				Thread(5e-3, 0.8e-3),
			"M6":				Thread(6e-3, 1e-3),
			"M7":				Thread(7e-3, 1e-3),
			"M8":				Thread(8e-3, 1.25e-3),
			"M9":				Thread(9e-3, 1.25e-3),
			"M10":				Thread(10e-3, 1.5e-3),
			"M11":				Thread(11e-3, 1.5e-3),
			"M12":				Thread(12e-3, 1.75e-3),
			"M14":				Thread(14e-3, 2e-3),
			"M16":				Thread(16e-3, 2e-3),
			"M18":				Thread(18e-3, 2.5e-3),
			"M20":				Thread(20e-3, 2.5e-3),
			"M22":				Thread(22e-3, 2.5e-3),
			"M24":				Thread(24e-3, 3e-3),
			"M27":				Thread(27e-3, 3e-3),
			"M30":				Thread(30e-3, 3.5e-3),
			"M33":				Thread(33e-3, 3.5e-3),
			"M36":				Thread(36e-3, 4e-3),
			"M39":				Thread(39e-3, 4e-3),
			"M42":				Thread(42e-3, 4.5e-3),
			"M45":				Thread(45e-3, 4.5e-3),
			"M48":				Thread(48e-3, 5e-3),
			"M56":				Thread(56e-3, 5.5e-3),
			"M64":				Thread(64e-3, 6e-3),
		},
		"Metric Fine": {
			"M2 x 0.25":		Thread(2e-3, 0.25e-3),
			"M2.5 x 0.35":		Thread(2.5e-3, 0.35e-3),
			"M2.6 x 0.35":		Thread(2.6e-3, 0.35e-3),
			"M3 x 0.35":		Thread(3e-3, 0.35e-3),
			"M3.5 x 0.35":		Thread(3.5e-3, 0.35e-3),
			"M4 x 0.35":		Thread(4e-3, 0.35e-3),
			"M4 x 0.5":			Thread(4e-3, 0.5e-3),
			"M5 x 0.5":			Thread(5e-3, 0.5e-3),
			"M6 x 0.5":			Thread(6e-3, 0.5e-3),
			"M6 x 0.75":		Thread(6e-3, 0.75e-3),
			"M7 x 0.75":		Thread(7e-3, 0.75e-3),
			"M8 x 0.5":			Thread(8e-3, 0.5e-3),
			"M8 x 0.75":		Thread(8e-3, 0.75e-3),
			"M8 x 1.0":			Thread(8e-3, 1e-3),
			"M9 x 1.0":			Thread(9e-3, 1e-3),
			"M10 x 0.75":		Thread(10e-3, 0.75e-3),
			"M10 x 1.0":		Thread(10e-3, 1e-3),
			"M10 x 1.25":		Thread(10e-3, 1.25e-3),
			"M11 x 1.0":		Thread(11e-3, 1e-3),
			"M12 x 1.0":		Thread(12e-3, 1e-3),
			"M12 x 1.25":		Thread(12e-3, 1.25e-3),
			"M12 x 1.5":		Thread(12e-3, 1.5e-3),
			"M14 x 1.25":		Thread(14e-3, 1.25e-3),
			"M14 x 1.5":		Thread(14e-3, 1.5e-3),
			"M16 x 1.0":		Thread(16e-3, 1e-3),
			"M16 x 1.25":		Thread(16e-3, 1.25e-3),
			"M16 x 1.5":		Thread(16e-3, 1.5e-3),
			"M18 x 1.5":		Thread(18e-3, 1.5e-3),
			"M20 x 1.0":		Thread(20e-3, 1e-3),
			"M20 x 1.5":		Thread(20e-3, 1.5e-3),
			"M24 x 1.5":		Thread(24e-3, 1.5e-3),
			"M24 x 2.0":		Thread(24e-3, 2e-3),
			"M30 x 1.5":		Thread(30e-3, 1.5e-3),
			"M30 x 2.0":		Thread(30e-3, 2e-3),
			"M36 x 1.5":		Thread(36e-3, 1.5e-3),
			"M36 x 2.0":		Thread(36e-3, 2e-3),
			"M42 x 1.5":		Thread(42e-3, 1.5e-3),
			"M42 x 2.0":		Thread(42e-3, 2e-3),
		},
		"UNC": {
			"#1-64":			Thread( 73 / 1000 * 25.4e-3, pitch_turn_per_inch(64)),
			"#2-56":			Thread( 86 / 1000 * 25.4e-3, pitch_turn_per_inch(56)),
			"#3-48":			Thread( 99 / 1000 * 25.4e-3, pitch_turn_per_inch(48)),
			"#4-40":			Thread(112 / 1000 * 25.4e-3, pitch_turn_per_inch(40)),
			"#5-40":			Thread(125 / 1000 * 25.4e-3, pitch_turn_per_inch(40)),
			"#6-32":			Thread(138 / 1000 * 25.4e-3, pitch_turn_per_inch(32)),
			"#8-32":			Thread(164 / 1000 * 25.4e-3, pitch_turn_per_inch(32)),
			"#10-24":			Thread(190 / 1000 * 25.4e-3, pitch_turn_per_inch(24)),
			"#12-24":			Thread(216 / 1000 * 25.4e-3, pitch_turn_per_inch(24)),
			"1/4\"-20":			Thread(1 /  4 * 25.4e-3, pitch_turn_per_inch(20)),
			"5/16\"-18":		Thread(5 / 16 * 25.4e-3, pitch_turn_per_inch(18)),
			"3/8\"-16":			Thread(3 /  8 * 25.4e-3, pitch_turn_per_inch(16)),
			"7/16\"-14":		Thread(7 / 16 * 25.4e-3, pitch_turn_per_inch(14)),
			"1/2\"-13":			Thread(1 /  2 * 25.4e-3, pitch_turn_per_inch(13)),
			"9/16\"-12":		Thread(9 / 16 * 25.4e-3, pitch_turn_per_inch(12)),
			"5/8\"-11":			Thread(5 /  8 * 25.4e-3, pitch_turn_per_inch(11)),
			"3/4\"-10":			Thread(3 /  4 * 25.4e-3, pitch_turn_per_inch(10)),
			"7/8\"-9":			Thread(7 /  8 * 25.4e-3, pitch_turn_per_inch(9)),
			"1\"-8":			Thread(1 /  1 * 25.4e-3, pitch_turn_per_inch(8)),
			"1 1/8\"-7":		Thread(1 + 1 /  8 * 25.4e-3, pitch_turn_per_inch(7)),
			"1 1/4\"-7":		Thread(1 + 1 /  4 * 25.4e-3, pitch_turn_per_inch(7)),
			"1 3/8\"-6":		Thread(1 + 3 /  8 * 25.4e-3, pitch_turn_per_inch(6)),
			"1 1/2\"-6":		Thread(1 + 1 /  2 * 25.4e-3, pitch_turn_per_inch(6)),
			"1 3/4\"-5":		Thread(1 + 3 /  4 * 25.4e-3, pitch_turn_per_inch(5)),
			"2\"-4.5":			Thread(2 * 25.4e-3, pitch_turn_per_inch(4.5)),
		},
		"UNF": {
			"#0-80":			Thread( 60 / 1000 * 25.4e-3, pitch_turn_per_inch(80)),
			"#1-72":			Thread( 73 / 1000 * 25.4e-3, pitch_turn_per_inch(72)),
			"#2-64":			Thread( 86 / 1000 * 25.4e-3, pitch_turn_per_inch(64)),
			"#3-56":			Thread( 99 / 1000 * 25.4e-3, pitch_turn_per_inch(56)),
			"#4-48":			Thread(112 / 1000 * 25.4e-3, pitch_turn_per_inch(48)),
			"#5-44":			Thread(125 / 1000 * 25.4e-3, pitch_turn_per_inch(44)),
			"#6-40":			Thread(138 / 1000 * 25.4e-3, pitch_turn_per_inch(40)),
			"#8-36":			Thread(164 / 1000 * 25.4e-3, pitch_turn_per_inch(36)),
			"#10-32":			Thread(190 / 1000 * 25.4e-3, pitch_turn_per_inch(32)),
			"#12-28":			Thread(216 / 1000 * 25.4e-3, pitch_turn_per_inch(28)),
			"1/4\"-28":			Thread(1 /  4 * 25.4e-3, pitch_turn_per_inch(28)),
			"5/16\"-24":		Thread(5 / 16 * 25.4e-3, pitch_turn_per_inch(24)),
			"3/8\"-24":			Thread(3 /  8 * 25.4e-3, pitch_turn_per_inch(24)),
			"7/16\"-20":		Thread(7 / 16 * 25.4e-3, pitch_turn_per_inch(20)),
			"1/2\"-20":			Thread(1 /  2 * 25.4e-3, pitch_turn_per_inch(20)),
			"9/16\"-18":		Thread(9 / 16 * 25.4e-3, pitch_turn_per_inch(18)),
			"5/8\"-18":			Thread(5 /  8 * 25.4e-3, pitch_turn_per_inch(18)),
			"3/4\"-16":			Thread(3 /  4 * 25.4e-3, pitch_turn_per_inch(16)),
			"7/8\"-14":			Thread(7 /  8 * 25.4e-3, pitch_turn_per_inch(14)),
			"1\"-12":			Thread(1 /  1 * 25.4e-3, pitch_turn_per_inch(12)),
			"1 1/8\"-12":		Thread(1 + 1 /  8 * 25.4e-3, pitch_turn_per_inch(12)),
			"1 1/4\"-12":		Thread(1 + 1 /  4 * 25.4e-3, pitch_turn_per_inch(12)),
			"1 3/8\"-12":		Thread(1 + 3 /  8 * 25.4e-3, pitch_turn_per_inch(12)),
			"1 1/2\"-12":		Thread(1 + 1 /  2 * 25.4e-3, pitch_turn_per_inch(12)),
		},
		"BSP/DIN ISO 228": {
			"G 1/8\"":			Thread(  9.73e-3, pitch_turn_per_inch(28)),
			"G 1/4\"":			Thread( 13.16e-3, pitch_turn_per_inch(19)),
			"G 3/8\"":			Thread( 16.66e-3, pitch_turn_per_inch(19)),
			"G 1/2\"":			Thread( 20.95e-3, pitch_turn_per_inch(14)),
			"G 5/8\"":			Thread( 22.91e-3, pitch_turn_per_inch(14)),
			"G 3/4\"":			Thread( 26.44e-3, pitch_turn_per_inch(14)),
			"G 7/8\"":			Thread( 30.20e-3, pitch_turn_per_inch(14)),
			"G 1\"":			Thread( 33.25e-3, pitch_turn_per_inch(11)),
			"G 1 1/8\"":		Thread( 37.90e-3, pitch_turn_per_inch(11)),
			"G 1 1/4\"":		Thread( 41.91e-3, pitch_turn_per_inch(11)),
			"G 1 3/8\"":		Thread( 44.32e-3, pitch_turn_per_inch(11)),
			"G 1 1/2\"":		Thread( 47.80e-3, pitch_turn_per_inch(11)),
			"G 1 3/4\"":		Thread( 53.74e-3, pitch_turn_per_inch(11)),
			"G 2\"":			Thread( 59.61e-3, pitch_turn_per_inch(11)),
			"G 2 1/4\"":		Thread( 65.71e-3, pitch_turn_per_inch(11)),
			"G 2 1/2\"":		Thread( 75.18e-3, pitch_turn_per_inch(11)),
			"G 2 3/4\"":		Thread( 81.53e-3, pitch_turn_per_inch(11)),
			"G 3\"":			Thread( 87.88e-3, pitch_turn_per_inch(11)),
			"G 3 1/4\"":		Thread( 93.98e-3, pitch_turn_per_inch(11)),
			"G 3 1/2\"":		Thread(100.33e-3, pitch_turn_per_inch(11)),
			"G 3 3/4\"":		Thread(106.68e-3, pitch_turn_per_inch(11)),
			"G 4\"":			Thread(113.03e-3, pitch_turn_per_inch(11)),
		},
		"BSW": {
			"W 1/16\"":			Thread(1 / 16 * 25.4e-3, pitch_turn_per_inch(60)),
			"W 3/32\"":			Thread(3 / 32 * 25.4e-3, pitch_turn_per_inch(48)),
			"W 1/8\"":			Thread(1 /  8 * 25.4e-3, pitch_turn_per_inch(40)),
			"W 5/32\"":			Thread(5 / 32 * 25.4e-3, pitch_turn_per_inch(32)),
			"W 3/16\"":			Thread(3 / 16 * 25.4e-3, pitch_turn_per_inch(24)),
			"W 7/32\"":			Thread(7 / 32 * 25.4e-3, pitch_turn_per_inch(24)),
			"W 1/4\"":			Thread(1 /  4 * 25.4e-3, pitch_turn_per_inch(20)),
			"W 5/16\"":			Thread(5 / 16 * 25.4e-3, pitch_turn_per_inch(18)),
			"W 3/8\"":			Thread(3 /  8 * 25.4e-3, pitch_turn_per_inch(16)),
			"W 7/16\"":			Thread(7 / 16 * 25.4e-3, pitch_turn_per_inch(14)),
			"W 1/2\"":			Thread(1 /  2 * 25.4e-3, pitch_turn_per_inch(12)),
			"W 9/16\"":			Thread(9 / 16 * 25.4e-3, pitch_turn_per_inch(12)),
			"W 5/8\"":			Thread(5 /  8 * 25.4e-3, pitch_turn_per_inch(11)),
			"W 3/4\"":			Thread(3 /  4 * 25.4e-3, pitch_turn_per_inch(10)),
			"W 7/8\"":			Thread(7 /  8 * 25.4e-3, pitch_turn_per_inch(9)),
			"W 1\"":			Thread(1 * 25.4e-3, pitch_turn_per_inch(8)),
		},
		"BSF": {
			"BSF 3/16\"":			Thread( 3 / 16 * 25.4e-3, pitch_turn_per_inch(32)),
			"BSF 7/32\"":			Thread( 7 / 32 * 25.4e-3, pitch_turn_per_inch(28)),
			"BSF 1/4\"":			Thread( 1 /  4 * 25.4e-3, pitch_turn_per_inch(26)),
			"BSF 9/32\"":			Thread( 9 / 32 * 25.4e-3, pitch_turn_per_inch(26)),
			"BSF 5/16\"":			Thread( 5 / 16 * 25.4e-3, pitch_turn_per_inch(22)),
			"BSF 3/8\"":			Thread( 3 /  8 * 25.4e-3, pitch_turn_per_inch(20)),
			"BSF 7/16\"":			Thread( 7 / 16 * 25.4e-3, pitch_turn_per_inch(18)),
			"BSF 1/2\"":			Thread( 1 /  2 * 25.4e-3, pitch_turn_per_inch(16)),
			"BSF 9/16\"":			Thread( 9 / 16 * 25.4e-3, pitch_turn_per_inch(16)),
			"BSF 5/8\"":			Thread( 5 /  8 * 25.4e-3, pitch_turn_per_inch(14)),
			"BSF 11/16\"":			Thread(11 / 16 * 25.4e-3, pitch_turn_per_inch(14)),
			"BSF 3/4\"":			Thread( 3 /  4 * 25.4e-3, pitch_turn_per_inch(12)),
			"BSF 13/16\"":			Thread(13 / 16 * 25.4e-3, pitch_turn_per_inch(12)),
			"BSF 7/8\"":			Thread( 7 /  8 * 25.4e-3, pitch_turn_per_inch(11)),
			"BSF 15/16\"":			Thread(15 / 16 * 25.4e-3, pitch_turn_per_inch(11)),
			"BSF 1\"":				Thread(1 * 25.4e-3, pitch_turn_per_inch(10)),
			"BSF 1 1/8\"":			Thread((1 + (1 / 8)) * 25.4e-3, pitch_turn_per_inch(9)),
			"BSF 1 1/4\"":			Thread((1 + (1 / 4)) * 25.4e-3, pitch_turn_per_inch(9)),
			"BSF 1 3/8\"":			Thread((1 + (3 / 8)) * 25.4e-3, pitch_turn_per_inch(8)),
			"BSF 1 1/2\"":			Thread((1 + (1 / 2)) * 25.4e-3, pitch_turn_per_inch(8)),
			"BSF 1 5/8\"":			Thread((1 + (5 / 8)) * 25.4e-3, pitch_turn_per_inch(8)),
			"BSF 1 3/4\"":			Thread((1 + (3 / 4)) * 25.4e-3, pitch_turn_per_inch(7)),
			"BSF 2\"":				Thread(2 * 25.4e-3, pitch_turn_per_inch(7)),
			"BSF 2 1/4\"":			Thread((2 + (1 / 4)) * 25.4e-3, pitch_turn_per_inch(6)),
			"BSF 2 1/2\"":			Thread((2 + (1 / 2)) * 25.4e-3, pitch_turn_per_inch(6)),
		},
		"Optics": {
			"Leica L-Mount":		Thread(39e-3, pitch_turn_per_inch(26)),
			"T2":					Thread(42e-3, 0.75e-3),
			"C-Mount":				Thread(25.4e-3, pitch_turn_per_inch(32)),
		},

	}

	_threadusagedb = {
		"BSP/DIN ISO 228": {
			"G 5/8\"":			("200 bar compressed air",),
			"G 1/4\"":			("10 bar compressed air 1/4\"",),
			"G 3/8\"":			("10 bar compressed air 3/8\"",),
			"G 1/2\"":			("10 bar compressed air 1/2\"",),
		},
		"Metric Fine": {
			"M10 x 1.0":		("Spark Plug",),
			"M12 x 1.25":		("Spark Plug",),
			"M14 x 1.25":		("Spark Plug",),
			"M18 x 1.5":		("Spark Plug",),
		},
		"Metric": {
			"M3":				("PC screw fine thread",),
		},
		"UNC": {
			"#6-32":			("PC screw coarse thread",),
		},
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

