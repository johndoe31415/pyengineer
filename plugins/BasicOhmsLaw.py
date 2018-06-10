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
	${input_text("v", "Voltage", righthand_side = "V")}
	${input_text("i", "Current", righthand_side = "A")}
	${input_text("r", "Resistance", righthand_side = "Ω")}
	${submit_button("Calculate")}
</form>
"""

_response_template = """
${result_table_begin("Parameter", "Symbol", "Value")}

<tr>
	<td>Voltage:</td>
	<td>V</sub> = </td>
	<td>${d["v"]["fmt"]}V</td>
</tr>
<tr>
	<td>Current:</td>
	<td>I</sub> = </td>
	<td>${d["i"]["fmt"]}A</td>
</tr>
<tr>
	<td>Resistance:</td>
	<td>R</sub> = </td>
	<td>${d["r"]["fmt"]}Ω</td>
</tr>
<tr>
	<td>Power:</td>
	<td>P</sub> = </td>
	<td>${d["p"]["fmt"]}W</td>
</tr>

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "201ebd90-808d-47e2-a398-6744112a1334"
	_TITLE = "Ohm's Law"
	_MENU_HIERARCHY = ("Basics", "Ohm's Law")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		if parameters["v"].strip() == "":
			i = UnitValue(parameters["i"])
			r = UnitValue(parameters["r"])
			v = UnitValue(float(i) * float(r))
		elif parameters["i"].strip() == "":
			r = UnitValue(parameters["r"])
			v = UnitValue(parameters["v"])
			i = UnitValue(float(v) / float(r))
		elif parameters["r"].strip() == "":
			v = UnitValue(parameters["v"])
			i = UnitValue(parameters["i"])
			r = UnitValue(float(v) / float(i))
		else:
			raise InputDataException("Exactly one of V, I, R must be left empty.")
		p = UnitValue((float(i) ** 2) * float(r))

		return {
			"v":		v.to_dict(),
			"i":		i.to_dict(),
			"r":		r.to_dict(),
			"p":		p.to_dict(),
		}

if __name__ == "__main__":
	from pyengineer import Configuration
	plugin = Plugin(Configuration("configuration.json"), instanciated_from = __file__)
	plugin.dump_request({ "v": "33", "r": "100", "i": "" })
	plugin.dump_request({ "v": "33", "r": "", "i": "1m" })
	plugin.dump_request({ "v": "", "r": "1k", "i": "1m" })
