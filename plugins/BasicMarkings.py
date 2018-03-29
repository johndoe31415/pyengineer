from pyengineer import BasePlugin, UnitValue

_form_template = """
<form id="input_data">
	${input_text("marking", "Marking")}
	${submit_button("Determine Meaning")}
</form>
"""

_response_template = """
${result_table_begin("Component Type", "Value")}

<tr>
	<td>Resistor:</td>
	<td>${d["r"]["fmt"]}Ω</td>
</tr>
<tr>
	<td>Capacitor:</td>
	<td>${d["c"]["fmt"]}F</td>
</tr>
<tr>
	<td>Inductor:</td>
	<td>${d["l"]["fmt"]}H</td>
</tr>

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "e8ad7bb4-b0e9-4bed-b1bb-333b6fa69045"
	_TITLE = "Component Markings"
	_MENU_HIERARCHY = ("Basics", "Markings")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		marking = int(parameters["marking"])
		(base, exponent) = divmod(marking, 10)
		value = base * (10 ** exponent)
		return {
			"marking": marking,
			"r":		UnitValue(value).to_dict(),
			"c":		UnitValue(value * 1e-12).to_dict(),
			"l":		UnitValue(value * 1e-6).to_dict(),
		}


if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config).request("calc", { "input_value": "123.456k", "significant_digits": "4" }))
