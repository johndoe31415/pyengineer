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
	${input_text("period", "Target period", righthand_side = "sec")}
	${input_text("bit_width", "Counter register width", default_value = "8", righthand_side = "Bit")}
	${input_text("prescaler", "Custom clock prescaler", optional = True)}
	${submit_button("Calculate")}
</form>
"""

_response_template = """
${result_table_begin("Name", "Prescaler", "Timing", "Cycles", "Result", "Error")}

%for option in d["options"]:
<tr>
	<td>${option["name"]}</td>
	<td>1 / ${option["prescaler"]}</td>
	<td>
		Full overflow: ${option["t_full_overflow"]["fmt"]}s<br />
		Overflow frequency: ${option["f_full_overflow"]["fmt"]}Hz<br />
		Count cycle: ${option["t_cnt_cycle"]["fmt"]}s
	</td>
	<td>
		Ideal: ${option["cycles_ideal"]}<br />
		Actual: ${option["cycles"]}
	</td>
	<td>
		Preload: 0x${"%x" % (option["preload"])}<br />
		Period: ${option["actual_period"]["fmt"]}s<br />
		Frequency: ${option["actual_frequency"]["fmt"]}Hz
	</td>
	<td>${"%+.1f%%" % (100 * option["error"])}</td>
</tr>
%endfor

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "97ade7c9-e0fd-41d5-a549-cf0700822b6f"
	_TITLE = "AVR Timer"
	_MENU_HIERARCHY = ("AVR MCUs", "Timer")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	@staticmethod
	def _calculate(name, f, period, bit_width, prescaler):
		t_cnt_cycle = 1 / float(f) * prescaler
		t_full_overflow = t_cnt_cycle * (2 ** bit_width)
		cycles_ideal = round(float(period) / t_cnt_cycle)

		# However, we're limited by the counter.
		cycles = cycles_ideal
		if cycles < 1:
			cycles = 1
		elif cycles > (2 ** bit_width):
			cycles = 2 ** bit_width
		preload = (2 ** bit_width) - cycles

		actual_period = t_cnt_cycle * cycles
		error = (actual_period - float(period)) / float(period)

		return {
			"name":				name,
			"prescaler":		prescaler,
			"t_cnt_cycle":		UnitValue(t_cnt_cycle).to_dict(),
			"t_full_overflow":	UnitValue(t_full_overflow).to_dict(),
			"f_full_overflow":	UnitValue(1 / t_full_overflow).to_dict(),
			"cycles_ideal":		cycles_ideal,
			"cycles":			cycles,
			"actual_period":	UnitValue(actual_period).to_dict(),
			"actual_frequency":	UnitValue(1 / actual_period).to_dict(),
			"error":			error,
			"preload":			preload,
		}

	def request(self, endpoint, parameters):
		if parameters["f_std"] != "":
			f = UnitValue(parameters["f_std"])
		else:
			f = UnitValue(parameters["f_user"])
		ckdiv8 = "ckdiv8" in parameters
		if ckdiv8:
			f = UnitValue(f.exact_value / 8)
		period = UnitValue(parameters["period"])
		bit_width = int(parameters["bit_width"])
		if parameters["prescaler"] != "":
			user_prescaler = int(parameters["prescaler"])
		else:
			user_prescaler = None

		options = [ ]
		for prescaler_value in [ 1, 8, 64, 256, 1024 ]:
			option = self._calculate("Prescaler CK / %d" % (prescaler_value), f = f, period = period, bit_width = bit_width, prescaler = prescaler_value)
			options.append(option)
		options.sort(key = lambda opt: abs(opt["error"]))

		if user_prescaler is not None:
			option = self._calculate("User choice", f = f, period = period, bit_width = bit_width, prescaler = user_prescaler)
			options.insert(0, option)

		return {
			"options": options,
		}

if __name__ == "__main__":
	from pyengineer import Configuration
	plugin = Plugin(Configuration("configuration.json"))
	plugin.dump_request({ "f_std": "", "f_user": "16M", "period": "500u", "bit_width": "8", "prescaler": "" })
