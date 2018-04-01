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

class DiffedFunction(object):
	"""Function and it's differential."""
	def f(self, x):
		"""Needs to be implemented by child class."""
		raise Exception(NotImplemented)

	def fdiff(self, x):
		# If this isn't overriden in child class, we use trivial numeric
		# estimation
		return self.numeric_fdiff(x, epsilon = 1e-9)

	def numeric_fdiff(self, x, epsilon):
		y0 = self.f(x)
		y1 = self.f(x + epsilon)
		return (y1 - y0) / epsilon

	def test_correctness(self, x, epsilon = 1e-9, max_error = 1e-6):
		ydiff = self.fdiff(x)
		ydiff_numeric = self.numeric_fdiff(x, epsilon = epsilon)
		return abs(ydiff - ydiff_numeric) < max_error

class NewtonSolver(object):
	"""Find root of given equation using Newton's method."""
	def __init__(self, diffed_function):
		self._diffed_function = diffed_function

	def solve(self, x0 = 0, max_residual = 1e-7, max_iterations = 10):
		x = x0
		for i in range(max_iterations):
			fval = self._diffed_function.f(x)
			fdiffval = self._diffed_function.fdiff(x)
			x_new = x - fval / fdiffval
			residual = abs(x - x_new)
			x = x_new
			if residual < max_residual:
				break
		return x
