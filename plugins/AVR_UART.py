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
	${input_set("f_std", "CPU Frequency", valueset_group_name = "frequency", valueset_name = "Crystals", empty_value = "Custom")}
	${input_text("f_user", "Custom CPU Frequency", righthand_side = "Hz")}
	${input_checkbox("ckdiv8", "Divide clock by 8 (CKDIV8)")}
	${input_checkbox("u2x", "Double speed (U2X)")}
	${submit_button("Calculate")}
</form>
"""

_response_template = """
${result_table_begin("Baudrate Target", "UBRR", "Actual Baudrate", "Deviation", "Ideal Frequency")}

%for item in d["items"]:
<tr>
	<td>${item["baudrate"]["repr"]}</td>
	<td>${item["ubrr"]}</td>
	<td>${round(item["act_baudrate"])}</td>
	<td>${"%.1f%%" % (100 * item["error"])}</td>
	<td>${item["ideal_freq"]["repr"]}Hz</td>
</tr>
%endfor

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "1abf3e17-551b-493b-bc9e-db09d50a120f"
	_TITLE = "AVR UART"
	_MENU_HIERARCHY = ("AVR MCUs", "UART")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		if parameters["f_std"] != "":
			f = UnitValue(parameters["f_std"])
		else:
			f = UnitValue(parameters["f_user"])
		ckdiv8 = "ckdiv8" in parameters
		u2x = "u2x" in parameters
		if ckdiv8:
			f = UnitValue(f.exact_value / 8)
		ckdivisor = 8 if u2x else 16

		result_items = [ ]
		for baudrate in self.config.get_valuesets("baudrate")["Standard"].values.ordered_tuple:
			ubrr = max(0, round(float(f) / (ckdivisor * float(baudrate))) - 1)
			act_baudrate = float(f) / (ckdivisor * (ubrr + 1))
			error = (act_baudrate - float(baudrate)) / float(baudrate)
			ideal_freq = float(baudrate) * (ckdivisor * (ubrr + 1))
			if ckdiv8:
				ideal_freq *= 8

			result_items.append({
				"baudrate":		baudrate.to_dict(),
				"act_baudrate":	act_baudrate,
				"ubrr":			ubrr,
				"error":		error,
				"ideal_freq":	UnitValue(ideal_freq, repr_callback = lambda value: value.format(significant_digits = 6)).to_dict(),
			})

		return {
			"items": result_items,
		}

if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config).request("calc", { "f_std": "", "f_user": "8M" }))

