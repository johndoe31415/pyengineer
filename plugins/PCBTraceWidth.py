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
	${input_text("i", "Current rating", righthand_side = "A")}
	${input_text("thickness", "Copper thickness", default_value = "1", righthand_side = [ ("oz", "oz/in²"), ("mil", "mil"), ("mm", "mm") ])}
	${input_text("tempdelta", "Temperature delta", righthand_side = [ ("C", "°C"), ("F", "°F") ])}
	${input_text("trace_width", "Trace width", righthand_side = [ ("mil", "mil"), ("mm", "mm") ])}
	${input_checkbox("inner_layer", "Inner layer")}
	${submit_button("Calculate")}
</form>
"""

_response_template = """

<%def name="format_all(variables)">
%if "i" in variables:
I = ${variables["i"]["fmt"]}A<br />
%endif
%if "t" in variables:
t = ${"%.1f" % (variables["t"]["kelvin"])} °C<br />
%endif
%if "width" in variables:
w = ${"%.1f" % (variables["width"]["mil"])} mil<br />
%endif
%if "A" in variables:
A = ${"%.1f" % (variables["A"]["sqrmil"])} mil<sup>2</sup><br />
%endif
</%def>

${result_table_begin("Given", "Calculated")}

%for calculation in d:
<tr>
	<td>
		${format_all(calculation["given"])}
	</td>
	<td>
		${format_all(calculation["calculated"])}
	</td>
</tr>
%endfor

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "9e001362-db63-4859-b427-b6398df6b754"
	_TITLE = "Trace Width Calculation"
	_MENU_HIERARCHY = ("PCB Design", "Trace Width")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		if parameters.get("i", "") != "":
			i = UnitValue(parameters["i"])
		else:
			i = None
		if parameters.get("thickness", "") != "":
			thickness = UnitValue(parameters["thickness"])
			thickness_unit = parameters["thickness_unit"]
			uc = UnitConversion.lengths()
			uc.add(1, "oz", 35, "um")
			thickness_mil = uc.convert(float(thickness), thickness_unit, "mil")
		else:
			thickness_mil = None
		if parameters.get("tempdelta", "") != "":
			tempdelta = UnitValue(parameters["tempdelta"])
			tempdelta_unit = parameters["tempdelta_unit"]
			uc = UnitConversion.temperatures()
			t = uc.convert_delta(float(tempdelta), tempdelta_unit, "K")
		else:
			t = None
		if parameters.get("trace_width", "") != "":
			trace_width = UnitValue(parameters["trace_width"])
			trace_width_unit = parameters["trace_width_unit"]
			uc = UnitConversion.lengths()
			trace_width_mil = uc.convert(float(trace_width), trace_width_unit, "mil")
		else:
			trace_width_mil = None
		inner_layer = (int(parameters.get("inner_layer", "0")) == 1)
		k = 0.024 if inner_layer else 0.048



		# IPC-2221A, pg. 50
		# k = 0.048 for outer, 0.024 for inner layers
		# I = k * T^0.44 * A^0.725
		# A = Cross section in mil²
		# T = Temperature delta in °C
		# A = (I / k / T^0.44)^(1 / 0.725)


		results = [ ]
		if (i is not None) and (t is not None) and (thickness_mil is not None):
			# Calculate trace width
			calc_A_sqrmil = (float(i) / k / (t ** 0.44)) ** (1 / 0.725)
			calc_trace_width_mil = calc_A_sqrmil / thickness_mil
			result = {
				"given": {
					"i":			i.to_dict(),
					"t": {
						"kelvin":	t,
					},
				},
				"calculated": {
					"A": {
						"sqrmil":		calc_A_sqrmil,
					},
					"width": {
						"mil":		calc_trace_width_mil,
					},
				},
			}
			results.append(result)

		if (trace_width_mil is not None) and (t is not None) and (thickness_mil is not None):
			# Calculate current
			calc_A_sqrmil = trace_width_mil * thickness_mil
			calc_i = UnitValue(k * (t ** 0.44) * (calc_A_sqrmil ** 0.725))

			result = {
				"given": {
					"t": {
						"kelvin":	t,
					},
					"A": {
						"sqrmil":		calc_A_sqrmil,
					},
					"width": {
						"mil":		trace_width_mil,
					},
				},
				"calculated": {
					"i":			calc_i.to_dict(),
				},
			}
			results.append(result)



		return results

if __name__ == "__main__":
	from pyengineer import Configuration
	plugin = Plugin(Configuration("configuration.json"), instanciated_from = __file__)

	response = plugin.dump_request({ "i": "5", "thickness": "2", "thickness_unit": "oz", "tempdelta": 20, "tempdelta_unit": "C" })
#	assert(abs(response["width_mil"] - 35.7) < 0.1)

	response = plugin.dump_request({ "i": "15", "thickness": "1.5", "thickness_unit": "oz", "tempdelta": 20, "tempdelta_unit": "C" })
#	assert(abs(response["width_mil"] - 217) < 1)

	response = plugin.dump_request({ "i": "2", "thickness": "1", "thickness_unit": "oz", "tempdelta": 40, "tempdelta_unit": "C" })
