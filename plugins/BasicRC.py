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

${result_table_end()}
"""

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

		if v2 > v1:
			# Capacitor is charging
			raise InputDataException("Solving charging capacitors is not supported.")

		# Capacitor is discharging
		# V = V0 * exp(-t / tau)
		# i.e., v1 = V0 * exp(-t1 / tau)     and     v1 = V0 * exp(-t1 / tau)
		# V0 = v1 / exp(-t1 / tau)
		tau = (float(t1) - float(t2)) / math.log(float(v2) / float(v1))
		v0 = float(v1) / math.exp(-float(t1) / tau)
		f = 1 / (2 * math.pi * tau)

		return {
			"tau":	tau,
			"v0":	UnitValue(v0).to_dict(),
			"f":	UnitValue(f).to_dict(),
		}


if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config).request("calc", { "t1": "0.5", "v1": 10, "t2": "3", "v2": "8" }))
	print(Plugin(config).request("calc", { "t1": "0.5", "v1": 8,  "t2": "3", "v2": "10" }))

