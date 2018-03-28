from pyengineer import BasePlugin, UnitValue

class Plugin(BasePlugin):
	_ID = "5583023c-88de-4eb3-b8ba-bcae6edfff14"
	_TITLE = "Deunify"
	_MENU_HIERARCHY = ("Simple Stuff", "Deunify")

	def request(self, endpoint, parameters):
		return { "output": float(UnitValue(parameters["input"])) }

	def index(self):
		return "muh content"

if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config).request("calc", { "input": "123.456k" }))
