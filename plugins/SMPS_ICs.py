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
%if d["r1_r2_switched"]:
<div class="warning">Warning! In our calculations, R<sub>1</sub> is always the low side. This is exactly the opposite as it is in the datasheet of this device (i.e., identifiers R<sub>1</sub> and R<sub>2</sub> are switched).</div>
%endif

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
	_VOUT = {
		"lm2596-25degc":	(1.2, 37),
		"lm2596-full":		(1.2, 37),
		"xl4005":			(0.8, 30),
		"xl4015":			(1.25, 32),
		"mp1584":			(0.8, 25),
		"mp2307":			(0.925, 20),
#		"ap3502":			(),		# Unspecified?
		"cx8509":			(0.925, 20),
	}

	# By deafult, R1 is the low side (connects to GND). For some ICs, it's the
	# exact opposite. For us, R1 is *always* the low side, i.e., for some chips
	# we might want to show a warning they're switched.
	_R1_R2_SWITCHED = {
		"mp1584":			True,
		"mp2307":			True,
		"ap3502":			True,
		"cx8509":			True,
	}
	_VREFS = {
		"lm2596-25degc":	(1.193, 1.23, 1.267),
		"lm2596-full":		(1.18, 1.23, 1.28),
		"xl4005":			(0.776, 0.8, 0.824),
		"xl4015":			(1.225, 1.25, 1.275),
		"mp1584":			(0.776, 0.8, 0.824),
		"mp2307":			(0.900, 0.925, 0.950),
		"ap3502":			(0.907, 0.925, 0.943),
		"cx8509":			(0.900, 0.925, 0.950),
	}
	_R1_RANGE = {
		"lm2596-25degc":	(240, 1500),
		"lm2596-full":		(240, 1500),
		"xl4005":			(2e3 * 0.75, 2e3 * 1.25),
		"xl4015":			(240, 1500),
		"mp1584":			(1000, 40000),		# R1 < 40k
		"mp2307":			(4700, 100000),		# R1 < 100k, ideally 10k
#		"ap3502":			(),
		"cx8509":			(4700, 100000),		# R1 < 100k, ideally 10k
	}

	def _get_vout(self, ic_name, vref, r1, r2):
		return vref * (1 + (r2 / r1))

	def _get_r2(self, ic_name, vref, r1, v_out):
		return r1 * ((v_out / vref) - 1)

	def request(self, endpoint, parameters):
		part = parameters["part"]
		v_out = UnitValue(parameters["v_out"])
		r_set = self.config.get_valuesets("r")[parameters["r_set"]]
		(v_ref_min, v_ref_typ, v_ref_max) = self._VREFS[part]
		(r1_rangemin, r1_rangemax) = self._R1_RANGE[part]
		try:
			r_tolerance = float(parameters["r_tolerance"]) / 100
		except ValueError:
			r_tolerance = 0

		# Low side R1:
		# vout = vref * (1 + (r2 / r1))
		# vout / vref = 1 + (r2 / r1)
		# (vout / vref) - 1 = r2 / r1
		# r2 = r1 * ((vout / vref) - 1)
		# r1 = r2 / ((vout / vref) - 1)

		# Low side R2:
		# r2 = r1 / ((vout / vref) - 1)

		options = [ ]
		for r1 in r_set.iter_range(r1_rangemin, r1_rangemax):
			ideal_r2 = self._get_r2(ic_name = part, vref = v_ref_typ, r1 = float(r1), v_out = float(v_out))
			for r2 in r_set.iter_closest(ideal_r2):
				r1_min = float(r1) * (1 - r_tolerance)
				r1_max = float(r1) * (1 + r_tolerance)
				r2_min = float(r2) * (1 - r_tolerance)
				r2_max = float(r2) * (1 + r_tolerance)

				typical_v_out = self._get_vout(ic_name = part, vref = v_ref_typ, r1 = float(r1), r2 = float(r2))
				extreme1_v_out = self._get_vout(ic_name = part, vref = v_ref_typ, r1 = r1_min, r2 = r2_max)
				extreme2_v_out = self._get_vout(ic_name = part, vref = v_ref_typ, r1 = r1_max, r2 = r2_min)
				minimal_v_out = min(extreme1_v_out, extreme2_v_out)
				maximal_v_out = max(extreme1_v_out, extreme2_v_out)

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
			"r1_r2_switched":		self._R1_R2_SWITCHED.get(part, False),
			"options":				options[ : 15 ],
		}

if __name__ == "__main__":
	from pyengineer import Configuration
	plugin = Plugin(Configuration("configuration.json"), instanciated_from = __file__)
	plugin.dump_request({ "v_out": "3.3", "r_set": "E12", "part": "lm2596-full", "r_tolerance": "5" })

	example_values = [
		("lm2596-full", 1e3, 8756, 12),
		("lm2596-25degc", 1e3, 8756, 12),
		("xl4005", 2e3, 28e3, 12),
		("xl4015", 3.3e3, 10e3, 5),
		("mp1584", 40.2e3, 124e3, 3.3),
		("mp2307", 10e3, 26.1e3, 3.3),
#		("ap3502", 10e3, 26.1e3, 3.3),
		("cx8509", 10e3, 44.2e3, 5),
	]
	for (chipname, r1, r2, output_voltage) in example_values:
		result = plugin.request(None, { "v_out": str(output_voltage), "r_set": "E24", "part": chipname, "r_tolerance": "0" })
		best = result["options"][0]
		assert(abs(best["v_out_typical"]["flt"] - output_voltage) < 0.25)

		best_ratio = best["r1"]["flt"] / best["r2"]["flt"]
		ratio = r1 / r2
		assert(abs((ratio - best_ratio) / best_ratio) <= 0.05)
