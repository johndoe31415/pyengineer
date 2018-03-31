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
	_ID = "1fe6d538-5fca-4cf9-8b08-a5fbbd5a392d"
	_TITLE = "MP2307 SMPS / Mini-360 Calculator"
	_MENU_HIERARCHY = ("SMPS", "MP2307")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		v_out = UnitValue(parameters["v_out"])
		r_set = self.config.get_valuesets("r")[parameters["r_set"]]

		options = [ ]
		for r2 in r_set.iter_range(500, 50000):
			ideal_r1 = (float(v_out) / 0.925 * float(r2)) - float(r2)
			for r1 in r_set.iter_closest(ideal_r1):
				actual_v_out = 0.925 * (float(r1) + float(r2)) / float(r2)
				error = (actual_v_out - float(v_out)) / float(v_out)
				options.append({
					"r1":		r1.to_dict(),
					"r2":		r2.to_dict(),
					"v_out":	UnitValue(actual_v_out).to_dict(),
					"error":	error,
				})
		options.sort(key = lambda opt: abs(opt["error"]))
		return {
			"options": options[ : 15 ],
		}


if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config, instanciated_from = "local").request("calc", { "v_out": "3.3", "r_set": "E12" }))
