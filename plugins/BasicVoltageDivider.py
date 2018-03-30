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
	${input_text("v_in", "Input voltage", righthand_side = "V")}
	${input_text("v_out", "Output voltage", righthand_side = "V")}
	${input_text("r_sum", "Total resistance", righthand_side = "Ω")}
	${input_set("r_set", "Resistor set", valueset_group_name = "r")}
	${input_text("r_tolerance", "Resistor tolerance", righthand_side = "%", default_value = "35")}
	${submit_button("Calculate")}
</form>
"""

_response_template = """
${result_table_begin("R<sub>1</sub>", "R<sub>2</sub>", "R<sub>total</sub>", "I", "P", "V<sub>out</sub>")}

%for option in d["options"]:
<tr>
	<td>${option["r1"]["fmt"]}Ω</td>
	<td>${option["r2"]["fmt"]}Ω</td>
	<td>${option["r_total"]["fmt"]}Ω (${"%+.1f%%" % (100 * option["r_error"])})</td>
	<td>${option["i"]["fmt"]}A</td>
	<td>${option["p"]["fmt"]}W</td>
	<td>${option["v_out"]["fmt"]}V (${"%+.1f%%" % (100 * option["v_error"])})</td>
</tr>
%endfor
${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "09d06413-06ef-4246-a8f7-6fa6015ad79f"
	_TITLE = "Voltage Divider"
	_MENU_HIERARCHY = ("Basics", "Voltage Divider")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		v_in = UnitValue(parameters["v_in"])
		v_out = UnitValue(parameters["v_out"])
		r_sum = UnitValue(parameters["r_sum"])
		r_set = self.config.get_valuesets("r")[parameters["r_set"]]
		r_tolerance = float(parameters["r_tolerance"]) / 100

		options = [ ]
		ideal_r1 = float(r_sum) * (float(v_out)) / float(v_in)
		min_r1 = ideal_r1 * (1 - r_tolerance)
		max_r1 = ideal_r1 * (1 + r_tolerance)
		for r1 in r_set.iter_range(min_r1, max_r1):
			ideal_r2 = float(r1) * (float(v_in) - float(v_out)) / float(v_out)
			for r2 in r_set.iter_closest(ideal_r2):
				opt_v_out = float(v_in) * float(r1) / (float(r1) + float(r2))
				opt_r_sum = float(r1) + float(r2)
				opt_i = float(v_in) / opt_r_sum
				opt_p = (opt_i ** 2) * opt_r_sum
				option = {
					"r1":		r1.to_dict(),
					"r2":		r2.to_dict(),
					"r_total":	UnitValue(opt_r_sum).to_dict(),
					"v_out":	UnitValue(opt_v_out).to_dict(),
					"v_error":	(opt_v_out - float(v_out)) / float(v_out),
					"r_error":	(opt_r_sum - float(r_sum)) / float(r_sum),
					"i":		UnitValue(opt_i).to_dict(),
					"p":		UnitValue(opt_p).to_dict(),
				}
				options.append(option)
		options.sort(key = lambda opt: (abs(opt["v_error"]), abs(opt["r_error"])))

		return {
			"options": options,
		}


if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config).request("calc", { "v_in": "12", "v_out": "3.3", "r_sum": "10k", "r_set": "E12", "r_tolerance": "35" }))

