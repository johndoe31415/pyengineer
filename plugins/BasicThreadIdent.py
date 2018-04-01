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

from pyengineer import BasePlugin, UnitValue, FractionalRepresentation, Thread

_form_template = """
<form id="input_data">
	${input_text("diameter", "Diameter", righthand_side = "m")}
	${input_text("length", "Length", righthand_side = "m")}
	${input_text("turns", "Over turns", default_value = "1")}
	${submit_button("Find thread")}
</form>
"""

_response_template = """
<h4>Reference</h4>
${result_table_begin("Parameter", "Symbol", "Value")}
<tr>
	<td>Diameter:</td>
	<td>d = </td>
	<td>${d["diameter"]["fmt"]}m<br />
		${"%.3f" % (d["diameter_inch"]["flt"])}" ≈ ${d["diameter_frac"]["html"]}" (${"%+.1f%%" % (100 * d["diameter_frac"]["abs_error"])})
	</td>
</tr>
<tr>
	<td>Pitch:</td>
	<td>p = </td>
	<td>${d["pitch"]["fmt"]}m / turn<br />
	${"%.1f" % (d["pitch_tpi"])} threads per inch (TPI)
	</td>
</tr>
${result_table_end()}

<h4>Candidates</h4>
${result_table_begin("Class", "Name", "Diameter", "Pitch", "Error", "Usage")}
%for candidate in d["candidates"]:
<tr>
	<td>${candidate["group"]}</td>
	<td>${candidate["name"]}</td>
	<td>
		${candidate["diameter"]["fmt"]}m<br />
		${candidate["diameter_frac"]["html"] + '"' if not candidate["diameter_frac"]["is_zero"] else ""}
	</td>
	<td>
		${candidate["pitch"]["fmt"]}m/turn<br />
		${"%.1f" % (candidate["pitch_tpi"])}
	</td>
	<td>
		Diameter ${"%+.1f%%" % (100 * candidate["diameter_err"])}<br />
		Pitch ${"%+.1f%%" % (100 * candidate["pitch_err"])}
	</td>
	<td>${candidate["usage"] or "&nbsp;"}</td>
</tr>
%endfor
${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "a955a2d2-3d66-4113-a48c-6808d464612e"
	_TITLE = "Thread Identification"
	_MENU_HIERARCHY = ("Basics", "Thread Ident")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		diameter = UnitValue(parameters["diameter"])
		length = UnitValue(parameters["length"])
		turns = int(parameters["turns"])
		pitch = float(length) / turns
		diameter_inch = UnitValue(diameter.exact_value * 10000 / 254)

		reference = Thread(diameter = float(diameter), pitch = pitch)
		candidates = list(self.config.thread_db.closest(reference))
		candidates = [ {
			"group":			candidate.group,
			"name":				candidate.name,
			"usage":			candidate.usage,
			"diameter":			UnitValue(candidate.diameter).to_dict(),
			"diameter_frac":	FractionalRepresentation(candidate.diameter * 10000 / 254, max_abs_fractional_error = 0.01).to_dict(),
			"pitch":			UnitValue(candidate.pitch).to_dict(),
			"pitch_tpi":		candidate.pitch_tpi,
			"diameter_err":		(candidate.diameter - float(diameter)) / float(diameter),
			"pitch_err":		(candidate.pitch - pitch) / pitch,
		} for candidate in candidates ]

		return {
			"diameter":			diameter.to_dict(),
			"diameter_inch":	diameter_inch.to_dict(),
			"diameter_frac":	FractionalRepresentation(diameter_inch.exact_value, max_abs_fractional_error = 0.01).to_dict(),
			"pitch":			UnitValue(pitch).to_dict(),
			"pitch_tpi":		0.0254 / pitch,
			"candidates":		candidates,
		}

if __name__ == "__main__":
	from pyengineer import Configuration
	plugin = Plugin(Configuration("configuration.json"), instanciated_from = __file__)
	plugin.dump_request({ "diameter": "3.05m", "length": "5m", "turns": "8" })
