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

from pyengineer import BasePlugin, UnitValue, InputDataException

_form_template = """
<form id="input_data">
	${input_text("r", "Resistor", righthand_side = "Ω")}
	${input_set("r_set", "Resistor set", valueset_group_name = "r")}
	${submit_button("Calculate")}
</form>
"""

_response_template = """
${result_table_begin("R<sub>1</sub>", "R<sub>2</sub>", "R", "Error", "Ratio")}

%for option in d["options"]:
<tr>
	<td>${option["r1"]["fmt"]}</td>
	<td>${option["r2"]["fmt"]}</td>
	<td>${option["r"]["repr"]}</td>
	<td>${"%+.1f%%" % (100 * option["error"])}</td>
	<td>1 : ${"%.1f" % (option["ratio"])} = ${"%.0f : %.0f" % (100 / (1 + option["ratio"]), 100 - (100 / (1 + option["ratio"])))}</td>
</tr>
%endfor

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "5bb9645f-46cb-4704-9efe-13e55c695482"
	_TITLE = "Parallel Resistor Calculation"
	_MENU_HIERARCHY = ("Basics", "Parallel Resistor")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		r = UnitValue(parameters["r"])
		r_set = self.config.get_valuesets("r")[parameters["r_set"]]

		options = [ ]
		for r1 in r_set:
			if r1 == r:
				continue
			ideal_r2 = 1 / ((1 / float(r)) - (1 / float(r1)))
			for r2 in r_set.iter_closest(ideal_r2):
				if r2 < r1:
					continue
				r_total = 1 / ((1 / float(r1)) + (1 / float(r2)))
				error = (r_total - float(r)) / float(r)
				if abs(error) > 0.75:
					continue
				option = {
					"r1":		r1.to_dict(),
					"r2":		r2.to_dict(),
					"r":		UnitValue(r_total, repr_callback = lambda v: v.format(significant_digits = 4)).to_dict(),
					"error":	error,
					"ratio":	float(r2) / float(r1),
				}
				options.append(option)
		options.sort(key = lambda o: (abs(o["error"]), o["ratio"]))
		return {
			"options" : options[ : 15],
		}


if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config).request("calc", { "r": "12345", "r_set": "E12" }))
