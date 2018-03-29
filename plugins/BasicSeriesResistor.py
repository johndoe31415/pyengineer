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
${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "0c1b1c49-73da-432e-acca-dfc40184aa27"
	_TITLE = "Series Resistor Calculation"
	_MENU_HIERARCHY = ("Basics", "Series Resistor")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

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

		return {
			"v_in":		v_in.json(),
			"v_load":	v_load.json(),
			"i":		i.json(),
			"v_r":		UnitValue(v_r).json(),
			"r":		UnitValue(r).json(),
			"p_r":		UnitValue(p_r).json(),
			"eta":		eta,
		}


if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config).request("calc", { "v_in": "12", "v_load": "5", "i": "10m" }))
