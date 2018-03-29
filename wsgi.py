#!/usr/bin/python3
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

from pyengineer import Configuration, GUIApplication

config = Configuration("configuration.json")
gui_application = GUIApplication(config)

if __name__ == "__main__":
	import os
	plugin_dir = "plugins/"
	extra_files = [ "configuration.json" ]
	extra_files += [ plugin_dir + filename for filename in filter(lambda name: name.endswith(".py"), os.listdir(plugin_dir)) ]
	extra_files += [ "pyengineer/templates/" + filename for filename in filter(lambda name: name.endswith(".html"), os.listdir("pyengineer/templates/")) ]
	gui_application.app.run(debug = True, extra_files = extra_files)
