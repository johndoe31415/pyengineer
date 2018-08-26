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

from pyengineer import BasePlugin, UnitValue

_form_template = """
<form id="input_data">
	${input_text("v_out", "Output Voltage", righthand_side = "V")}
	${input_set("r_set", "Resistor set", valueset_group_name = "r")}
	<!--
	${input_text("v_in", "Input Voltage", righthand_side = "V", optional = True)}
	${input_text("l", "Inductor", righthand_side = "H", optional = True)}
	${input_text("i_out", "Output Current", righthand_side = "A", optional = True)}
	-->
	${submit_button("Calculate")}
</form>
"""

_response_template = """
${result_table_begin("R<sub>1<sub>", "R<sub>2</sub>", "V<sub>out</sub>", "Error")}

%for option in d["options"]:
<tr>
	<td>${option["r1"]["fmt"]}Ω</td>
	<td>${option["r2"]["fmt"]}Ω</td>
	<td>${option["v_out"]["fmt"]}V</td>
	<td>${"%+.1f%%" % (100 * option["error"])}</td>
</tr>
%endfor

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "7a227782-2457-42fc-8d88-651b491cbc9f"
	_TITLE = "LM2596 SMPS"
	_MENU_HIERARCHY = ("SMPS", "LM2596")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		v_out = UnitValue(parameters["v_out"])
		r_set = self.config.get_valuesets("r")[parameters["r_set"]]
		v_ref = 1.23
		# vout = vref * (1 + (r2 / r1))
		# vout / vref = 1 + (r2 / r1)
		# (vout / vref) - 1 = r2 / r1
		# r1 * ((vout / vref) - 1) = r2

		options = [ ]
		for r1 in r_set.iter_range(240, 1500):
			ideal_r2 = float(r1) * ((float(v_out) / v_ref) - 1)
			for r2 in r_set.iter_closest(ideal_r2):
				actual_v_out = v_ref * (1 + (float(r2) / float(r1)))
				error = (actual_v_out - float(v_out)) / float(v_out)
				option = {
					"r1":		r1.to_dict(),
					"r2":		r2.to_dict(),
					"v_out":	UnitValue(actual_v_out).to_dict(),
					"error":	error,
				}
				options.append(option)
		options.sort(key = lambda opt: abs(opt["error"]))
		return {
			"options":		options[ : 15 ],
		}

if __name__ == "__main__":
	from pyengineer import Configuration
	plugin = Plugin(Configuration("configuration.json"), instanciated_from = __file__)
	plugin.dump_request({ "v_out": "3.3", "r_set": "E12" })
