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
	${input_customset("part", "SMPS IC", values = [
		("lm2596-full", "LM2596 (-40°C to 125°C)"),
		("lm2596-25degc", "LM2596 (25°C)"),
		("xl4005", "XL4005"),
		("xl4015", "XL4015"),
		("mp1584", "MP1584"),
		("mp2307", "MP2307"),
	])}
	${input_text("v_out", "Output Voltage", righthand_side = "V")}
	${input_set("r_set", "Resistor set", valueset_group_name = "r")}
	${input_text("r_tolerance", "Resistor tolerance", righthand_side = "%", optional = True, default_value = "0")}
	${submit_button("Calculate")}
</form>
"""

_response_template = """
${result_table_begin("R<sub>1<sub>", "R<sub>2</sub>", "V<sub>out</sub>", "Error")}

%for option in d["options"]:
<tr>
	<td>${option["r1"]["fmt"]}Ω</td>
	<td>${option["r2"]["fmt"]}Ω</td>
	<td>${option["v_out_typical"]["fmt"]}V (${option["v_out_min"]["fmt"]}V – ${option["v_out_max"]["fmt"]}V)</td>
	<td>${"%+.1f%%" % (100 * option["error_typical"])} (${"%+.1f%%" % (100 * option["error_v_out_min"])} – ${"%+.1f%%" % (100 * option["error_v_out_max"])})</td>
</tr>
%endfor

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "7a227782-2457-42fc-8d88-651b491cbc9f"
	_TITLE = "SMPS ICs"
	_MENU_HIERARCHY = ("SMPS", "SMPS ICs")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template
	_VREFS = {
		"lm2596-25degc":	(1.193, 1.23, 1.267),
		"lm2596-full":		(1.18, 1.23, 1.28),
		"xl4005":			(0.776, 0.8, 0.824),
		"xl4015":			(1.225, 1.25, 1.275),
		"mp1584":			(0.776, 0.8, 0.824),
		"mp2307":			(0.900, 0.925, 0.950),
	}
	_R1_RANGE = {
		"lm2596-25degc":	(240, 1500),
		"lm2596-full":		(240, 1500),
		"xl4005":			(2e3 * 0.75, 2e3 * 1.25),
		"xl4015":			(240, 1500),
		"mp1584":			(240, 8000),	# R2 < 40k
		"mp2307":			(240, 4000),	# R2 < 100k
	}
	_R2_MAX = {
		"mp1584":			40000,
		"mp2307":			100000,
	}

	def request(self, endpoint, parameters):
		v_out = UnitValue(parameters["v_out"])
		r_set = self.config.get_valuesets("r")[parameters["r_set"]]
		(v_ref_min, v_ref_typ, v_ref_max) = self._VREFS[parameters["part"]]
		(r1_rangemin, r1_rangemax) = self._R1_RANGE[parameters["part"]]
		r2_abs_max = self._R2_MAX.get(parameters["part"])
		try:
			r_tolerance = float(parameters["r_tolerance"]) / 100
		except ValueError:
			r_tolerance = 0
		# vout = vref * (1 + (r2 / r1))
		# vout / vref = 1 + (r2 / r1)
		# (vout / vref) - 1 = r2 / r1
		# r2 = r1 * ((vout / vref) - 1)
		# r1 = r2 / ((vout / vref) - 1)

		options = [ ]
		for r1 in r_set.iter_range(r1_rangemin, r1_rangemax):
			ideal_r2 = float(r1) * ((float(v_out) / v_ref_typ) - 1)
			for r2 in r_set.iter_closest(ideal_r2):
				if (r2_abs_max is not None) and (float(r2) > r2_abs_max):
					# Invalid combination, R2 is too large
					continue

				r1_min = float(r1) * (1 - r_tolerance)
				r1_max = float(r1) * (1 + r_tolerance)
				r2_min = float(r2) * (1 - r_tolerance)
				r2_max = float(r2) * (1 + r_tolerance)

				typical_v_out = v_ref_typ * (1 + (float(r2) / float(r1)))
				minimal_v_out = v_ref_min * (1 + (r2_min / r1_max))
				maximal_v_out = v_ref_max * (1 + (r2_max / r1_min))

				error_min_v_out = (minimal_v_out - float(v_out)) / float(v_out)
				error_max_v_out = (maximal_v_out - float(v_out)) / float(v_out)
				error_typical = (typical_v_out - float(v_out)) / float(v_out)
				option = {
					"r1":				r1.to_dict(),
					"r2":				r2.to_dict(),
					"v_out_typical":	UnitValue(typical_v_out).to_dict(),
					"v_out_min":		UnitValue(minimal_v_out).to_dict(),
					"v_out_max":		UnitValue(maximal_v_out).to_dict(),
					"error_typical":	error_typical,
					"error_v_out_min":	error_min_v_out,
					"error_v_out_max":	error_max_v_out,
				}
				options.append(option)
		options.sort(key = lambda opt: abs(opt["error_typical"]))
		return {
			"options":		options[ : 15 ],
		}

if __name__ == "__main__":
	from pyengineer import Configuration
	plugin = Plugin(Configuration("configuration.json"), instanciated_from = __file__)
	plugin.dump_request({ "v_out": "3.3", "r_set": "E12", "part": "lm2596-full", "r_tolerance": "5" })
