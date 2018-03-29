from pyengineer import BasePlugin, UnitValue

_template_source = """

<script>
function show_result(response) {

}
</script>

<form id="input_data">
	${input_text("input_value", "Input value")}
	${submit_button("Calculate")}
</form>



"""

class Plugin(BasePlugin):
	_ID = "5583023c-88de-4eb3-b8ba-bcae6edfff14"
	_TITLE = "Deunify"
	_MENU_HIERARCHY = ("Simple Stuff", "Deunify")

	def request(self, endpoint, parameters):
		return { "output": float(UnitValue(parameters["input"])) }

	@property
	def template_source(self):
		return _template_source

if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config).request("calc", { "input": "123.456k" }))
