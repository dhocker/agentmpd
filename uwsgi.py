import sys
import os
import subprocess

# Debugging code for attempts to determine why 2.7.10 cannot load urllib2
# Determined that problem was incompatibility between python 2.7.10 and the
# installed version of uwsgi that came with raspbian. The latest version of
# uwsgi is 2.0.11 and the raspbian installed version reports as 1.2.3???
# Installed uwsgi 2.0.11 in venv flask and this works with python 2.7.10.
# Changed uwsgi init.d script to use uwsgi in flask venv.

debugging = False

if debugging:
	print "sys.path"
	for p in sys.path:
		print p
	print "PYTHONPATH"
	print os.getenv("PYTHONPATH", "undefined")
	print "PYTHONHOME"
	print os.getenv("PYTHONHOME", "undefined")

	# show uwsgi version
	print "uwsgi version is:"
	print subprocess.check_output(["/home/pi/Virtualenvs/agentmpd/bin/uwsgi", "--version"])
	
	try:
		# Under 2.7.10 this statement produces the following error:
		# /home/pi/Virtualenvs/flask/lib/python2.7/lib-dynload/_io.so: undefined symbol: PyUnicodeUCS2_Replace
    		from urllib2 import parse_http_list as _parse_list_header
	except ImportError as err: # pragma: no cover
    		#from urllib.request import parse_http_list as _parse_list_header
		print "Import error for urllib2 caught"
		print err

from nu_app import app
