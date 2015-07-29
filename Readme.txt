
AgendMPD - mpd web client
-------------------------

This web app is designed to manage an instance of the mpd (music player daemon) app.

Files
-----

requirements.txt - pip requirements file. Can be used to create the required virtual environment.
    Note that the uwsgi file is set up for a flask virtual environment.
nginx_site - nginx configuration file for the app. This file should go in /etc/nginx/sites-available.
    To activate the site, put a symbolic link to the file in /etc/nginx/sites-enabled.
    Edit this file based on your nginx server installation. If AgentMPD is the only web app running
    under nginx, you might not need to make any changes.
uwsgi_app.ini - uwsgi configuration file for the app. This file should go in /etc/uwsgi/apps-available.
    To activate the app, put a symbolic link in /etc/uwsgi/apps-enabled.
    Edit this file based on how you set up your virtualenv. If you rename the file, make sure it ends
    with .ini otherwise uwsgi will not recognize it.
runserver.py - useful for testing the app, particularly under PyCharm. This will run the app without
    involving either nginx or uwsgi.

uWSGI
-----

The stock version of uWSGI that is currently installed under Raspbian Wheezy is out of date. It is recommended
that you install the most current version of uWSGI (as identified in the requirements.txt file) and modify the init.d
script to use the version you install in a virtualenv.