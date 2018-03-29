from pyengineer import BasePlugin, UnitValue, InputDataException

_form_template = """
<form id="input_data">
	${input_text("v_in", "Input Voltage", righthand_side = "V")}
	${input_text("v_load", "Load Voltage", righthand_side = "V")}
	${input_text("i", "Current", righthand_side = "A")}
	${input_set("r_set", "r", "Resistor set")}
	${submit_button("Calculate")}
</form>
"""

_response_template = """
${result_table_begin("Parameter", "Symbol", "Value")}

<tr>
	<td>Input voltage:</td>
	<td>V<sub>in</sub> = </td>
	<td>${d["v_in"]["fmt"]}V</td>
</tr>
<tr>
	<td>Load voltage:</td>
	<td>V<sub>load</sub> = </td>
	<td>${d["v_load"]["fmt"]}V</td>
</tr>
<tr>
	<td>Current:</td>
	<td>I = </td>
	<td>${d["i"]["fmt"]}A</td>
</tr>
<tr>
	<td>Ideal resistor:</td>
	<td>R = </td>
	<td>${d["r"]["fmt"]}Ω</td>
</tr>
<tr>
	<td>Dissipated power:</td>
	<td>P = </td>
	<td>${d["p_r"]["fmt"]}W</td>
</tr>
<tr>
	<td>Efficiency:</td>
	<td>η = </td>
	<td>${"%.1f%%" % (100 * d["eta"])}</td>
</tr>

%for choice in d["choices"]:
<tr>
	  <th colspan="3">Resistor choice: ${choice["name"]}</th>
</tr>
<tr>
	<td>Resistor value:</td>
	<td>R = </td>
	<td>${choice["r"]["fmt"]}Ω</td>
</tr>
<tr>
	<td>Actual load voltage:</td>
	<td>V = </td>
	<td>${choice["v_load"]["fmt"]}</td>
</tr>
<tr>
	<td colspan="2">Voltage error:</td>
	<td>${"%+.1f%%" % (100 * choice["rel_error"])} / ${choice["abs_error"]["fmt"]}V</td>
</tr>
%endfor

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "0c1b1c49-73da-432e-acca-dfc40184aa27"
	_TITLE = "Series Resistor Calculation"
	_MENU_HIERARCHY = ("Basics", "Series Resistor")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	@staticmethod
	def _calculate_choice(name, r, v_in, v_load, i):
		r_load = v_load / i
		actual_v_load = v_in * r_load / (r_load + float(r))
		rel_error = (actual_v_load - v_load) / v_load
		abs_error = UnitValue(actual_v_load - v_load)
		return {
			"name":			name,
			"r":			r.json(),
			"v_load":		UnitValue(actual_v_load).json(),
			"rel_error":	rel_error,
			"abs_error":	abs_error.json(),
		}

	def request(self, endpoint, parameters):
		v_in = UnitValue(parameters["v_in"])
		v_load = UnitValue(parameters["v_load"])
		i = UnitValue(parameters["i"])

		if v_in < v_load:
			raise InputDataException("Input voltage is lower than load voltage.")

		v_r = float(v_in) - float(v_load)
		r = v_r / float(i)
		p_r = float(i) * v_r
		eta = float(v_load) / float(v_in)

		choices = [ ]
		if parameters["r_set"] != "":
			r_set = self.config.get_valuesets("r")[parameters["r_set"]]
			(smaller, larger) = r_set.find_closest(r)
			if smaller is not None:
				choices.append(self._calculate_choice("Smaller in set", r = smaller, v_in = float(v_in), v_load = float(v_load), i = float(i)))
			if larger is not None:
				choices.append(self._calculate_choice("Larger in set", r = larger, v_in = float(v_in), v_load = float(v_load), i = float(i)))

		return {
			"v_in":		v_in.json(),
			"v_load":	v_load.json(),
			"i":		i.json(),
			"v_r":		UnitValue(v_r).json(),
			"r":		UnitValue(r).json(),
			"p_r":		UnitValue(p_r).json(),
			"eta":		eta,
			"choices":	choices,
		}


if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config).request("calc", { "v_in": "12", "v_load": "5", "i": "10m" }))
