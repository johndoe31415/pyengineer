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
	${input_text("marking", "Marking")}
	${submit_button("Determine Meaning")}
</form>
"""

_response_template = """
${result_table_begin("Component Type", "Value")}

%if d["r"] is not None:
<tr>
	<td>Resistor:</td>
	<td>${d["r"]["fmt"]}Ω</td>
</tr>
%endif
%if d["c"] is not None:
<tr>
	<td>Capacitor:</td>
	<td>${d["c"]["fmt"]}F</td>
</tr>
%endif
%if d["l"] is not None:
<tr>
	<td>Inductor:</td>
	<td>${d["l"]["fmt"]}H</td>
</tr>
%endif

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "e8ad7bb4-b0e9-4bed-b1bb-333b6fa69045"
	_TITLE = "Component Markings"
	_MENU_HIERARCHY = ("Basics", "Markings")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		marking = parameters["marking"].strip()
		try:
			int_marking = int(marking)
		except ValueError:
			int_marking = None
		try:
			flt_marking = float(marking)
		except ValueError:
			flt_marking = None

		if (int_marking is not None) and (int_marking >= 100):
			(base, exponent) = divmod(int_marking, 10)
			value = base * (10 ** exponent)
			(r, c, l) = (1, 1e-12, 1e-6)
		elif flt_marking is not None:
			value = flt_marking
			(r, c, l) = (1, 1e-12, None)
		else:
			replacers = {
				"r":	(1,		None,	1e-6),
				"u":	(None,	1e-6,	1e-6),
				"n":	(None,	1e-9,	1e-9),
				"p":	(None,	1e-12,	None),
			}
			lmarking = marking.lower()
			for (character, (r, c, l)) in replacers.items():
				if character in lmarking:
					value = float(lmarking.replace(character, "."))
					break
			else:
				raise InputDataException("Unable to interpret \"%s\"." % (marking))
		return {
			"r":		UnitValue(value * r).to_dict() if r else None,
			"c":		UnitValue(value * c).to_dict() if c else None,
			"l":		UnitValue(value * l).to_dict() if l else None,
		}


if __name__ == "__main__":
	from pyengineer import Configuration
	plugin = Plugin(Configuration("configuration.json"))
	plugin.dump_request({ "marking": "4702" })
