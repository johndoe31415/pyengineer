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
from pyengineer.NewtonSolver import DiffedFunction, NewtonSolver

_form_template = """
<form id="input_data">
	${input_text("r1", "R<sub>1</sub>", righthand_side = "Ω")}
	${input_text("r2", "R<sub>2</sub>", righthand_side = "Ω")}
	${input_text("c1", "C<sub>1</sub>", righthand_side = "F")}
	${submit_button("Calculate")}
</form>
"""

_response_template = """
${result_table_begin("Parameter", "Value")}

<tr>
	<td>R<sub>1</sub>:</td>
	<td>${d["r1"]["fmt"]}Ω</td>
</tr>

<tr>
	<td>R<sub>2</sub>:</td>
	<td>${d["r2"]["fmt"]}Ω</td>
</tr>

<tr>
	<td>C<sub>1</sub>:</td>
	<td>${d["c1"]["fmt"]}F</td>
</tr>

<tr>
	<td>t<sub>on</sub>:</td>
	<td>${d["t_on"]["fmt"]}sec</td>
</tr>

<tr>
	<td>t<sub>off</sub>:</td>
	<td>${d["t_off"]["fmt"]}sec</td>
</tr>

<tr>
	<td>Period t:</td>
	<td>${d["t"]["fmt"]}sec</td>
</tr>

<tr>
	<td>Frequency f:</td>
	<td>${d["f"]["fmt"]}Hz</td>
</tr>

<tr>
	<td>Duty Cycle:</td>
	<td>${"%.0f" % (d["duty"] * 100)}%</td>
</tr>

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "182792ec-828b-488d-b3dc-02a33e61cafa"
	_TITLE = "NE555 Timer"
	_MENU_HIERARCHY = ("ICs", "NE555")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		r1 = UnitValue(parameters["r1"])
		r2 = UnitValue(parameters["r2"])
		c1 = UnitValue(parameters["c1"])

		t_on = 0.693 * (float(r1) + float(r2)) * float(c1)
		t_off = 0.693 * float(r2) * float(c1)
		t = t_on + t_off
		f = 1 / t
		duty = t_on / t

		return {
			"r1":			r1.to_dict(),
			"r2":			r2.to_dict(),
			"c1":			c1.to_dict(),
			"t":			UnitValue(t).to_dict(),
			"t_on":			UnitValue(t_on).to_dict(),
			"t_off":		UnitValue(t_off).to_dict(),
			"f":			UnitValue(f).to_dict(),
			"duty":			duty,
		}

if __name__ == "__main__":
	from pyengineer import Configuration
	plugin = Plugin(Configuration("configuration.json"), instanciated_from = __file__)

	plugin.dump_request({ "r1": "10k", "r2": "3k", "c1": "100n" })
