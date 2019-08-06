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
	${input_text("thickness", "Copper thickness", default_value = "1", righthand_side = [ ("oz", "oz/ft²"), ("mil", "mil"), ("mm", "mm") ])}
	${input_text("tempdelta", "Temperature delta", righthand_side = [ ("C", "°C"), ("F", "°F") ])}
	${input_text("trace_width", "Trace width", righthand_side = [ ("mil", "mil"), ("mm", "mm") ])}
	${input_checkbox("inner_layer", "Inner layer")}
	${input_text("trace_length", "Trace length", righthand_side = "m")}
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
A = ${"%.1f" % (variables["A"]["sqrmil"])} mil<sup>2</sup> ≙  ${"%.4f" % (variables["A"]["mm2"])} mm<sup>2</sup><br />
%endif
%if "thickness" in variables:
h = ${"%.1f" % (variables["thickness"]["mil"])} mil ≙ ${"%.0f" % (1000 * variables["thickness"]["mm"])}µm ≙ ${"%.1f" % (variables["thickness"]["oz"])} oz/ft<sup>2</sup><br />
%endif
%if "R_per_cm" in variables:
R<sub>dyn</sub> = ${variables["R_per_cm"]["fmt"]}Ω/cm<br />
%endif
%if "l" in variables:
l = ${variables["l"]["fmt"]}m<br />
%endif
%if "R" in variables:
R = ${variables["R"]["fmt"]}Ω<br />
%endif
%if "P" in variables:
P = ${variables["P"]["fmt"]}W<br />
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
		if parameters.get("trace_length", "") != "":
			trace_length = UnitValue(parameters["trace_length"])
		else:
			trace_length = None
		k = 0.024 if inner_layer else 0.048



		# IPC-2221A, pg. 50
		# k = 0.048 for outer, 0.024 for inner layers
		# I = k * T^0.44 * A^0.725
		# A = Cross section in mil²
		# T = Temperature delta in °C
		# A = (I / k / T^0.44)^(1 / 0.725)
		# T = (I / k / A^0.725)^ (1 / 0.44)

		def unit_temperature(tempdelta_kelvin):
			return {
				"kelvin":	tempdelta_kelvin,
			}

		def unit_length_mil(length_mil):
			return {
				"mil":		length_mil,
			}

		def unit_area_sqrmil(area_sqrmil):
			return {
				"sqrmil":	area_sqrmil,
				"mm2":		area_sqrmil / ((1000 / 25.4) ** 2),
			}

		def unit_copper_thickness(length_mil):
			uc = UnitConversion.lengths()
			uc.add(1, "oz", 35, "um")
			return {
				"mil":		length_mil,
				"oz":		uc.convert(length_mil, "mil", "oz"),
				"mm":		uc.convert(length_mil, "mil", "mm"),
			}


		results = [ ]
		if (i is not None) and (t is not None) and (thickness_mil is not None):
			# Calculate trace width
			calc_A_sqrmil = (float(i) / k / (t ** 0.44)) ** (1 / 0.725)
			calc_trace_width_mil = calc_A_sqrmil / thickness_mil
			result = {
				"given": {
					"i":			i.to_dict(),
					"t":			unit_temperature(t),
					"thickness":	unit_copper_thickness(thickness_mil),
				},
				"calculated": {
					"A":			unit_area_sqrmil(calc_A_sqrmil),
					"width":		unit_length_mil(calc_trace_width_mil),
				},
			}
			results.append(result)

		if (trace_width_mil is not None) and (t is not None) and (thickness_mil is not None):
			# Calculate current
			calc_A_sqrmil = trace_width_mil * thickness_mil
			calc_i = UnitValue(k * (t ** 0.44) * (calc_A_sqrmil ** 0.725))

			result = {
				"given": {
					"width":		unit_length_mil(calc_trace_width_mil),
					"t":			unit_temperature(t),
					"thickness":	unit_copper_thickness(thickness_mil),
				},
				"calculated": {
					"A":			unit_area_sqrmil(calc_A_sqrmil),
					"i":			calc_i.to_dict(),
				},
			}
			results.append(result)

		if (trace_width_mil is not None) and (t is not None) and (i is not None):
			# Calculate copper thickness
			calc_A_sqrmil = (float(i) / k / (t ** 0.44)) ** (1 / 0.725)
			calc_copper_height_mil = calc_A_sqrmil / trace_width_mil

			result = {
				"given": {
					"i":			i.to_dict(),
					"t":			unit_temperature(t),
					"width":		unit_length_mil(trace_width_mil),
				},
				"calculated": {
					"A":			unit_area_sqrmil(calc_A_sqrmil),
					"thickness":	unit_copper_thickness(calc_copper_height_mil),
				},
			}
			results.append(result)

		if (trace_width_mil is not None) and (i is not None) and (thickness_mil is not None):
			# Calculate temperature rise
			calc_A_sqrmil = trace_width_mil * thickness_mil
			calc_t = (float(i) / k / (calc_A_sqrmil ** 0.725)) ** (1 / 0.44)

			result = {
				"given": {
					"i":			i.to_dict(),
					"width":		unit_length_mil(trace_width_mil),
					"thickness":	unit_copper_thickness(thickness_mil),
				},
				"calculated": {
					"A":			unit_area_sqrmil(calc_A_sqrmil),
					"t":			unit_temperature(calc_t),
				},
			}
			results.append(result)

		for result in results:
			cu_resistivity = 1.68e-8	# Ohm-meters
			area_sqrm = result["calculated"]["A"]["mm2"] / 1e6
			resistance_per_meter = cu_resistivity / area_sqrm
			result["calculated"]["R_per_cm"] = UnitValue(resistance_per_meter / 100).to_dict()
			if trace_length is not None:
				result["given"]["l"] = trace_length.to_dict()
				result["calculated"]["R"] = UnitValue(resistance_per_meter * float(trace_length)).to_dict()
				if ("i" in result["given"]):
					i = result["given"]["i"]["flt"]
				else:
					i = result["calculated"]["i"]["flt"]
				P = (i ** 2) * result["calculated"]["R"]["flt"]
				result["calculated"]["P"] = UnitValue(P).to_dict()

		return results

if __name__ == "__main__":
	from pyengineer import Configuration
	plugin = Plugin(Configuration("configuration.json"), instanciated_from = __file__)

	response = plugin.dump_request({ "i": "5", "thickness": "2", "thickness_unit": "oz", "tempdelta": 20, "tempdelta_unit": "C" })
#	assert(abs(response["width_mil"] - 35.7) < 0.1)

	response = plugin.dump_request({ "i": "15", "thickness": "1.5", "thickness_unit": "oz", "tempdelta": 20, "tempdelta_unit": "C" })
#	assert(abs(response["width_mil"] - 217) < 1)

	response = plugin.dump_request({ "i": "2", "thickness": "1", "thickness_unit": "oz", "tempdelta": 40, "tempdelta_unit": "C" })
