# ![Logo](https://raw.githubusercontent.com/johndoe31415/pyengineer/master/docs/logo.png) pyengineer
[![Build Status](https://travis-ci.org/johndoe31415/pyengineer.svg?branch=master)](https://travis-ci.org/johndoe31415/pyengineer)
pyengineer is a collection of scripts that are useful for electronics or
hardware design. It is a wsgi-enabled Python application and has a GUI in your
browser. The idea is that you can adapt the software to your workshop; for
example, you tell pyengineer in the configuration file what resistors you have
at hand (configuration.json) and then, inside the UI, you can for example say
that you'd like to know what combination of parallel resistors (that you have
at hand!) make a certain value.

One of the key concepts is that additional tools (i.e., "plugins") should be
extremely simple to add and test. This is why they're all entirely
self-contained in one single file each. There's some boilerplate code inside
pyengineer which you should never have to touch because it should be sufficient
to simply write everything in that one plugin file.

## Starting it up
Just type

```
$ ./wsgi.py
```

On the command line and it should come right up:

```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 194-208-269
```

Then, go to the shown address and it should work.

## Screenshots
[Here are some screenshots of how PyEngineer looks
like.](https://johndoe31415.github.io/pyengineer/)

## Writing a plugin
Writing a plugin is extremely easy: Just copy any ".py" file inside the
"plugins/" directory to a file name you like. The only two things you will
*have* to change is: The plugin `_ID` (which should be a random type-4 UUID
that you create) and the placement inside the menu (`_MENU_HIERARCHY`). Then
you're ready to go.  pyengineer will auto-discover that new Python file in the
plugins/ directory, integrate it into the menu and show it to you.  You can
also run it without and UI from the command line. This is useful for testing
and all present plugins can do this:

```
$ python3 plugins/BasicDeunify.py
Request <default>:
{
    "input_value": "123.456k",
    "significant_digits": "4"
}
Response:
{
    "significant_digits": 4,
    "value": {
        "flt": 123456.0,
        "fmt": "123.5 k"
    }
}



123456.000 = 1.23e+05 = <strong>123.5 k</strong>
```

## Dependencies
pyengineer depends on Python3, Mako and Flask.

## License
GNU GPL-3.
