from pyengineer import BasePlugin, UnitValue

_form_template = """
<form id="input_data">
	${input_text("input_value", "Input value")}
	${input_text("significant_digits", "Significant digits", default_value = "3")}
	${submit_button("Calculate")}
</form>
"""

_response_template = """
That's da response

${r["data"]["value_fmt"]}
"""

class Plugin(BasePlugin):
	_ID = "5583023c-88de-4eb3-b8ba-bcae6edfff14"
	_TITLE = "Deunify"
	_MENU_HIERARCHY = ("Simple Stuff", "Deunify")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	def request(self, endpoint, parameters):
		value = UnitValue(parameters["input_value"])
		significant_digits = int(parameters["significant_digits"])
		return {
			"value":				float(value),
			"value_fmt":			value.format(significant_digits = significant_digits),
			"significant_digits":	significant_digits,
		}


if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config).request("calc", { "input_value": "123.456k", "significant_digits": "4" }))
