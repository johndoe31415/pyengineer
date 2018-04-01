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

import math
from pyengineer import BasePlugin, UnitValue, InputDataException
from pyengineer.NewtonSolver import DiffedFunction, NewtonSolver

_form_template = """
<form id="input_data">
	${input_text("t1", "Timestamp 1", righthand_side = "sec")}
	${input_text("v1", "Voltage 1", righthand_side = "V")}
	${input_text("t2", "Timestamp 2", righthand_side = "sec")}
	${input_text("v2", "Voltage 2", righthand_side = "V")}
	${submit_button("Calculate")}
</form>
"""

_response_template = """
${result_table_begin("Parameter", "Symbol", "Value")}

<tr>
	<td>Time constant:</td>
	<td>τ = </td>
	<td>${"%.2f" % (d["tau"])} sec</td>
</tr>

<tr>
	<td>Initial voltage:</td>
	<td>V<sub>0</sub> = </td>
	<td>${d["v0"]["fmt"]}V</td>
</tr>

<tr>
	<td>Cutoff frequency:</td>
	<td>f = </td>
	<td>${d["f"]["fmt"]}Hz</td>
</tr>

<tr>
	<td>Absolute error:</td>
	<td>f = </td>
	<td>${d["abs_error"]["fmt"]}V</td>
</tr>

${result_table_end()}
"""

class _ChargingCapFunction(DiffedFunction):
	"""f(tau) = d - (1 - math.exp(-t1 / tau)) / (1 - math.exp(-t2 / tau))"""

	def __init__(self, d, t1, t2):
		self._d = d
		self._t1 = t1
		self._t2 = t2

	def f(self, tau):
		(d, t1, t2) = (self._d, self._t1, self._t2)
		return d - (1 - math.exp(-t1 / tau)) / (1 - math.exp(-t2 / tau))

	def fdiff(self, tau):
		(d, t1, t2) = (self._d, self._t1, self._t2)
		return t2 * (math.exp(-t1 / tau) - 1) * math.exp(-t2 / tau) / ((tau ** 2) * (math.exp(-t2 / tau) - 1) ** 2) \
					- t1 * math.exp(-t1 / tau) / ((tau ** 2) * (math.exp(-t2 / tau) - 1))

class Plugin(BasePlugin):
	_ID = "1fc081a2-b445-4880-b4a0-db8bfe8e0205"
	_TITLE = "RC Circuit"
	_MENU_HIERARCHY = ("Basics", "RC Circuit")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		t1 = UnitValue(parameters["t1"])
		v1 = UnitValue(parameters["v1"])
		t2 = UnitValue(parameters["t2"])
		v2 = UnitValue(parameters["v2"])
		if t1 > t2:
			(t1, v1, t2, v2) = (t2, v2, t1, v1)

		if v2 < v1:
			# Capacitor is discharging
			# v(t) = v0 * exp(-t / tau)
			# v1 = v0 * exp(-t1 / tau)  ->  v0 = v1 / exp(-t1 / tau)
			# v2 = v0 * exp(-t2 / tau)  ->  v0 = v2 / exp(-t2 / tau)
			# v1 / exp(-t1 / tau) = v2 / exp(-t2 / tau)
			# v1 / v2 = exp(-t1 / tau) / exp(-t2 / tau) = exp((-t1 - (-t2)) / tau) = exp((t2 - t1) / tau)
			# (t2 - t1) / tau = ln(v1 / v2)
			# tau = (t2 - t1) / ln(v1 / v2)
			tau = (float(t2) - float(t1)) / math.log(float(v1) / float(v2))
		else:
			# Capacitor is charging, here we need to rely on numeric solution.
			# v(t) = v0 * (1 - exp(-t / tau))
			# v1 = v0 * exp(-t1 / tau)
			# v2 = v0 * exp(-t2 / tau)
			# v1 / v2 = exp(-t1 / tau) / exp(-t2 / tau)
			# Substitute: d = v1 / v2
			# d = exp(-t1 / tau) / exp(-t2 / tau)
			# d - exp(-t1 / tau) / exp(-t2 / tau) = 0
			# Solve this by Newton's method.
			d = float(v1) / float(v2)
			function = _ChargingCapFunction(d = float(v1) / float(v2), t1 = float(t1), t2 = float(t2))
			try:
				tau = NewtonSolver(function).solve(x0 = 1)
			except ZeroDivisionError:
				raise InputDataException("Result is numerically instable, cannot solve.")

		# In either case:
		# v0 = v1 / exp(-t1 / tau)
		v0 = float(v1) / math.exp(-float(t1) / tau)

		if tau < 0:
			raise InputDataException("Result is numerically instable, tau was negative.")

		# Now, plausibilize values.
		if v2 < v1:
			calc_v1 = v0 * math.exp(-float(t1) / tau)
			calc_v2 = v0 * math.exp(-float(t2) / tau)
		else:
			calc_v1 = v0 * (1 - math.exp(-float(t1) / tau))
			calc_v2 = v0 * (1 - math.exp(-float(t2) / tau))

		error_v1 = abs(calc_v1 - float(v1))
		error_v2 = abs(calc_v2 - float(v2))
		max_error = max(error_v1, error_v2)
		if (max_error > 10):
			raise InputDataException("Result is numerically instable and diverged. Refusing to give a completely wrong answer. Absolute error was %.2e" % (max_error))

		# Cutoff frequency
		f = 1 / (2 * math.pi * tau)

		return {
			"tau":			tau,
			"v0":			UnitValue(v0).to_dict(),
			"f":			UnitValue(f).to_dict(),
			"abs_error":	UnitValue(max_error).to_dict(),
		}


if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config).request("calc", { "t1": "0.5", "v1": 10, "t2": "3", "v2": "8" }))
	print(Plugin(config).request("calc", { "t1": "0.5", "v1": 8,  "t2": "3", "v2": "10" }))

