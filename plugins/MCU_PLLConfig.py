#	pyengineer - Helping hand for electronics and mechanical engineering
#	Copyright (C) 2012-2019 Johannes Bauer
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
from pyengineer.SortedList import SortedList

_form_template = """
<form id="input_data">
	${input_text("f_in", "Input Frequency", righthand_side = "Hz")}
	${input_text("mul", "Clock Multipliers", default_value = "2-16")}
	${input_text("div", "Clock Dividers", default_value = "1-16")}
	${input_text("f_out", "Output Frequency", righthand_side = "Hz")}
	${submit_button("Calculate")}
</form>
"""

_response_template = """
${result_table_begin("f<sub>out</sub>", "Multiplier", "Divider", "Error")}

%for option in d:
<tr>
	<td>${option["f_out"]["fmt"]}Hz</td>
	<td>${option["multiplier"]}</td>
	<td>${option["divider"]}</td>
	<td>${"%+.1f%%" % (100 * option["error"])}</td>
</tr>
%endfor

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "e51d4f32-3820-4e89-98dd-997a04a9fd4f"
	_TITLE = "PLL Clock Multiplier/Divider Calculator"
	_MENU_HIERARCHY = ("MCUs", "PLL Calculator")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	@staticmethod
	def _parse_ckfield(text):
		def _parse_subfield(text):
			if "-" in text:
				(value_from, value_to) = text.split("-", maxsplit = 1)
				value_from = int(value_from)
				value_to = int(value_to)
				yield from range(value_from, value_to + 1)
			else:
				yield int(text)

		values = set()
		for field in text.split(","):
			values |= set(_parse_subfield(field))
		return values

	def request(self, endpoint, parameters):
		f_in = UnitValue(parameters["f_in"])
		f_out = UnitValue(parameters["f_out"])
		multipliers = self._parse_ckfield(parameters["mul"])
		dividers = SortedList(self._parse_ckfield(parameters["div"]))

		results = [ ]
		ratio = float(f_out) / float(f_in)
		for multiplier in multipliers:
			ideal_divider = multiplier/ ratio
			for divider in dividers.less_more_list(ideal_divider):
				f_result = float(f_in) * multiplier / divider
				error = (f_result - float(f_out)) / float(f_out)

				result = {
					"multiplier":	multiplier,
					"divider":		divider,
					"f_out":		UnitValue(f_result).to_dict(),
					"error":		error,
				}
				results.append(result)
		results.sort(key = lambda result: abs(result["error"]))

		return results

if __name__ == "__main__":
	from pyengineer import Configuration
	plugin = Plugin(Configuration("configuration.json"), instanciated_from = __file__)
	plugin.dump_request({ "f_in": "10M", "f_out": "48M", "div": "1,2,3,4-16", "mul": "2-16" })
