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

import re
import collections
from pyengineer import BasePlugin, UnitValue, InputDataException
from pyengineer.MultiRegex import MultiRegex

_form_template = """
<form id="input_data">
	${input_text("marking", "Marking")}
	${submit_button("Determine Chip")}
</form>
"""

_response_template = """
${result_table_begin("Property", "Value")}

%for (key, value) in d:
<tr>
	<td>${key}:</td>
	<td>${value}</td>
</tr>
%endfor

${result_table_end()}
"""

class Plugin(BasePlugin):
	_ID = "e336ba9b-08b6-4d1b-b2b4-c202d7fd8edd"
	_TITLE = "IC Identification"
	_MENU_HIERARCHY = ("Basics", "IC Ident")
	_FORM_TEMPLATE = _form_template
	_RESPONSE_TEMPLATE = _response_template

	_ChipRegex = MultiRegex(collections.OrderedDict((
		("stm32", re.compile("stm32f(?P<main>\d{3})(?P<q1>[a-z0-9])(?P<q2>[a-z0-9])(?P<q3>[a-z0-9])(?P<q4>[a-z0-9])", flags = re.IGNORECASE)),
	)))

	class IdentificationObject():
		def __init__(self):
			self._properties = [ ]

		@property
		def properties(self):
			return self._properties

		def _match_stm32(self, match):
			self._properties.append(("Vendor", "ST Microelectronics"))
			if match["main"] == "030":
				self._properties.append(("Core", "ARM Cortex-M0"))
				self._properties.append(("Line", "Value Line"))
			elif match["main"] == "101":
				self._properties.append(("Core", "ARM Cortex-M3"))
				self._properties.append(("Line", "Access Line"))
			elif match["main"] == "102":
				self._properties.append(("Core", "ARM Cortex-M3"))
				self._properties.append(("Line", "USB Access Line, USB 2.0 full-speed interface"))
			elif match["main"] == "103":
				self._properties.append(("Core", "ARM Cortex-M3"))
				self._properties.append(("Line", "Performance Line"))
			elif match["main"] == "765":
				self._properties.append(("Core", "ARM Cortex-M7"))
				self._properties.append(("Line", "USB OTG FS/HS, camera interface, Ethernet"))
			elif match["main"] == "767":
				self._properties.append(("Core", "ARM Cortex-M7"))
				self._properties.append(("Line", "USB OTG FS/HS, camera interface, Ethernet, LCD-TFT"))
			elif match["main"] == "768":
				self._properties.append(("Core", "ARM Cortex-M7"))
				self._properties.append(("Line", "USB OTG FS/HS, camera interface, DSI host, WLCSP with internal regulator OFF"))
			elif match["main"] == "769":
				self._properties.append(("Core", "ARM Cortex-M7"))
				self._properties.append(("Line", "USB OTG FS/HS, camera interface, Ethernet, DSI host"))

			self._properties.append(("Pin Count", {
				"f":	"20",
				"k":	"32",
				"t":	"36",
				"c":	"48",
				"r":	"64",
				"v":	"100",
				"z":	"144",
				"i":	"176",
				"a":	"180",
				"b":	"208",
				"n":	"216",
			}.get(match["q1"].lower(), "Unknown")))

			self._properties.append(("Flash Size", {
				"4":	"16 kiB",
				"6":	"32 kiB",
				"8":	"64 kiB",
				"b":	"128 kiB",
				"c":	"256 kiB",
				"f":	"768 kiB",
				"g":	"1024 kiB",
				"i":	"2048 kiB",
			}.get(match["q2"].lower(), "Unknown")))

			self._properties.append(("Package", {
				"h":	"BGA / TFBGA",
				"i":	"UFBGA",
				"k":	"UFBGA",
				"t":	"LQFP",
				"u":	"VFQFPN or UFQFPN",
				"p":	"TSSOP",
				"y":	"WLCSP",
			}.get(match["q3"].lower(), "Unknown")))

			self._properties.append(("Temperature Range", {
				"6":	"Industrial Range -40°C - 85°C",
				"7":	"Industrial Range -40°C - 105°C",
			}.get(match["q4"].lower(), "Unknown")))

	def request(self, endpoint, parameters):
		marking = parameters["marking"].strip()
		idobject = self.IdentificationObject()
		self._ChipRegex.fullmatch(marking, idobject, groupdict = True)
		return idobject.properties

if __name__ == "__main__":
	from pyengineer import Configuration
	plugin = Plugin(Configuration("configuration.json"), instanciated_from = __file__)
	plugin.dump_request({ "marking": "stm32f103c8t6" })
	plugin.dump_request({ "marking": "stm32f103rbt6" })
