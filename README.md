## Graphite exec plugin for Motorola Surfboard 6141

This tries to do a reasonable job of parsing the horrible status page.

## Installation

* git clone
* append new types to your local TypesDB
	* cat /path/to/graphite-surfboard6141/surfboard6141-types.db >> /etc/collectd.d/local-types.db
* modify exec plugin:
	* Exec nobody "python" "/path/to/graphite-surfboard6141/surfboard6141.py"

## Acknowledgements

* https://github.com/jforman/munin-surfboard6120
* https://github.com/djamps/munin-surfboard6141

