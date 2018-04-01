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
from pyengineer.NewtonSolver import DiffedFunction, NewtonSolver

class _Parabola(DiffedFunction):
	def __init__(self, a, b, c):
		self._a = a
		self._b = b
		self._c = c

	def f(self, x):
		(a, b, c) = (self._a, self._b, self._c)
		return a * (x ** 2) + b * x + c

class NewtonSolverTests(unittest.TestCase):
	def test_basic(self):
		parabola = _Parabola(a = 1, b = -1, c = -6)
		solver = NewtonSolver(parabola)
		x0 = solver.solve(x0 = -5)
		self.assertAlmostEqual(x0, -2)
		self.assertAlmostEqual(parabola.f(x0), 0)

		x1 = solver.solve(x0 = 1.234567)
		self.assertAlmostEqual(x1, 3)
		self.assertAlmostEqual(parabola.f(x1), 0)
