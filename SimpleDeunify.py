from pyengineer import BasePlugin, UnitValue

_form_template = """
<form id="input_data">
	${input_text("input_value", "Input value")}
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

	def request(self, endpoint, parameters):
		value = UnitValue(parameters["input_value"])
		return {
			"value":		float(value),
			"value_fmt":	value.format(),
		}

	@property
	def form_template(self):
		return _form_template

	@property
	def response_template(self):
		return _response_template

if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config).request("calc", { "input": "123.456k" }))
