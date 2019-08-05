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
from pyengineer import BasePlugin, UnitValue, UnitConversion, InputDataException
from pyengineer.NewtonSolver import DiffedFunction, NewtonSolver

_form_template = """
<form id="input_data">
	${input_text("thickness", "Copper thickness", righthand_side = [ ("foo", "fofdjsioo") ])}
	${submit_button("Calculate")}
</form>
"""

_response_template = """
${result_table_begin("Parameter", "Value")}

<tr>
	<td>Trace width:</td>
	<td>${"%.1f" % (d["width_mil"])} mil</td>
</tr>

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "9e001362-db63-4859-b427-b6398df6b754"
	_TITLE = "Trace Width Calculation"
	_MENU_HIERARCHY = ("PCB Design", "Trace Width")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		i = UnitValue(parameters["i"])
		thickness = UnitValue(parameters["thickness"])
		thickness_unit = parameters["thickness_unit"]
		tempdelta = UnitValue(parameters["tempdelta"])
		tempdelta_unit = parameters["tempdelta_unit"]
		inner_layer = (int(parameters.get("inner_layer", "0")) == 1)

		uc = UnitConversion.lengths()
		uc.add(1, "oz", 35, "um")
		thickness_mil = uc.convert(float(thickness), thickness_unit, "mil")

		uc = UnitConversion.temperatures()
		t = uc.convert(float(tempdelta), tempdelta_unit, "C")

		# IPC-2221A, pg. 50
		# k = 0.048 for outer, 0.024 for inner layers
		# I = k * T^0.44 * A^0.725
		# A = Cross section in mil²
		# T = Temperature delta in °C
		# A = (I / k / T^0.44)^(1 / 0.725)

		k = 0.024 if inner_layer else 0.048
		A_sqrmil = (float(i) / k / (t ** 0.44)) ** (1 / 0.725)
		width_mil = A_sqrmil / thickness_mil

		return {
			"A_sqrmil":		A_sqrmil,
			"width_mil":	width_mil,
		}

if __name__ == "__main__":
	from pyengineer import Configuration
	plugin = Plugin(Configuration("configuration.json"), instanciated_from = __file__)

	response = plugin.dump_request({ "i": "5", "thickness": "2", "thickness_unit": "oz", "tempdelta": 20, "tempdelta_unit": "C" })
	assert(abs(response["width_mil"] - 35.7) < 0.1)

	response = plugin.dump_request({ "i": "15", "thickness": "1.5", "thickness_unit": "oz", "tempdelta": 20, "tempdelta_unit": "C" })
	assert(abs(response["width_mil"] - 217) < 1)

	response = plugin.dump_request({ "i": "2", "thickness": "1", "thickness_unit": "oz", "tempdelta": 40, "tempdelta_unit": "C" })
