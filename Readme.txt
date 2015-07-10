nginx_uwsgi_app
---------------

This is a boiler plate template for a Flask web app that will run under NGINX and uWSGI.
Consider it to be a prototype of the classic "Hello World" app for python based
web sites.

Files
-----

requirements.txt - pip requirements file. Can be used to create the required virtual environment.
	Note that the uwsgi file is set up for a flask virtual environment.
nginx_site - nginx configuration file for the app. This file should go in /etc/nginx/sites-available.
uwsgi_app - uwsgi configuration file for the app. This file should go in /etc/uwsgi/apps-available.
runserver.py - useful for testing the app, particularly under PyCharm. This will run the app without
	involving either nginx or uwsgi.
