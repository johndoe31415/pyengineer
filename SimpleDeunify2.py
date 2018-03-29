from pyengineer import BasePlugin, UnitValue

class Plugin(BasePlugin):
	_ID = "c5af73ce-7dbe-4e1d-bb60-04da90e29b32"
	_TITLE = "muh kuh"
	_MENU_HIERARCHY = ("Simple Stuff", "moerks")

	def request(self, endpoint, parameters):
		return { "output": float(UnitValue(parameters["input"])) }

if __name__ == "__main__":
	from pyengineer import Configuration
	config = Configuration("configuration.json")
	print(Plugin(config).request("calc", { "input": "123.456k" }))
